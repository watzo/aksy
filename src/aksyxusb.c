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
	struct usb_bus *bus;
	struct usb_device *dev;

	if (akai_z48) 
	{
		return PyErr_Format(PyExc_Exception, "USB is already initialized");
	}


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

        // disable confirmation messages
		unsigned char buf[8];
        char* msg = "\x10\x08\x00\xf0\x47\x5f\x00\x00\x01\x00\xf7";
		rc = usb_bulk_write(akai_z48, EP_OUT, msg, 11, USB_TIMEOUT);  
		rc = usb_bulk_read(akai_z48, EP_IN, buf, 8, USB_TIMEOUT);  
		rc = usb_bulk_read(akai_z48, EP_IN, buf, 8, USB_TIMEOUT);  

    	Py_INCREF(Py_None);
	    return Py_None;
	}

}

static PyObject* 
Z48Sampler_close_usb(PyObject *self, PyObject *args)
{
	int rc;

	if (!akai_z48)
	{
		return PyErr_Format(PyExc_Exception, "USB was not initialized so could not be closed");
	}

	rc = usb_release_interface(akai_z48, 0);
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
Z48Sampler_clear_remote_buf(PyObject *self, PyObject *args)
{
	int rc = 1, read = 0;
	unsigned char buf[1];
	usb_bulk_write(akai_z48, EP_OUT, "\x00", 1, USB_TIMEOUT);  
	while (rc > 0)
	{
		rc = usb_bulk_read(akai_z48, EP_IN, buf, 1, USB_TIMEOUT);  
		read += rc;
	}

	printf("%i bytes read from endpoint\n", read);
    Py_INCREF(Py_None);
    return Py_None;
}

/* Checks whether buffer is an ok reply (0x41 0x6b 0x61 0x49). Caller must ensure buffer points to an array with 4 elements */
inline int 
z48_reply_ok(unsigned char* buffer)
{
	if (buffer[0] != 0x41) return 0;
	if (buffer[1] != 0x6b) return 0;
	if (buffer[2] != 0x61) return 0;
	if (buffer[3] != 0x49) return 0;
	return 1;
}

#ifdef _POSIX_SOURCE
void
print_transfer_stats(struct timeval t1, struct timeval t2, int bytes_transferred)
{
	float elapsed, kbps;
	gettimeofday(&t2, NULL); // timeval, timezone struct
	// get elapsed time in seconds. 
	elapsed = (t2.tv_sec - t1.tv_sec) + (t2.tv_usec - t1.tv_usec)/1000000.0f;
	kbps = bytes_transferred/(1024*elapsed);
	printf("Transfered %i bytes in elapsed %6f (%6f kB/s)\n", bytes_transferred, elapsed, kbps); 
}
#endif

/* Gets a file from the sampler. Any existing file with the same name will be overwritten */
static PyObject*
Z48Sampler_get(PyObject* self, PyObject* args)
{
	PyObject *self_arg, *ret = NULL;
	unsigned char *dest, *src, *command, *data;
	int src_len, dest_len, block_size = 4096*4, bytes_transferred = 0;
	FILE* fp;
	int rc = 0;

#ifdef _POSIX_SOURCE
	struct timeval t1, t2;
#endif

	if(!PyArg_ParseTuple(args, "Os#s#", &self_arg, &src, &src_len, &dest, &dest_len))
	{
		return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
	}
	else
	{
		/* Z48_MEMORY_GET + ITEM HANDLE */
		/* create get request */
		command = (unsigned char*) PyMem_Malloc((src_len+1) * sizeof(unsigned char));
		command[0] = Z48_DISK_GET;
		memcpy(command+1, src, src_len * sizeof(unsigned char));

		usb_bulk_write(akai_z48, EP_OUT, command, src_len+1, USB_TIMEOUT);
		PyMem_Free(command);

		fp = fopen(dest, "w+"); 

		data = PyMem_Malloc(block_size * sizeof(unsigned char));
#ifdef _POSIX_SOURCE
	   	gettimeofday(&t1, NULL); // timeval, timezone struct
#endif


		do
		{
			rc = usb_bulk_read(akai_z48, EP_IN, data, block_size, USB_TIMEOUT);  

			if (rc == block_size)
			{
				bytes_transferred+= rc;

				/* write to file */
				fwrite(data, sizeof(unsigned char), rc, fp);

				/* sent continue request */
				usb_bulk_write(akai_z48, EP_OUT, "\x00", 1, USB_TIMEOUT);  
			}	
			else if (rc == 8)
			{
				/* get the number of bytes to read */
#ifdef _DEBUG
				printf("Current block size: %i. Bytes read now: %i, Total bytes read: %i. Advertised: %i\n", 
					block_size, rc, bytes_transferred, GET_BYTES_TRANSFERRED(data));
#endif
				if (bytes_transferred > 0) 
				{
					block_size = GET_BLOCK_SIZE(data);
					if (block_size == 0)
					{
						/* file transfer completed */
						break;
					}
				}
			}
			else if (rc == 4 && z48_reply_ok(data))	
			{
				continue;
			}
			else
			{
				printf("At bulk read: Unexpected reply, rc %i or unexpected end of transmission.\n", rc);
				ret = PyErr_Format(PyExc_Exception, "Transmission Error."); 
			}

		} while(rc > 0);

		/* close the file */
		fclose(fp);
		PyMem_Free(data);

		if (ret != NULL)
		{
			return ret;
		}
		else
		{
#ifdef _POSIX_SOURCE
			print_transfer_stats(t1, t2, bytes_transferred);
#endif
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
	unsigned char *src, *dest, *buf, *command, *reply_buf;
	char destination = 0x0;
	int src_len, dest_len, filesize, rc, blocksize = 4096 * 4, bytes_transferred = 0, bytes_read = 0;
	FILE* fp;
			
#ifdef _POSIX_SOURCE
	struct timeval t1, t2;
#endif
	if(!PyArg_ParseTuple(args, "Os#s#b", &self_arg, &src, &src_len, &dest, &dest_len, &destination))
	{
		return PyErr_Format(PyExc_Exception, "Arguments could not be parsed");
	}
	else
	{
		/* Get file info */
		struct stat* st = (struct stat*)PyMem_Malloc(sizeof(struct stat));
		rc = stat(src, st);

		if (rc < 0)
		{
			PyMem_Free(st);
			return PyErr_Format(PyExc_Exception, "Could not stat file %s. rc: %i", src, rc);
		}

		filesize = st->st_size;
		//  read in st->st_blksize ???
		PyMem_Free(st);
		buf = PyMem_Malloc(filesize * sizeof(unsigned char));

		fp = fopen(src, "r");

		printf("File name to upload %s, Size of file: %i bytes\n", dest, filesize);
		/* create 'put' command: 0x41, byte size and the name of the file to transfer */
		command = (unsigned char*) PyMem_Malloc((dest_len+5) * sizeof(unsigned char));
		command[0] = (destination)?Z48_DISK_PUT:Z48_MEMORY_PUT;
		command[1] = filesize >> 24;
		command[2] = filesize >> 16;
		command[3] = filesize >> 8;
		command[4] = filesize;

		memcpy(command+5, dest, dest_len * sizeof(unsigned char));

		rc = usb_bulk_write(akai_z48, EP_OUT, command, dest_len+5, 1000); 

		reply_buf = (unsigned char*) PyMem_Malloc(64 * sizeof(unsigned char));

#ifdef _POSIX_SOURCE
	   	gettimeofday(&t1, NULL); // timeval, timezone struct
#endif

		do 
		{
			rc = usb_bulk_read(akai_z48, EP_IN, reply_buf, 64, 1000); 

			if (rc == 4 && z48_reply_ok(reply_buf))	
			{
				continue;
			}
			else if (rc == 8)
			{
	
#ifdef _DEBUG
				int i = 0;
				for (; i < rc; i++)
					printf("%02x ", reply_buf[i]);
				printf("\n");
#endif
				blocksize = GET_BLOCK_SIZE(reply_buf);	
				if (GET_BYTES_TRANSFERRED(reply_buf) == filesize) 
				{
					continue;
				}
			}
			else if (rc == 5)
			{
				break; // finished TODO: check contents of buffer...
			}

			/* check is probably not necessary */
			if (! feof(fp))
			{
				bytes_read = fread(buf, sizeof(unsigned char), blocksize, fp);

				usb_bulk_write(akai_z48, EP_OUT, buf, bytes_read, 1000); 
				bytes_transferred += bytes_read;

			}

			/* continue */
			usb_bulk_write(akai_z48, EP_OUT, "\x00", 1, 1000); 
		} while(rc > 0);

#ifdef _POSIX_SOURCE
		print_transfer_stats(t1, t2, bytes_transferred);
#endif
		fclose(fp);

		PyMem_Free(reply_buf);
		PyMem_Free(buf);

		if (rc < 0)
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
		usb_bulk_write(akai_z48, EP_OUT, sysex_command, string_length, USB_TIMEOUT);
		buffer = (unsigned char*)PyMem_Malloc( 4096 * sizeof(unsigned char));
		rc = usb_bulk_read(akai_z48, EP_IN, buffer, 4096, USB_TIMEOUT);  

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

static PyMethodDef Z48SamplerMethods[] = 
{
    {"__init__", Z48Sampler_init, METH_O, "init"},
    {"init_usb", Z48Sampler_init_usb, METH_O, "Initializes USB device and interface."},
    {"close_usb", Z48Sampler_close_usb, METH_O, "Closes USB device and interface."},
    {"_clear", Z48Sampler_clear_remote_buf, METH_O, "Clears unread data on the sampler."},
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

