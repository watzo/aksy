#include <Python.h>
#include <stdio.h>
#include <usb.h>
#include <assert.h>
#include <time.h>
#include "akaiusb.h"
#include "aksyxusb.h"

static akai_usb_device sampler = NULL;

extern int z48_sysex_reply_ok(char* sysex_reply);

static PyObject*
AkaiSampler_init(PyObject *self, PyObject* args)
{
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* 
AkaiSampler_init_usb(PyObject *self, PyObject *args)
{
    PyObject* self_arg;
    int rc;

    if (sampler) 
    {
        return PyErr_Format(PyExc_Exception, "Sampler USB is already initialized");
    }

    if(!PyArg_ParseTuple(args, "O", &self_arg))
    {
        return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
    }

    sampler = (akai_usb_device)PyMem_Malloc(sizeof(struct _akai_usb_device));
    rc = akai_usb_device_init(sampler);

    if (rc == AKAI_NO_SAMPLER_FOUND) 
    {
        // valgrind complaint: invalid read
        PyMem_Free(sampler);
        sampler = NULL;
        return PyErr_Format(PyExc_Exception, "No sampler found");
    }

    if (rc == AKAI_USB_INIT_ERROR) 
    {
        PyMem_Free(sampler);
        sampler = NULL;
        return PyErr_Format(PyExc_Exception, "USB device init failed");
    }

    if (rc == AKAI_TRANSMISSION_ERROR) 
    {
        PyMem_Free(sampler);
        sampler = NULL;
        return PyErr_Format(PyExc_Exception, "Akai setup sequence failed");
    }

    PyObject* sysex_id_str = Py_BuildValue("s", "sysex_id");
    PyObject* sysex_id = Py_BuildValue("i", sampler->id);
    PyObject_SetAttr(self_arg, sysex_id_str, sysex_id); 
    Py_DECREF(sysex_id_str);
    Py_DECREF(sysex_id);
      Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* 
AkaiSampler_close_usb(PyObject *self, PyObject *args)
{
    int rc;

    if (!sampler)
    {
        return PyErr_Format(PyExc_Exception, "Device was not initialized so could not be closed");
    }

    rc = akai_usb_device_close(sampler);
    // valgrind: invalid read
    PyMem_Free(sampler);
    sampler = NULL;

    if (rc)
    {
        return PyErr_Format(PyExc_Exception, "Device was not successfully closed. rc: %i", rc);
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* 
AkaiSampler_reset_usb(PyObject *self, PyObject *args)
{    
    int rc;

    if (!sampler)
    {
        return PyErr_Format(PyExc_Exception, "Device was not initialized so could not be reset");
    }

    rc = akai_usb_device_reset(sampler);
    if (rc < 0)
        return PyErr_Format(PyExc_Exception, "Exeption during USB reset");

    return AkaiSampler_close_usb(self, args);
}

/* Gets a file from the sampler. Any existing file with the same name will be overwritten */
static PyObject*
AkaiSampler_get(PyObject* self, PyObject* args)
{
    PyObject *self_arg = NULL;
    unsigned char *dest, *src;
    int rc;
    char location;

    if (!sampler)
    {
        return PyErr_Format(PyExc_Exception, "Device is not initialized.");
    }


    if(!PyArg_ParseTuple(args, "Ossb", &self_arg, &src, &dest, &location))
    {
        return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
    }
    else
    {
        /* create get request */
        rc = akai_usb_device_get(sampler, src, dest, location, USB_TIMEOUT);

        if (rc) 
        {
            switch(rc)
            {
                case AKAI_FILE_NOT_FOUND:
                    return PyErr_Format(PyExc_Exception, "File not found");
                case AKAI_INVALID_FILENAME:
                    return PyErr_Format(PyExc_Exception, "Exception during transfer: invalid filename");
                case AKAI_TRANSMISSION_ERROR:
                    return PyErr_Format(PyExc_Exception, "Exception during transfer: transmission error");
                case AKAI_SYSEX_ERROR:
                    return PyErr_Format(PyExc_Exception, "Exception during transfer: sysex error");
                default:
                    return PyErr_Format(PyExc_Exception, "Unknown exception during transfer");
            }
        }
        else
        {
            Py_INCREF(Py_None);
            return Py_None;
        }
    }
}

/* uploads a file to the sampler. */
static PyObject*
AkaiSampler_put(PyObject* self, PyObject* args)
{
    PyObject *self_arg;
    unsigned char *src, *dest;
    char location;
    int rc;
            
    if(!PyArg_ParseTuple(args, "Ossb", &self_arg, &src, &dest, &location))
    {
        return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
    }
    else
    {
        rc = akai_usb_device_put(sampler, src, dest, location, USB_TIMEOUT);
        if (rc) 
        {
            switch(rc)
            {
                case AKAI_FILE_NOT_FOUND:
                    return PyErr_Format(PyExc_Exception, "Exception before transfer: file not found");
                case AKAI_FILE_STAT_ERROR:
                    return PyErr_Format(PyExc_Exception, "Exception before transfer: could not get file size");
                case AKAI_EMPTY_FILE_ERROR:
                    return PyErr_Format(PyExc_Exception, "Exception before transfer: cowardly refusing to transfer an empty file");
                case AKAI_FILE_READ_ERROR:
                    return PyErr_Format(PyExc_Exception, "Exception during transfer: error reading file");
                case AKAI_INVALID_FILENAME:
                    return PyErr_Format(PyExc_Exception, "Exception during transfer: invalid filename");
                case AKAI_TRANSMISSION_ERROR:
                    return PyErr_Format(PyExc_Exception, "Exception during transfer: transmission error");
                case AKAI_SYSEX_ERROR:
                    return PyErr_Format(PyExc_Exception, "Exception during transfer: sysex error");
                default:
                    return PyErr_Format(PyExc_Exception, "Unknown exception during transfer");
            }
        }
        else
        {
            Py_INCREF(Py_None);
            return Py_None;
        }
    }
}

static PyObject*
AkaiSampler_execute(PyObject* self, PyObject* args)
{
    PyObject *self_arg, *ret;
    char* sysex_command;
    int sysex_length, rc;
    const int BUFF_SIZE = 4096;
    unsigned char* buffer;

    if (!sampler)
    {
        return PyErr_Format(PyExc_Exception, "USB not initialized. Call init_usb first");
    }

    if(!PyArg_ParseTuple(args, "Os#", &self_arg, &sysex_command, &sysex_length))
    {
        return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
    }
    else
    {
        buffer = (unsigned char*)PyMem_Malloc( BUFF_SIZE * sizeof(unsigned char));
        buffer = memset(buffer, 128, sizeof(unsigned char));
        rc = akai_usb_device_exec_sysex(
            sampler, sysex_command, sysex_length, buffer, BUFF_SIZE, USB_TIMEOUT);

        if (rc < 0)
        {
            ret = PyErr_Format(PyExc_Exception, "Error reading sysex reply, rc: %i.", rc);
        }
        else
        {
            ret = Py_BuildValue("s#", buffer, rc); 
        }

        // valgr: val unitialized?
        PyMem_Free(buffer);
        return ret;
    }
}

static PyMethodDef AkaiSamplerMethods[] = 
{
    {"__init__", AkaiSampler_init, METH_O, ""},
    {"init_usb", AkaiSampler_init_usb, METH_VARARGS, "Initializes USB device and interface."},
    {"reset_usb", AkaiSampler_reset_usb, METH_VARARGS, "Resets USB device and interface."},
    {"close_usb", AkaiSampler_close_usb, METH_O, "Closes USB device and interface."},
    {"_get", AkaiSampler_get, METH_VARARGS, "Gets a file from the sampler"},
    {"_put", AkaiSampler_put, METH_VARARGS, "Puts a file on the sampler"},
    {"_execute", AkaiSampler_execute, METH_VARARGS, "Executes a Sysex string on the sampler"},
    {NULL},
};

static PyMethodDef ModuleMethods[] = { {NULL} };

#ifdef __cplusplus
extern "C"
#endif

void initaksyxusb()
{
    PyMethodDef *def;

    /* create a new module and class */
    /* TODO: prevent multiple instances */
    PyObject *module = Py_InitModule("aksyxusb", ModuleMethods);
    PyObject *moduleDict = PyModule_GetDict(module);
    PyObject *classDict = PyDict_New();
    PyObject *className = PyString_FromString("AkaiSampler");
    PyObject *aksyxClass = PyClass_New(NULL, classDict, className);

    PyObject* loc_disk_str = Py_BuildValue("s", "DISK");
    PyObject* loc_disk_id = Py_BuildValue("i", LOC_DISK);
    PyObject* loc_mem_str = Py_BuildValue("s", "MEMORY");
    PyObject* loc_mem_id = Py_BuildValue("i", LOC_MEMORY);

    PyDict_SetItemString(moduleDict, "AkaiSampler", aksyxClass);

    PyObject_SetAttr(aksyxClass, loc_disk_str, loc_disk_id); 
    PyObject_SetAttr(aksyxClass, loc_mem_str, loc_mem_id); 

    Py_DECREF(loc_disk_str);
    Py_DECREF(loc_mem_str);
    Py_DECREF(loc_disk_id);
    Py_DECREF(loc_mem_id);
    Py_DECREF(classDict);
    Py_DECREF(className);
    Py_DECREF(aksyxClass);
    
    /* add methods to class */
    for (def = AkaiSamplerMethods; def->ml_name != NULL; def++) 
    {
        PyObject *func = PyCFunction_New(def, NULL);
        PyObject *method = PyMethod_New(func, NULL, aksyxClass);
        PyDict_SetItemString(classDict, def->ml_name, method);
        Py_DECREF(func);
        Py_DECREF(method);
    }
}

