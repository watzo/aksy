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
	if (sampler) 
	{
		return PyErr_Format(PyExc_Exception, "Sampler USB is already initialized");
	}

    // sampler = malloc(sizeof(struct _akai_usb_device));
	sampler = (akai_usb_device)PyMem_Malloc(sizeof(struct _akai_usb_device));
    int rc = akai_usb_device_init(sampler);

	if (rc == AKAI_NO_SAMPLER_FOUND) 
	{
		return PyErr_Format(PyExc_Exception, "No sampler found");
	}

	if (rc == AKAI_USB_INIT_ERROR) 
	{
		return PyErr_Format(PyExc_Exception, "USB device init failed");
	}

	if (rc == AKAI_TRANSMISSION_ERROR) 
	{
		return PyErr_Format(PyExc_Exception, "Akai setup sequence failed");
	}

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
    PyMem_Free(sampler);

	if (rc)
	{
		return PyErr_Format(PyExc_Exception, "Device was not successfully closed. rc: %i", rc);
	}

    Py_INCREF(Py_None);
    return Py_None;
}

/* Gets a file from the sampler. Any existing file with the same name will be overwritten */
static PyObject*
AkaiSampler_get(PyObject* self, PyObject* args)
{
	PyObject *self_arg = NULL;
	unsigned char *dest, *src;
	int rc, location;

	if (!sampler)
	{
		return PyErr_Format(PyExc_Exception, "Device is not initialized.");
	}


	if(!PyArg_ParseTuple(args, "Ossi", &self_arg, &src, &dest, &location))
	{
		return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
	}
	else
	{
		/* Z48_MEMORY_GET + ITEM HANDLE */
		/* create get request */
        rc = akai_usb_device_get(sampler, src, dest, location, USB_TIMEOUT);

        if (rc)
		{
		    return PyErr_Format(PyExc_Exception, "Exception during transfer");
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
	char destination = 0x0;
	int rc;
			
	if(!PyArg_ParseTuple(args, "Ossb", &self_arg, &src, &dest, &destination))
	{
		return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
	}
	else
	{

        rc = akai_usb_device_put(sampler, src, dest, USB_TIMEOUT);
		if (rc)
		{
			return PyErr_Format(PyExc_Exception, "File transfer failed.");
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
		buffer = (unsigned char*)PyMem_Malloc( 4096 * sizeof(unsigned char));
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

		PyMem_Free(buffer);
		return ret;
	}
}

static PyMethodDef AkaiSamplerMethods[] = 
{
    {"__init__", AkaiSampler_init, METH_O, ""},
    {"init_usb", AkaiSampler_init_usb, METH_O, "Initializes USB device and interface."},
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
    PyDict_SetItemString(moduleDict, "AkaiSampler", aksyxClass);
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

