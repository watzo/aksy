#include <stdio.h>
#include <string.h>
#include <usb.h>
#include <assert.h>
#include <errno.h>
#include "akaiusb.h"

#ifdef _POSIX_SOURCE
    #include <sys/stat.h>
    #include <sys/time.h>
    #include <time.h>
#endif

#ifdef _WIN32
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
#endif 

/* Checks whether buffer is an ok reply (0x41 0x6b 0x61 0x49) */
inline int 
akai_usb_reply_ok(unsigned char* buffer)
{
    printf("Buff contents reply ok\n");
    int i = 0;
    for (; i < 4 ; i++)
		printf("%02x ", buffer[i]);
	printf("\n");

	if (buffer[0] != 0x41) return 0;
	if (buffer[1] != 0x6b) return 0;
	if (buffer[2] != 0x61) return 0;
	if (buffer[3] != 0x49) return 0;
	return 1;
}

inline int
akai_usb_sysex_reply_ok(unsigned char* sysex_reply)
{
	printf("REPLY TYPE for %02x %02x\n", sysex_reply[6], sysex_reply[4]);
    return sysex_reply[4] == SYSEX_OK;
}

inline int
eos(unsigned char* sysex_reply, int sysex_length)
{
    return sysex_reply[sysex_length-1] == 0xf7;
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

int akai_usb_device_init(akai_usb_device akai_dev)
{
    struct usb_bus *bus;
    struct usb_device *dev;
    int usb_product_id;
    int rc;

    usb_init();

    usb_find_busses();
    usb_find_devices();

    for (bus = usb_get_busses(); bus; bus = bus->next)
    {
       for (dev = bus->devices; dev; dev = dev->next)
       {
         if (dev->descriptor.idVendor == VENDOR_ID)
         {
             usb_product_id = dev->descriptor.idProduct;

             if (usb_product_id != Z48 && usb_product_id != S56K)
             {
                return AKAI_UNSUPPORTED_DEVICE;
             }

             /* found the akai z48 or s56k */
             akai_dev->dev = usb_open(dev);
             akai_dev->id = usb_product_id;
             if (! akai_dev->dev)
             {
                return AKAI_USB_INIT_ERROR;
             }

             rc = usb_claim_interface(akai_dev->dev, 0);
             if (rc < 0) 
             {
                 usb_close(akai_dev->dev);
                 return AKAI_USB_INIT_ERROR;
             }

             /* setup sequence, snooped from ak.Sys */
             rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x01", 2, 1000);
             if (rc < 0) return AKAI_TRANSMISSION_ERROR;
			 
             return 0;
          }
       }
    }

    return AKAI_NO_SAMPLER_FOUND;
}
int akai_usb_device_close(akai_usb_device akai_dev)
{
    int rc;
    rc = usb_release_interface(akai_dev->dev, 0);
    rc = usb_close(akai_dev->dev)|rc;
    return rc;
}

int akai_usb_device_reset(akai_usb_device akai_dev)
{
   return usb_reset(akai_dev->dev);
}

int akai_usb_device_exec_sysex(akai_usb_device akai_dev,  
    char *sysex, int sysex_length, 
    char *result_buff, int result_buff_length, int timeout) 
{

	int i = 0;
    for (; i < sysex_length ; i++)
		printf("%02x ", sysex[i]);
	printf("\n");

    int rc = usb_bulk_write(akai_dev->dev, EP_OUT, sysex, sysex_length, timeout);

    if (rc < 0)
    {
        return rc;
    }

    rc = usb_bulk_read(akai_dev->dev, EP_IN, result_buff, result_buff_length, timeout);

    if (rc < 0)
    {
        return rc;
    }
 
    if (akai_usb_sysex_reply_ok(result_buff))
    {
        printf("reply ok!\n");
        return usb_bulk_read(akai_dev->dev, EP_IN, result_buff, result_buff_length, timeout);
    }

    return rc;
}

int akai_usb_device_send_bytes(akai_usb_device akai_dev, char* bytes, 
    int byte_length, int timeout) 
{
    return usb_bulk_write(akai_dev->dev, EP_OUT, bytes, byte_length, timeout);
}

int akai_usb_device_recv_bytes(akai_usb_device akai_dev, char* buff, 
    int buff_length, int timeout)
{
    return usb_bulk_read(akai_dev->dev, EP_IN, buff, buff_length, timeout);
}

int akai_usb_device_get_handle_by_name(akai_usb_device akai_dev,
    char* name, char* handle, char* cmd_id, int timeout)
{
    unsigned char section;
    unsigned char *extension, *sysex, *data;
    int retval;
    int name_length = strlen(name);
    if (name_length < 4)
    {
        /* invalid name */
        return AKAI_INVALID_FILENAME;
    }

    extension = (unsigned char*) calloc(4, sizeof(unsigned char));
    strncpy(extension, name + name_length-3, 4);
    if (strcasecmp(extension, "akm") == 0)
    {
        section = '\x18';
        if (cmd_id) *cmd_id = Z48_MEMORY_GET_MULTI;
    }
    else if (strcasecmp(extension, "wav") == 0)
    {
        section = '\x1c';
        if (cmd_id) *cmd_id = Z48_MEMORY_GET_SAMPLE;
    }
    else if (strcasecmp(extension, "akp") == 0)
    {
        section = '\x14';
        if (cmd_id) *cmd_id = Z48_MEMORY_GET_PROGRAM;
    }
    else if (strcasecmp(extension, "mid") == 0)
    {
        section = '\x28';
        if (cmd_id) *cmd_id = Z48_MEMORY_GET_MIDI;
    }
    else
    {
        /* invalid name */
        return AKAI_INVALID_FILENAME;
    }

    /* request: \x10\x08\x00\xf0\x47 <device> <section, command, name, \xf7 */
    char sysex_length = (unsigned char)name_length+7; // 5 + 
    char sysex_id = akai_dev->id;
    sysex = (unsigned char*) calloc(sysex_length, sizeof(unsigned char));
    memcpy(sysex, "\x10", 5 * sizeof(unsigned char));
    memcpy(sysex+1, &sysex_length, 1 * sizeof(unsigned char));
    memcpy(sysex+2, "\x00\xf0\x47", 5 * sizeof(unsigned char));
    memcpy(sysex+5, &sysex_id, 1 * sizeof(unsigned char));
    memcpy(sysex+6, "\x00", 1 * sizeof(unsigned char));
    memcpy(sysex+7, &section, 1 * sizeof(unsigned char));
    memcpy(sysex+8, "\x08", 1 * sizeof(unsigned char));
    memcpy(sysex+9, name, (name_length -4) * sizeof(unsigned char)); // strip extension
    memcpy(sysex+9 + name_length - 4, "\x00\xf7", 2 * sizeof(unsigned char));

	int i = 0;
    for (; i < sysex_length ; i++)
		printf("%02x ", sysex[i]);
	printf("\n");

    
    /* success reply: \xf0\x47 <device> userref <section, command, <reply_ok> <4 byte handle>, \xf7 */
    /* error reply: \xf0\x47 <device> userref <section, command, <reply_error>, \xf7 */
    if (!usb_bulk_write(akai_dev->dev, EP_OUT, sysex, sysex_length, timeout))
    {
        retval = AKAI_TRANSMISSION_ERROR;
    }
    else
    {
        data = (unsigned char*) calloc(13, sizeof(unsigned char));
        int ret;
read_sysex:
        if ((ret = usb_bulk_read(akai_dev->dev, EP_IN, data, 13, timeout)) < 0)
        {
            retval = AKAI_TRANSMISSION_ERROR;
        }
        else
        {
             int i = 0;
             printf("REPLY\n");
	    	    for (; i < 13 ; i++)
	    	    	printf("%02x ", data[i]);
	    	    printf("\n");
    
            if (data[4] == SYSEX_ERROR)
            {
                retval = AKAI_FILE_NOT_FOUND;
            }
            else if (data[4] == SYSEX_REPLY)
            {
                memcpy(handle, data+8, 4*sizeof(unsigned char));

                retval = 0;
            }
            else if (data[4] == SYSEX_OK)
            {
                goto read_sysex;
            }
            else
            {
                retval = AKAI_SYSEX_UNEXPECTED;
            }
        }

        free(data);
    }

    free(sysex);
    return retval;
}

int akai_usb_device_get(akai_usb_device akai_dev, char *src_filename, 
    char *dest_filename, int location, int timeout)
{
    unsigned char *command, *data, *handle, cmd_id;
	int blocksize = 4096*4, bytes_transferred = 0, actually_transferred = 0, rc = 0, retval = 0;
    int src_filename_length = strlen(src_filename) + 1;
#ifdef _POSIX_SOURCE
	struct timeval t1, t2;
#endif
    FILE *dest_file;

    /* create get request */
    if (location == LOC_MEMORY)
    {
        cmd_id = Z48_MEMORY_GET_SAMPLE;
        handle = (unsigned char*) calloc(4, sizeof(unsigned char));
        rc = akai_usb_device_get_handle_by_name(
            akai_dev, src_filename, handle, &cmd_id, timeout); 

        if (rc)
        {
            free(handle);
            return rc;
        }
        else
        {
            command = (unsigned char*) calloc(5, sizeof(unsigned char));
            command[0] = cmd_id;
            /* 
                the handle we retrieved uses 7 bits bytes but for the
                transfer request uses 8 bit values so we swap back and forth:
                check this for ppc
            */
            int native_int_handle = ((handle[3] << 21) | (handle[2] << 14) | (handle[1] << 7) | handle[0]); 

#if (_BIG_ENDIAN == 1)
            int be_handle = native_int_handle;
#else
            int be_handle = ENDSWAP_INT(native_int_handle);
#endif

            memcpy(command+1, &be_handle, 1 * sizeof(int));

            free(handle);
            retval = usb_bulk_write(akai_dev->dev, EP_OUT, command, 5, timeout);

            if (retval < 0)
            {
                free(command);
                return AKAI_TRANSMISSION_ERROR;
            }
        }
    }
    else
    {
        command = (unsigned char*) calloc(src_filename_length+1, sizeof(unsigned char));
        command[0] = Z48_DISK_GET;
        memcpy(command+1, src_filename, src_filename_length * sizeof(unsigned char));
        retval = usb_bulk_write(akai_dev->dev, EP_OUT, command, src_filename_length+1, timeout);
        if (retval < 0)
        {
            free(command);
            return AKAI_TRANSMISSION_ERROR;
        }
    }

    free(command);

    if (retval < 0)
    {
       return retval;
    }

	dest_file = fopen(dest_filename, "w+"); 

    if (!dest_file)
    {
        return errno;
    }

    data = calloc(blocksize, sizeof(unsigned char));
#ifdef _POSIX_SOURCE
    gettimeofday(&t1, NULL); // timeval, timezone struct
#endif

    int read_transfer_status = 1;
    do
    {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, data, blocksize, timeout);  

        if (rc == blocksize && !read_transfer_status)
        {
            bytes_transferred+= rc;

            fseek(dest_file, actually_transferred, 0);

            /* write to file */
            fwrite(data, sizeof(unsigned char), rc, dest_file);

            /* sent continue request */
            usb_bulk_write(akai_dev->dev, EP_OUT, "\x00", 1, timeout);  
            blocksize = 8;
            read_transfer_status = 1;
            continue;
        }	
        else if (rc == 8)
        {
            /* get the number of bytes to read */
#ifdef _DEBUG
            int i;
            printf("Reply block: ");
            for(i=0;i<8;i++)
                printf("%02X ", data[i]);
            printf("\n");
            actually_transferred = GET_BYTES_TRANSFERRED(data);
            if (actually_transferred == 1) 
            {
                retval =  AKAI_FILE_NOT_FOUND;
                break;
            }
            printf("Current block size: %i. Bytes read now: %i, Total bytes read: %i. Actually transferred: %i\n", 
                blocksize, rc, bytes_transferred, actually_transferred);
#endif
            
            blocksize = GET_BLOCK_SIZE(data);

            if (blocksize == 0)
            {
                /* file transfer completed */
                retval = 0;
                break;
            }

            read_transfer_status = 0;
            continue;
        }
        else if (rc == 4 && akai_usb_reply_ok(data))	
        {
             continue;
        }
        else
        {
            printf("At bulk read: Unexpected reply, rc %i or unexpected end of transmission.\n", rc);
            retval = AKAI_TRANSMISSION_ERROR;
        }

    } while(rc > 0);

    fclose(dest_file);
    free(data);

    if (!retval)
    {
#ifdef _POSIX_SOURCE
        print_transfer_stats(t1, t2, bytes_transferred);
#endif
        return 0;
    }
    else
    {
        // remove(dest_filename);
        return retval;
    }
}

/* uploads a file to the sampler. */
int akai_usb_device_put(akai_usb_device akai_dev, 
    char *src_filename, char *dest_filename, int location, int timeout)
{
	unsigned char *buf, *command, *reply_buf;
    struct stat* st;
	unsigned long filesize = 0;
    int rc, retval = 0, blocksize = 4096 * 4, transferred = 0, bytes_read = 0;
    int dest_filename_length = strlen(dest_filename) + 1; 
	FILE* fp;
			
#ifdef _POSIX_SOURCE
	struct timeval t1, t2;
#endif

#ifdef _POSIX_SOURCE
    /* Get file info */
    st = (struct stat*)malloc(sizeof(struct stat));
    rc = stat(src_filename, st);

    if (rc == -1)
    {
        int err = errno;
        free(st);
        if (err == ENOENT)
            return AKAI_FILE_NOT_FOUND;
        else
            return AKAI_FILE_STAT_ERROR;
    }

    filesize = st->st_size;
    free(st);
#endif
#ifdef _WIN32
    DWORD rc = GetFileSize(fp, &filesize);

    if (rc)
    {
        return AKAI_FILE_STAT_ERROR;
    }
#endif 

    printf("File name to upload %s, Size of file: %i bytes\n", dest_filename, filesize);
    /* create 'put' command: 0x41, byte size and the name of the file to transfer */
    command = (unsigned char*) calloc(dest_filename_length+5,  sizeof(unsigned char));
    command[0] = (location)?Z48_MEMORY_PUT:Z48_DISK_PUT;
    command[1] = filesize >> 24;
    command[2] = filesize >> 16;
    command[3] = filesize >> 8;
    command[4] = filesize;
    memcpy(command+5, dest_filename, dest_filename_length * sizeof(unsigned char));

    rc = usb_bulk_write(akai_dev->dev, EP_OUT, command, dest_filename_length+5, 1000); 

    if (rc < 0)
    {
        return AKAI_TRANSMISSION_ERROR;
    }

    reply_buf = (unsigned char*) calloc(64, sizeof(unsigned char));

#ifdef _POSIX_SOURCE
  	gettimeofday(&t1, NULL); // timeval, timezone struct
#endif

    fp = fopen(src_filename, "r");

    if (!fp)
    {
        return errno; 
    }

    buf = calloc(blocksize, sizeof(unsigned char));

	do 
	{
		rc = usb_bulk_read(akai_dev->dev, EP_IN, reply_buf, 64, 1000); 

#ifdef _DEBUG
        printf("return code: %i\n", rc);
		int i = 0;
		for (; i < rc; i++)
			printf("%02x ", reply_buf[i]);
		printf("\n");
#endif

        if (rc == 1) continue;

		if (rc == 4 && akai_usb_reply_ok(reply_buf))	
		{
			continue;
		}
		else if (rc == 8)
		{

			blocksize = GET_BLOCK_SIZE(reply_buf);	
            transferred = GET_BYTES_TRANSFERRED(reply_buf);
#ifdef _DEBUG
            printf("blocksize: %i\n", blocksize);
            printf("transferred: %i\n", transferred);
#endif
			if (transferred == filesize) 
			{
                // continue reading last reply 
				continue;
			}
		}
		else if (rc == 5)
		{
			break; // finished TODO: check contents of buffer...
		}

        fseek(fp, transferred, 0);
		bytes_read = fread(buf, sizeof(unsigned char), blocksize, fp);
#ifdef _DEBUG
        printf("writing %i bytes\n", bytes_read);
#endif
		usb_bulk_write(akai_dev->dev, EP_OUT, buf, bytes_read, 1000); 

		/* continue */
		usb_bulk_write(akai_dev->dev, EP_OUT, "\x00", 1, 1000); 
	} while(bytes_read > 0 && rc > 0);

    if (!feof(fp))
    {
        retval = AKAI_FILE_READ_ERROR;
    }

	fclose(fp);
	free(reply_buf);
	free(buf);

#ifdef _POSIX_SOURCE
	print_transfer_stats(t1, t2, transferred);
#endif
	return retval;
}


