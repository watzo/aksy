#include <Python.h>
#include <stdio.h>
#include <usb.h>
#include <assert.h>
#include <time.h>
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

	for (bus = usb_get_busses(); bus; bus = bus->next) 
	{
		for (dev = bus->devices; dev; dev = dev->next) 
		{
		  // found the akai z4 or z8
		  if (dev->descriptor.idVendor == VENDOR_ID && dev->descriptor.idProduct == PRODUCT_ID)
		  {
			akai_z48 = usb_open(dev);
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

		if (rc)
		{
			return PyErr_Format(PyExc_Exception, "USB initialization failed. Check permissions on device. rc: %i.", rc);
		}


		/* setup sequence (sniffed from windows usblog) */
		unsigned char* setup_msg = "\x03\x01";
	    rc = usb_bulk_write(akai_z48, EP_OUT, setup_msg, 2, 1000);

		/* turn of confirmation messages */
	    unsigned char* msg = "\x10\x08\x00\xF0\x47\x5F\x00\x00\x01\x00\xF7";
		unsigned char buffer[64];
	    rc = usb_bulk_write(akai_z48, EP_OUT, msg, 11, 1000);
		/* DONE message */
	 	rc = usb_bulk_read(akai_z48,EP_IN, buffer, 8, 1000);

		/* disable sync sysex current item and display */
		msg = "\x10\x08\x00\xf0\x47\x5f\x00\x00\x03\x00\xf7"; 
	    rc = usb_bulk_write(akai_z48, EP_OUT, msg, 11, 1000);
		/* sync DONE message */
	 	rc = usb_bulk_read(akai_z48,EP_IN,buffer,10,1000);

		/* disable checksums */
		msg = "\x10\x07\x00\xf0\x47\x5f\x00\x04\x00\xf7";
	    rc = usb_bulk_write(akai_z48, EP_OUT, msg, 10, 1000);
		/* DONE message */
	 	rc = usb_bulk_read(akai_z48,EP_IN, buffer, 64, 1000);

    	Py_INCREF(Py_None);
	    return Py_None;
	}

}

static PyObject* 
Z48Sampler_close_usb(PyObject *self, PyObject *args)
{
	if (!akai_z48)
	{
		return PyErr_Format(PyExc_Exception, "USB was not initialized so could not be closed");
	}

	int rc = usb_release_interface(akai_z48, 0);
	rc = usb_close (akai_z48)|rc;
	akai_z48 = 0;

	if (rc)
	{
		return PyErr_Format(PyExc_Exception, "USB was not successfully closed. rc: %i", rc);
	}

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
		return PyErr_Format(PyExc_Exception, "USB connection was not successfully reset, rc: %i.", rc);
	}

    Py_INCREF(Py_None);
    return Py_None;
}

/* Gets a file from the sampler */
static PyObject*
Z48Sampler_get(PyObject* self, PyObject* args)
{
	PyObject* self_arg;
	unsigned char *dest, *src, *command, *buffer;
	int src_len, dest_len, bytes_to_read;
	FILE* fp;

#ifdef _POSIX_SOURCE
	struct timeval t1, t2;
	float elapsed, kbps;
#endif

	if(!PyArg_ParseTuple(args, "Os#s#", &self_arg, &src, &src_len, &dest, &dest_len))
	{
		return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
	}
	else
	{
		/* create 'get' command: 0x41 and the name of the file to transfer */
		command = (unsigned char*) PyMem_Malloc((src_len+1) * sizeof(unsigned char));
		command[0] = GET_COMMAND;
		memcpy(command+1, src, src_len * sizeof(unsigned char));

		usb_bulk_write(akai_z48, EP_OUT, command, src_len+1, 500);
		PyMem_Free(command);

		/* get the number of bytes to read */
		buffer = (unsigned char*)PyMem_Malloc(8 * sizeof(unsigned char));
		int rc = usb_bulk_read(akai_z48, EP_IN, buffer, 8, 500);  
		bytes_to_read = (buffer[7]
				| buffer[6] << 8 
				| buffer[5] << 16 
				| buffer[4] << 24);

		PyMem_Free(buffer);
		buffer = (unsigned char*)PyMem_Malloc(bytes_to_read * sizeof(unsigned char));
#ifdef _POSIX_SOURCE
	   	gettimeofday(&t1, NULL); // timeval, timezone struct
#endif
		rc = usb_bulk_read(akai_z48, EP_IN, buffer, bytes_to_read, 5000);  

		if (rc < 0)
		{
			PyMem_Free(buffer);
			return PyErr_Format(PyExc_Exception, "File was not successfully transferred.");
		}
		else
		{
#ifdef _POSIX_SOURCE
			gettimeofday(&t2, NULL); // timeval, timezone struct
			elapsed = (t2.tv_usec - t1.tv_usec)/1000.0f;
			kbps = bytes_to_read/(1024*elapsed);
			printf("Transfered %i bytes in elapsed %4f (%4f kB/s)\n", rc, elapsed, kbps); 
#endif
			assert (rc == bytes_to_read);

			/* write the file */
			fp = fopen(dest, "w");
			fwrite(buffer, sizeof(unsigned char), rc, fp);
			fclose(fp);
			PyMem_Free(buffer);
			Py_INCREF(Py_None);
			return Py_None;
		}
	}
}

/* uploads a file to the sampler. */
static PyObject*
Z48Sampler_put(PyObject* self, PyObject* args)
{
	PyObject *self_arg;
	unsigned char *src, *dest, *buf;
	int src_len, dest_len;
	FILE* fp;

	if(!PyArg_ParseTuple(args, "Os#s#", &self_arg, &src, &src_len, &dest, &dest_len))
	{
		return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
	}
	else
	{
		/* Get file info */
		struct stat* st = (struct stat*)PyMem_Malloc(sizeof(struct stat));
		stat(src, st);
		int bytes_to_write = st->st_size;
		//  read in st->st_blksize ???
		PyMem_Free(st);
		buf = PyMem_Malloc(bytes_to_write * sizeof(unsigned char));

		fp = fopen(src, "r");
		fread(buf, sizeof(unsigned char), bytes_to_write, fp);
		fclose(fp);
		// command sequence ?
		// usb_bulk_write(akai_z48, EP_OUT, buf, bytes_to_write); 
		/* write the file data */
		int rc = usb_bulk_write(akai_z48, EP_OUT, buf, bytes_to_write, 1000); 

		if (rc < 0 || rc < bytes_to_write)
		{
			PyMem_Free(buf);
			return PyErr_Format(PyExc_Exception, "File transfer failed.");
		}
		else
		{
			PyMem_Free(buf);
			Py_INCREF(Py_None);
			return Py_None;
		}
	}

}

PyObject*
Z48Sampler_execute(PyObject* self, PyObject* args)
{
	PyObject *self_arg, *ret;
	char* sysex_command;
	int string_length, rc;

	unsigned char* buffer;

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
		usb_bulk_write(akai_z48, EP_OUT, sysex_command, string_length, 500);
		buffer = (unsigned char*)PyMem_Malloc( 1024 * sizeof(unsigned char));
		rc = usb_bulk_read(akai_z48, EP_IN, buffer, 1024, 500);  

		if (rc < 0)
		{
			PyMem_Free(buffer);
			return PyErr_Format(PyExc_Exception, "Error reading sysex reply, rc: %i.", rc);
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
    {"reset_usb_conn", Z48Sampler_reset_usb_conn, METH_O, "Resets USB endpoints."},
    {"close_usb", Z48Sampler_close_usb, METH_O, "Closes USB device and interface."},
    {"_get", Z48Sampler_get, METH_VARARGS, "Gets a file from the sampler"},
    {"_put", Z48Sampler_put, METH_VARARGS, "Puts a file on the sampler"},
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

