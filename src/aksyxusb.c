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
		// int retval = usb_set_configuration(akai_z48, 1);
		int retval = usb_claim_interface(akai_z48, 0);
		printf("Retval: %i \n", retval);
		// retval = usb_set_altinterface(akai_z48, 0);

		if (retval)
		{
			return PyErr_Format(PyExc_Exception, "USB initialization failed. Check permissions on device.");
		}


		char setupmsg[] = "\x03\x01";
	    //char msg1[] = "\x10\x08\x0\xF0\x47\x5F\x0\x20\x5\xF7";
	    char msg[] = "\x10\x08\x00\xF0\x47\x5F\x00\x00\x01\x00\xF7";
	    retval = usb_bulk_write(akai_z48, 0x82, setupmsg, 2, 5000);
		unsigned char buffer[8];
	    retval = usb_bulk_write(akai_z48, 0x82, msg, 11, 5000);
	 	retval = usb_bulk_read(akai_z48,0x02,buffer,8,1000);

		/*
		int i;
		for(i=0; i<retval; i++) {
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

	int retval = usb_release_interface(akai_z48, 0);
	retval = usb_close (akai_z48)|retval;
	akai_z48 = 0;

	if (retval)
	{
		
		return PyErr_Format(PyExc_Exception, "USB was not successfully closed");
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
		int retval = usb_bulk_write(akai_z48, 0x82, sysex_command, string_length, 1000);
		unsigned char* buffer = (unsigned char*)PyMem_Malloc( 64 * sizeof(unsigned char));
		retval = usb_bulk_read(akai_z48,0x02,buffer,64,1000);  
   		printf("Z48Sampler.execute finished with retval %i\n", retval);

		if (retval < 0)
		{
			PyMem_Free(buffer);
			return PyErr_Format(PyExc_Exception, "Error reading sysex reply.");
		}

		PyObject* ret;

		/* debug printing */
		int i = 0;
		for(i=0; i<retval; i++) 
		{
			printf("%02x", buffer[i]);
			if(i % 16 == 15) printf("\n");
			else printf(" ");
		}
		ret = Py_BuildValue("s#", buffer, retval); 
		PyMem_Free(buffer);
		return ret;
	}
}

static PyMethodDef Z48SamplerMethods[] = 
{
    {"__init__", Z48Sampler_init, METH_O, "init"},
    {"init_usb", Z48Sampler_init_usb, METH_O, "Initializes USB device and end point"},
    {"close_usb", Z48Sampler_close_usb, METH_O, "Closes USB device and end point"},
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
	/* TODO: extend object */
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

