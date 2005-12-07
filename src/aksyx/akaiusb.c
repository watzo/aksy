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
    #define inline _inline
#endif

/* Checks whether buffer is an ok reply (0x41 0x6b 0x61 0x49) */
inline int
akai_usb_reply_ok(unsigned char* buffer)
{
    if (buffer[0] != 0x41) return 0;
    if (buffer[1] != 0x6b) return 0;
    if (buffer[2] != 0x61) return 0;
    if (buffer[3] != 0x49) return 0;
    return 1;
}

inline int
akai_usb_sysex_reply_ok(unsigned char* sysex_reply)
{
    int userref_length = sysex_reply[3] >> 4;
    int index = userref_length + 4;
    assert(userref_length >=0 && userref_length <= 3);
    return sysex_reply[index] == SYSEX_OK;
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

int _init_akai_usb(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc;

    akai_dev->dev = usb_open(dev);

    if (! akai_dev->dev)
    {
	return AKAI_USB_INIT_ERROR;
    }

    rc = usb_set_configuration(akai_dev->dev, 1);
    if (rc < 0)
    {
	usb_close(akai_dev->dev);
	return AKAI_USB_INIT_ERROR;
    }

    rc = usb_claim_interface(akai_dev->dev, 0);
    if (rc < 0)
    {
	usb_close(akai_dev->dev);
	return AKAI_USB_INIT_ERROR;
    }

    return AKAI_SUCCESS;
}

int _init_z48(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc = _init_akai_usb(akai_dev, dev);
    if (rc) return rc;

    /* setup sequence, snooped from ak.Sys */
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x01", 2, 1000);
    if (rc < 0) return AKAI_USB_INIT_ERROR;

    akai_dev->sysex_id = Z48_ID;
    sysex_commands commands;
    commands.get_multi_handle = Z48_GET_MULTI_HANDLE;
    commands.get_midi_handle = Z48_GET_MIDI_HANDLE;
    commands.get_program_handle = Z48_GET_PROGRAM_HANDLE;
    commands.get_sample_handle = Z48_GET_SAMPLE_HANDLE;
    akai_dev->commands = commands;
    akai_dev->userref = "";
    akai_dev->userref_length = 0;
    return AKAI_SUCCESS;
}

int _init_s56k(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc = _init_akai_usb(akai_dev, dev);
    if (rc) return rc;

    /* setup sequence, snooped from ak.Sys */
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x14", 2, 1000);
    if (rc < 0) return AKAI_USB_INIT_ERROR;
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x04\x03", 2, 1000);
    if (rc < 0) return AKAI_USB_INIT_ERROR;

    akai_dev->sysex_id = S56K_ID;
    sysex_commands commands;
    commands.get_multi_handle = S56K_GET_MULTI_HANDLE;
    commands.get_midi_handle = S56K_GET_MIDI_HANDLE;
    commands.get_program_handle = S56K_GET_PROGRAM_HANDLE;
    commands.get_sample_handle = S56K_GET_SAMPLE_HANDLE;
    akai_dev->commands = commands;
    akai_dev->userref = "\x00\x00";
    akai_dev->userref_length = 2;
    return AKAI_SUCCESS;
}

int _init_mpc4k(akai_usb_device akai_dev, struct usb_device *dev) {
    return _init_z48(akai_dev, dev);
}

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

             switch (usb_product_id) {
		 case Z48_ID:
		     rc = _init_z48(akai_dev, dev);
		     break;
		 case S56K_ID:
		     rc = _init_s56k(akai_dev, dev);
		     break;
		 case MPC4K_ID:
		     rc = _init_mpc4k(akai_dev, dev);
		     break;
		 default:
		     continue;
	     }
	     return rc;
          }
       }
    }

    return AKAI_NO_SAMPLER_FOUND;
}

int akai_usb_device_close(akai_usb_device akai_dev)
{
    int rc = usb_release_interface(akai_dev->dev, 0);
    rc = usb_close(akai_dev->dev)|rc;
    return rc;
}

int akai_usb_device_reset(akai_usb_device akai_dev)
{
   return usb_reset(akai_dev->dev);
}

int akai_usb_device_exec_sysex(akai_usb_device akai_dev,
    unsigned char *sysex, int sysex_length,
    unsigned char *result_buff, int result_buff_length, int timeout)
{
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

    if (rc > 3 && akai_usb_sysex_reply_ok(result_buff))
    {
        return usb_bulk_read(akai_dev->dev, EP_IN, result_buff, result_buff_length, timeout);
    }

    return rc;
}

int akai_usb_device_send_bytes(akai_usb_device akai_dev, unsigned char* bytes,
    int byte_length, int timeout)
{
    return usb_bulk_write(akai_dev->dev, EP_OUT, bytes, byte_length, timeout);
}

int akai_usb_device_recv_bytes(akai_usb_device akai_dev, unsigned char* buff,
    int buff_length, int timeout)
{
    return usb_bulk_read(akai_dev->dev, EP_IN, buff, buff_length, timeout);
}

int akai_usb_device_get_handle_by_name(akai_usb_device akai_dev,
    unsigned char* name, unsigned char* handle, int timeout)
{
    unsigned char *sysex, *data, *cmd_id;
    int name_length = strlen(name);
    int retval;

    if (name_length < 4)
    {
        /* invalid name */
        return AKAI_INVALID_FILENAME;
    }

    if (IS_MULTI_FILE(name))
    {
        cmd_id = akai_dev->commands.get_multi_handle;
    }
    else if (IS_SAMPLE_FILE(name))
    {
        cmd_id = akai_dev->commands.get_sample_handle;
    }
    else if (IS_PROGRAM_FILE(name))
    {
        cmd_id = akai_dev->commands.get_program_handle;
    }
    else if (IS_MIDI_FILE(name))
    {
        cmd_id = akai_dev->commands.get_midi_handle;
    }
    else
    {
        /* invalid name */
        return AKAI_INVALID_FILENAME;
    }

    /* request: \x10\x08\x00\xf0\x47 <sysex_id> <device_id> <userref> <section, command, name, \xf7 */
    int sysex_length = name_length + 7 + akai_dev->userref_length;
    char device_id =  akai_dev->userref_length << 4;
    int index = 0;
    sysex = (unsigned char*) calloc(sysex_length, sizeof(unsigned char));
    memcpy(sysex, "\x10", 1 * sizeof(unsigned char));
    memcpy(sysex+1, &sysex_length, 1 * sizeof(unsigned char));
    memcpy(sysex+2, "\x00\xf0\x47", 3 * sizeof(unsigned char));
    memcpy(sysex+5, &akai_dev->sysex_id, 1 * sizeof(unsigned char));
    memcpy(sysex+6, &device_id, 1 * sizeof(unsigned char));
    memcpy(sysex+7,  &akai_dev->userref, akai_dev->userref_length * sizeof(unsigned char));
    index = 7 + akai_dev->userref_length;
    memcpy(sysex+index, cmd_id, 2 * sizeof(unsigned char));
    index += 2;
    memcpy(sysex+index, name, (name_length - 4) * sizeof(unsigned char)); // strip extension
    index += name_length - 4;
    memcpy(sysex+index, "\x00\xf7", 2 * sizeof(unsigned char));

    /* success reply: \xf0\x47 <device> userref <section, command, <reply_ok> <4 byte handle>, \xf7 */
    /* error reply: \xf0\x47 <device> userref <section, command, <reply_error>, \xf7 */
    if (!usb_bulk_write(akai_dev->dev, EP_OUT, sysex, sysex_length, timeout))
    {
        retval = AKAI_TRANSMISSION_ERROR;
    }
    else
    {
        data = (unsigned char*) calloc(13 + akai_dev->userref_length, sizeof(unsigned char));
        int ret;
read_sysex:
        if ((ret = usb_bulk_read(akai_dev->dev, EP_IN, data, 13 + akai_dev->userref_length, timeout)) < 0)
        {
            retval = AKAI_TRANSMISSION_ERROR;
        }
        else
        {
            if (data[4+akai_dev->userref_length] == SYSEX_ERROR)
            {
                retval = AKAI_FILE_NOT_FOUND;
            }
            else if (data[4+akai_dev->userref_length] == SYSEX_REPLY)
            {
                memcpy(handle, data+8+akai_dev->userref_length, 4*sizeof(unsigned char));

                retval = 0;
            }
            else if (data[4+akai_dev->userref_length] == SYSEX_OK)
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

int _init_get_request(unsigned char *get_request, unsigned char *filename, unsigned char *handle) {
    if (IS_SAMPLE_FILE(filename)) {
	get_request[0] = Z48_MEMORY_GET_SAMPLE;
    }
    else if (IS_PROGRAM_FILE(filename)) {
	get_request[0] = Z48_MEMORY_GET_PROGRAM;
    }
    else if (IS_MULTI_FILE(filename)) {
	get_request[0] = Z48_MEMORY_GET_MULTI;
    }
    else if (IS_MIDI_FILE(filename)) {
	get_request[0] = Z48_MEMORY_GET_MIDI;
    } else {
	return AKAI_INVALID_FILENAME;
    }

    /*
    the handle we retrieved uses 7 bits bytes but the
    transfer request uses 8 bit values so we swap back and forth:
    check this for ppc
    */
    int native_int_handle = ((handle[3] << 21) | (handle[2] << 14) | (handle[1] << 7) | handle[0]);

#if (_BIG_ENDIAN == 1)
    int be_handle = native_int_handle;
#else
    int be_handle = ENDSWAP_INT(native_int_handle);
#endif

    memcpy(get_request+1, &be_handle, 1 * sizeof(int));
    return AKAI_SUCCESS;
}

int akai_usb_device_get(akai_usb_device akai_dev, unsigned char *src_filename,
    unsigned char *dest_filename, int location, int timeout)
{
    unsigned char *get_request, *data, *handle;
    int blocksize = 4096*4, bytes_transferred = 0, actually_transferred = 0, rc = 0;
    int src_filename_length = strlen(src_filename) + 1;
#ifdef _POSIX_SOURCE
    struct timeval t1, t2;
#endif
    FILE *dest_file;

    /* create get request */
    if (location == LOC_MEMORY)
    {
        handle = (unsigned char*) calloc(4, sizeof(unsigned char));
        rc = akai_usb_device_get_handle_by_name(akai_dev, src_filename,
		handle, timeout);

        if (rc)
        {
            free(handle);
            return rc;
        }
        else
        {
            get_request = (unsigned char*) calloc(5, sizeof(unsigned char));
	    rc = _init_get_request(get_request, src_filename, handle);

	    if (rc) {
		free(handle);
		free(get_request);
		return rc;
	    }

            rc = usb_bulk_write(akai_dev->dev, EP_OUT, get_request, 5, timeout);

            if (rc < 0)
            {
                free(get_request);
                return AKAI_TRANSMISSION_ERROR;
            }
        }
    }
    else
    {
        get_request = (unsigned char*) calloc(src_filename_length+1, sizeof(unsigned char));
        get_request[0] = Z48_DISK_GET;
        memcpy(get_request+1, src_filename, src_filename_length * sizeof(unsigned char));
        rc = usb_bulk_write(akai_dev->dev, EP_OUT, get_request, src_filename_length+1, timeout);
        if (rc < 0)
        {
            free(get_request);
            return AKAI_TRANSMISSION_ERROR;
        }
    }

    dest_file = fopen(dest_filename, "w+b");

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
#if (_DEBUG == 1)
            int i;
            printf("Reply block: ");
            for(i=0;i<8;i++)
                printf("%02X ", data[i]);
            printf("\n");
#endif
            actually_transferred = GET_BYTES_TRANSFERRED(data);
            if (actually_transferred == 1)
            {
                rc =  AKAI_FILE_NOT_FOUND;
                break;
            }

#if (_DEBUG == 1)
            printf("Current block size: %i. Bytes read now: %i, Total bytes read: %i. Actually transferred: %i\n",
                blocksize, rc, bytes_transferred, actually_transferred);
#endif

            blocksize = GET_BLOCK_SIZE(data);

            if (blocksize == 0)
            {
                /* file transfer completed */
                rc = 0;
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
#if (_DEBUG == 1)
            printf("At bulk read: Unexpected reply, rc %i or unexpected end of transmission.\n", rc);
#endif
            rc = AKAI_TRANSMISSION_ERROR;
	    break;
        }

    } while(rc > 0);

    fclose(dest_file);
    free(data);

    if (!rc)
    {
#ifdef _POSIX_SOURCE
        print_transfer_stats(t1, t2, bytes_transferred);
#endif
        return AKAI_SUCCESS;
    }
    else
    {
        // remove(dest_filename);
        return rc;
    }
}

/* uploads a file to the sampler. */
int akai_usb_device_put(akai_usb_device akai_dev,
    unsigned char *src_filename, unsigned char *dest_filename, int location, int timeout)
{
    unsigned char *buf, *command, *reply_buf;
    unsigned long int filesize = 0;
    int rc, retval = 0, blocksize = 0, init_blocksize = 4096 * 8, transferred = 0, bytes_read = 0;
    int dest_filename_length = strlen(dest_filename) + 1;
    FILE* fp;

#ifdef _POSIX_SOURCE
    struct stat* st;
    struct timeval t1, t2;
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
    HANDLE tmp_fp =  CreateFile(
        src_filename,
        GENERIC_READ,
        FILE_SHARE_READ,
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        NULL);

    if (tmp_fp == INVALID_HANDLE_VALUE)
    {
        return AKAI_FILE_STAT_ERROR;
    }

    filesize = GetFileSize(tmp_fp, NULL);

    CloseHandle(tmp_fp);

    if (filesize == INVALID_FILE_SIZE)
    {
        return AKAI_FILE_STAT_ERROR;
    }
#endif

    if (filesize == 0)
    {
        return AKAI_EMPTY_FILE_ERROR;
    }

    printf("File name to upload %s, Size of file: %li bytes\n", dest_filename, filesize);
    /* create 'put' command: 0x41, byte size and the name of the file to transfer */
    command = (unsigned char*) calloc(dest_filename_length+6,  sizeof(unsigned char));
    command[0] = (location)?Z48_MEMORY_PUT:Z48_DISK_PUT;
    command[1] = filesize >> 24;
    command[2] = filesize >> 16;
    command[3] = filesize >> 8;
    command[4] = filesize;
    memcpy(command+5, dest_filename, dest_filename_length * sizeof(unsigned char));

    rc = usb_bulk_write(akai_dev->dev, EP_OUT, command, dest_filename_length+6, 1000);

    if (rc < 0)
    {
        return AKAI_TRANSMISSION_ERROR;
    }

    reply_buf = (unsigned char*) calloc(64, sizeof(unsigned char));

#ifdef _POSIX_SOURCE
      gettimeofday(&t1, NULL); // timeval, timezone struct
#endif

    fp = fopen(src_filename, "rb");

    if (!fp)
    {
        return AKAI_FILE_READ_ERROR;;
    }

    buf = calloc(init_blocksize, sizeof(unsigned char));

    do
    {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, reply_buf, 64, 1000);

#if (_DEBUG == 1)
        printf("return code: %i\n", rc);
        int i = 0;
        for (; i < rc; i++)
            printf("%02x ", reply_buf[i]);
        printf("\n");
#endif
        if (rc == 1) {
	    if (filesize == blocksize + transferred) {
		// S56k transfer ends here
		break;
	    } else {
		continue;
	    }
	}

        if (rc == 4 && akai_usb_reply_ok(reply_buf))
        {
            continue;
        }
        else if (rc == 8)
        {

            blocksize = GET_BLOCK_SIZE(reply_buf);
            assert (blocksize <= init_blocksize);
            transferred = GET_BYTES_TRANSFERRED(reply_buf);
#if (_DEBUG == 1)
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
#if (_DEBUG == 1)
        printf("writing %i bytes\n", bytes_read);
#endif
        usb_bulk_write(akai_dev->dev, EP_OUT, buf, bytes_read, 1000);

        /* continue */
        usb_bulk_write(akai_dev->dev, EP_OUT, "\x00", 1, 1000);
    } while(bytes_read > 0 && rc > 0);

    if (ferror(fp))
    {
        retval = AKAI_FILE_READ_ERROR;
    }

    fclose(fp);
    free(reply_buf);
    free(buf);

#ifdef _POSIX_SOURCE
    print_transfer_stats(t1, t2, filesize);
#endif
    return retval;
}


