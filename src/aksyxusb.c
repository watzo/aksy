#include <Python.h>
#include <usb.h>
#include "aksyxusb.h"

static struct usb_dev_handle *akai_z48 = 0;

static PyObject* 
Z48Sampler_init(PyObject *self, PyObject* args)
{
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* 
Z48Sampler_init_usb(PyObject *self, PyObject *args)
{
	if (akai_z48) 
	{
		return PyErr_Format(PyExc_Exception, "USB is already initialized");
	}

	struct usb_bus *bus;
	struct usb_device *dev;

	usb_init();

	usb_find_busses();
	usb_find_devices();

	for (bus = usb_busses; bus; bus = bus->next) 
	{
		for (dev = bus->devices; dev; dev = dev->next) 
		{
		  // found the akai z4 or z8
		  if (dev->descriptor.idVendor == VENDOR_ID && dev->descriptor.idProduct == PRODUCT_ID)
		  {
			akai_z48 = usb_open(dev);
			// printf("Opening device\n");
			break;
		  }
		}
	}

	if (!akai_z48) 
	{
		return PyErr_Format(PyExc_Exception, "No sampler found");
	}
	else
	{
		int rc = usb_claim_interface(akai_z48, 0);
		printf("Retval: %i \n", rc);

		if (rc)
		{
			return PyErr_Format(PyExc_Exception, "USB initialization failed. Check permissions on device.");
		}


		/* setup sequence (sniffed from windows usblog) */
		char setupmsg[] = "\x03\x01";
	    rc = usb_bulk_write(akai_z48, EP_OUT, setupmsg, 2, 5000);

		/* turn of confirmation messages */
	    char msg[] = "\x10\x08\x00\xF0\x47\x5F\x00\x00\x01\x00\xF7";
		unsigned char buffer[8];
	    rc = usb_bulk_write(akai_z48, EP_OUT, msg, 11, 5000);
	 	rc = usb_bulk_read(akai_z48,EP_IN,buffer,8,1000);

		/*
		int i;
		for(i=0; i<rc; i++) {
       		printf("%02x", buffer[i]);
        	if(i % 16 == 15) printf("\n");
        	else printf(" ");
   		}
                                                                                                                                                           
      	printf("\n");
		*/
    	Py_INCREF(Py_None);
	    return Py_None;
	}

}

static PyObject* 
Z48Sampler_close_usb(PyObject *self, PyObject *args)
{
	if (!akai_z48)
	{
		return PyErr_Format(PyExc_Exception, "USB was not initialized so couldn't not closed");
	}

	int rc = usb_release_interface(akai_z48, 0);
	rc = usb_close (akai_z48)|rc;
	akai_z48 = 0;

	if (rc)
	{
		return PyErr_Format(PyExc_Exception, "USB was not successfully closed");
	}

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* 
Z48Sampler_reset_usb(PyObject *self, PyObject *args)
{
	if (!akai_z48)
	{
		return PyErr_Format(PyExc_Exception, "USB was not initialized so couldn't not reset");
	}

	int rc = usb_reset(akai_z48);

	if (rc)
	{
		return PyErr_Format(PyExc_Exception, "USB was not successfully reset");
	}
	
	akai_z48 = 0;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* 
Z48Sampler_reset_usb_conn(PyObject *self, PyObject *args)
{
	int rc = usb_clear_halt(akai_z48, EP_IN);
	rc = rc | usb_clear_halt(akai_z48, EP_OUT);

	if (rc)
	{
		return PyErr_Format(PyExc_Exception, "USB connection was not successfully reset.");
	}

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject*
Z48Sampler_execute(PyObject* self, PyObject* args)
{
	char* sysex_command;
	int string_length;
	PyObject* self_arg;

	if (!akai_z48)
	{
		return PyErr_Format(PyExc_Exception, "USB not initialized. Call init_usb first");
	}

	if(!PyArg_ParseTuple(args, "Os#", &self_arg, &sysex_command, &string_length))
	{
		return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
	}
	else
	{
		usb_bulk_write(akai_z48, EP_OUT, sysex_command, string_length, 1000);
		unsigned char* buffer = (unsigned char*)PyMem_Malloc( 64 * sizeof(unsigned char));
		int rc = usb_bulk_read(akai_z48,EP_IN,buffer,64,1000);  
   		printf("Z48Sampler.execute finished with rc %i\n", rc);

		if (rc < 0)
		{
			PyMem_Free(buffer);
			return PyErr_Format(PyExc_Exception, "Error reading sysex reply.");
		}

		PyObject* ret;

		/* debug printing */
		int i;
		for(i = 0; i < rc; i++) 
		{
			printf("%02x", buffer[i]);
			if(i % 16 == 15 || i == rc - 1) printf("\n");
			else printf(" ");
		}

		ret = Py_BuildValue("s#", buffer, rc); 
		PyMem_Free(buffer);
		return ret;
	}
}

static PyMethodDef Z48SamplerMethods[] = 
{
    {"__init__", Z48Sampler_init, METH_O, "init"},
    {"init_usb", Z48Sampler_init_usb, METH_O, "Initializes USB device and interface."},
    {"_reset_usb", Z48Sampler_reset_usb, METH_O, "Resets USB device."},
    {"reset_usb_conn", Z48Sampler_reset_usb_conn, METH_O, "Resets USB endpoints."},
    {"close_usb", Z48Sampler_close_usb, METH_O, "Closes USB device and interface."},
    {"_execute", Z48Sampler_execute, METH_VARARGS, "Executes a Sysex string on the sampler"},
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
    PyObject *className = PyString_FromString("Z48Sampler");
    PyObject *aksyxClass = PyClass_New(NULL, classDict, className);
    PyDict_SetItemString(moduleDict, "Z48Sampler", aksyxClass);
    Py_DECREF(classDict);
    Py_DECREF(className);
    Py_DECREF(aksyxClass);
    
    /* add methods to class */
    for (def = Z48SamplerMethods; def->ml_name != NULL; def++) 
	{
		PyObject *func = PyCFunction_New(def, NULL);
		PyObject *method = PyMethod_New(func, NULL, aksyxClass);
		PyDict_SetItemString(classDict, def->ml_name, method);
		Py_DECREF(func);
		Py_DECREF(method);
    }
}

