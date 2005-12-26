#include <stdio.h>
#include <string.h>
#include <usb.h>
#include <assert.h>
#include <errno.h>
#include "akaiusb.h"
#include <stdarg.h>

#ifdef _POSIX_SOURCE
    #include <sys/stat.h>
    #include <sys/time.h>
    #include <time.h>
#endif

#ifdef _WIN32
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
    #define inline _inline
    #define strcasecmp stricmp
#endif

/* Checks whether buffer is an ok reply (0x41 0x6b 0x61 0x49) */
inline int
akai_usb_reply_ok(char* buffer)
{
    if (buffer[0] != 0x41) return 0;
    if (buffer[1] != 0x6b) return 0;
    if (buffer[2] != 0x61) return 0;
    if (buffer[3] != 0x49) return 0;
    return 1;
}

inline int
akai_usb_sysex_reply_ok(char* sysex_reply)
{
    int userref_length = sysex_reply[3] >> 4;
    int index = userref_length + 4;
    assert(userref_length >=0 && userref_length <= 3);
    return sysex_reply[index] == SYSEX_OK;
}

// WIN32 : long now = timeGetTime();
// DWORD GetTickCount()
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

void
log_debug(char* template, ...) {
    va_list ap;
    fprintf(stderr, "DEBUG: akaiusb: ");
    va_start(ap, template);
    vfprintf(stderr, template, ap);
    va_end(ap);
}

void
log_hex(char* buf, int buf_len, char* template, ...) {
    int i;
    va_list ap;
    va_start(ap, template);
    vfprintf(stderr, template, ap);
    va_end(ap);
    for(i=0;i<buf_len;i++)
	fprintf(stderr, "%02X ", buf[i]);
    printf("\n");
}

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
    sysex_commands commands;
    int rc = _init_akai_usb(akai_dev, dev);
    if (rc) return rc;

    /* setup sequence, snooped from ak.Sys */
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x01", 2, 1000);
    if (rc < 0) return AKAI_USB_INIT_ERROR;

    akai_dev->sysex_id = Z48_ID;
    commands.get_multi_handle = Z48_GET_MULTI_HANDLE;
    commands.get_midi_handle = Z48_GET_MIDI_HANDLE;
    commands.get_program_handle = Z48_GET_PROGRAM_HANDLE;
    commands.get_sample_handle = Z48_GET_SAMPLE_HANDLE;
    akai_dev->commands = commands;
    akai_dev->userref = "";
    akai_dev->userref_length = 0;
    akai_dev->get_handle_by_name = &z48_get_handle_by_name;
    return AKAI_SUCCESS;
}

int _init_s56k(akai_usb_device akai_dev, struct usb_device *dev) {
    sysex_commands commands;
    int rc = _init_akai_usb(akai_dev, dev);
    if (rc) return rc;

    /* setup sequence, snooped from ak.Sys */
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x14", 2, 1000);
    if (rc < 0) return AKAI_USB_INIT_ERROR;
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x04\x03", 2, 1000);
    if (rc < 0) return AKAI_USB_INIT_ERROR;

    akai_dev->sysex_id = S56K_ID;
    commands.get_multi_handle = S56K_GET_MULTI_HANDLE;
    commands.get_midi_handle = S56K_GET_MIDI_HANDLE;
    commands.get_program_handle = S56K_GET_PROGRAM_HANDLE;
    commands.get_sample_handle = S56K_GET_SAMPLE_HANDLE;
    akai_dev->commands = commands;
    akai_dev->userref = "\x00\x00";
    akai_dev->userref_length = 2;
    akai_dev->get_handle_by_name = &s56k_get_handle_by_name;
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
	     if (akai_dev->usb_product_id &&
		 akai_dev->usb_product_id != usb_product_id)
	     {
		 continue;
	     }
             switch (usb_product_id)
	     {
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
    return rc < 0? AKAI_USB_CLOSE_ERROR: AKAI_SUCCESS;
}

int akai_usb_device_reset(akai_usb_device akai_dev)
{
   int rc = usb_reset(akai_dev->dev);
   return rc < 0? AKAI_USB_RESET_ERROR: AKAI_SUCCESS;

}

int akai_usb_device_exec_cmd(akai_usb_device akai_dev, char *cmd, char *data,
			     int data_length, char *result_buff, int result_buff_length, int* bytes_read, int timeout)
{
    int rc, i;
    int sysex_length = 8 + akai_dev->userref_length + data_length;
    char* sysex = (char*)calloc(sysex_length, sizeof(char));
    char device_id =  akai_dev->userref_length << 4;
    sprintf(sysex, "\xf0\x47%c%c",akai_dev->sysex_id, device_id);
    memcpy(sysex+5,  &akai_dev->userref, akai_dev->userref_length);
    i = akai_dev->userref_length+5;
    memcpy(sysex+i, cmd, 2);
    i += 2;
    memcpy(sysex+i, data, data_length);
    i += data_length;
    sprintf(sysex+i, "\xf7");

    rc = akai_usb_device_exec_sysex(akai_dev, sysex, sysex_length, result_buff,
				    result_buff_length, bytes_read, timeout);
    free(sysex);
    return rc;
}

int akai_usb_device_exec_sysex(const akai_usb_device akai_dev,
    const char *sysex, const int sysex_length,
    char *result_buff, int result_buff_length, int* bytes_read, const int timeout)
{
    int rc;
    int request_length = sysex_length+3;
    char* request = (char*) calloc(request_length, sizeof(char));
    char byte1 = (char)sysex_length;
    char byte2 = (char)(sysex_length>>8);
    sprintf(request, "%c%c%c", CMD_EXEC_SYSEX, byte1, byte2);
    memcpy(request+3, sysex, sysex_length);

#if (AKSY_DEBUG == 1)
    log_hex(request, request_length, "Request: ");
#endif

    rc = usb_bulk_write(akai_dev->dev, EP_OUT, request, sysex_length+3, timeout);

    free(request);

    if (rc < 0)
    {
        return AKAI_TRANSMISSION_ERROR;
    }

    rc = usb_bulk_read(akai_dev->dev, EP_IN, result_buff, result_buff_length, timeout);

    if (rc < 0)
    {
        return AKAI_TRANSMISSION_ERROR;
    }

#if (AKSY_DEBUG == 1)
    log_hex(result_buff, rc, "Reply 1: ");
#endif

    while (rc == 4 && akai_usb_reply_ok(result_buff)) {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, result_buff, result_buff_length, timeout);
	log_hex(result_buff, rc, "Reply: ");
    }

    if (rc > 4 && akai_usb_sysex_reply_ok(result_buff))
    {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, result_buff, result_buff_length, timeout);

	if (rc < 0) {
	    return AKAI_TRANSMISSION_ERROR;
	}

#if (AKSY_DEBUG == 1)
	log_hex(result_buff, rc, "Reply 2: ");
#endif

    }

    *bytes_read = rc;
    return AKAI_SUCCESS;
}

int z48_get_handle_by_name(akai_usb_device akai_dev,
    char* name, char* handle, int timeout)
{
    char *data, *cmd_id, *basename;
    int basename_length = strlen(name) - 4;
    int bytes_read = 0;
    int retval;

    if (basename_length <= 0)
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
    basename = calloc(basename_length, sizeof(char));
    sprintf(basename, "%.*s", basename_length, name);
    data = (char*) calloc(13 + akai_dev->userref_length, sizeof(char));
    retval = akai_usb_device_exec_cmd(akai_dev, cmd_id,
				      basename, basename_length + 1, // include terminator
				      data, 13 + akai_dev->userref_length, &bytes_read, timeout);

    if (retval)
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
	    memcpy(handle, data+8+akai_dev->userref_length, 4*sizeof(char));

	    retval = 0;
	}
	else
	{
	    retval = AKAI_SYSEX_UNEXPECTED;
	}
    }

    free(data);
    return retval;
}

int s56k_get_handle_by_name(akai_usb_device akai_dev,
			    char* name, char* sysex_handle, int timeout)
{
    char *data, *get_no_items_cmd, *get_name_cmd_id, *item_name;
    int BUF_SIZE = 64;
    int name_length = strlen(name);
    int no_items = 0;
    int bytes_read = 0;
    int retval, offset;
    int i, handle;

    if (name_length < 4)
    {
        /* invalid name */
        return AKAI_INVALID_FILENAME;
    }
    /* commands to get the name of the file by index */
    if (IS_MULTI_FILE(name))
    {
	get_no_items_cmd = "\x0c\x40";
        get_name_cmd_id = akai_dev->commands.get_multi_handle;
    }
    else if (IS_SAMPLE_FILE(name))
    {
	get_no_items_cmd = "\x0e\x10";
        get_name_cmd_id = akai_dev->commands.get_sample_handle;
    }
    else if (IS_PROGRAM_FILE(name))
    {
	get_no_items_cmd = "\x0a\x10";
        get_name_cmd_id = akai_dev->commands.get_program_handle;
    }
    else if (IS_MIDI_FILE(name))
    {
	get_no_items_cmd = "\x16\x10";
        get_name_cmd_id = akai_dev->commands.get_midi_handle;
    }
    else
    {
        /* invalid name */
        return AKAI_INVALID_FILENAME;
    }

    // get the number of items in memory
    data = (char*) calloc(BUF_SIZE , sizeof(char));

    retval = akai_usb_device_exec_cmd(
	akai_dev, get_no_items_cmd, NULL, 0, data, BUF_SIZE , &bytes_read, timeout);

    if (retval) {
	return retval;
    }

    memcpy(&no_items, data+8+akai_dev->userref_length, 2*sizeof(char));

    for (i=0;i < no_items; i++) {
#if (_BIG_ENDIAN == 1)
	handle = ENDSWAP_INT(i);
#else
	handle = i;
#endif
	sysex_handle[0] = (char)(i>>8);
	sysex_handle[1] = (char)i;
	retval = akai_usb_device_exec_cmd(
	    akai_dev, get_name_cmd_id, sysex_handle, 2, data, BUF_SIZE, &bytes_read, timeout);

	if (retval) {
	    return retval;
	}
	else
	{
	    if (data[4+akai_dev->userref_length] == SYSEX_ERROR)
	    {
		retval = AKAI_FILE_NOT_FOUND;
	    }
	    else if (data[4+akai_dev->userref_length] == SYSEX_REPLY)
	    {
		offset = 8+akai_dev->userref_length;
		int item_name_length = bytes_read-offset+6+akai_dev->userref_length;
		item_name = (char*)calloc(item_name_length, sizeof(char));
		memcpy(item_name, data+8+akai_dev->userref_length, item_name_length);
		if (strcasecmp(name, item_name) == 0) {
		    retval = AKAI_SUCCESS;
		    break;
		}
		free(item_name);
	    }
	    else
	    {
		retval = AKAI_SYSEX_UNEXPECTED;
		break;
	    }
	}
    }

    free(data);
    return retval;
}

int _init_get_request(char *get_request, char *filename, char *handle) {
    int native_int_handle;
    int be_handle;

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
    transfer request uses 8 bit values so we swap back and forth
    */
    native_int_handle = ((handle[3] << 21) | (handle[2] << 14) | (handle[1] << 7) | handle[0]);

#if (_BIG_ENDIAN == 1)
    be_handle = native_int_handle;
#else
    be_handle = ENDSWAP_INT(native_int_handle);
#endif

    memcpy(get_request+1, &be_handle, 1 * sizeof(int));
    return AKAI_SUCCESS;
}

int akai_usb_device_exec_get_request(akai_usb_device akai_dev, char* request, int request_length,
				  char *dest_filename, int timeout) {
    char* data;
    int blocksize = 4096*4, bytes_transferred = 0, actually_transferred = 0, rc = 0;
    int read_transfer_status;
#ifdef _POSIX_SOURCE
    struct timeval t1, t2;
#endif
    FILE *dest_file;
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, request, request_length, timeout);
    if (rc < 0)
    {
	return AKAI_TRANSMISSION_ERROR;
    }

    dest_file = fopen(dest_filename, "w+b");

    if (!dest_file)
    {
	return errno;
    }

    data = calloc(blocksize, sizeof(char));
#ifdef _POSIX_SOURCE
    gettimeofday(&t1, NULL); // timeval, timezone struct
#endif

    read_transfer_status = 1;
    do
    {
	rc = usb_bulk_read(akai_dev->dev, EP_IN, data, blocksize, timeout);

	if (rc == blocksize && !read_transfer_status)
	{
	    bytes_transferred+= rc;

	    fseek(dest_file, actually_transferred, 0);

	    /* write to file */
	    fwrite(data, sizeof(char), rc, dest_file);

	    /* sent continue request */
	    usb_bulk_write(akai_dev->dev, EP_OUT, "\x00", 1, timeout);
	    blocksize = 8;
	    read_transfer_status = 1;
	    continue;
	}
	else if (rc == 8)
	{
	    /* get the number of bytes to read */
#if (AKSY_DEBUG == 1)
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

#if (AKSY_DEBUG == 1)
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
#if (AKSY_DEBUG == 1)
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

int akai_usb_device_get(akai_usb_device akai_dev, char *src_filename,
    char *dest_filename, int location, int timeout)
{
    int rc = 0, src_filename_length = strlen(src_filename) + 1;
    char *get_request, *handle;

    /* create get request */
    if (location == LOC_MEMORY)
    {
        handle = (char*) calloc(4, sizeof(char));
        rc = akai_dev->get_handle_by_name(akai_dev, src_filename, handle, timeout);

        if (rc)
        {
            free(handle);
            return rc;
        }
        else
        {
            get_request = (char*) calloc(5, sizeof(char));
	    rc = _init_get_request(get_request, src_filename, handle);
	    free(handle);

	    if (rc) {
		free(get_request);
		return rc;
	    }

	    rc = akai_usb_device_exec_get_request(akai_dev, get_request, 5, dest_filename, timeout);
	    free(get_request);
            return rc;
        }
    }
    else
    {
	get_request = (char*) calloc(src_filename_length+1, sizeof(char));
	get_request[0] = Z48_DISK_GET;
	memcpy(get_request+1, src_filename, src_filename_length * sizeof(char));

	rc = akai_usb_device_exec_get_request(akai_dev, get_request, src_filename_length+1, dest_filename, timeout);
	free(get_request);
	return rc;
    }
}

/* uploads a file to the sampler. */
int akai_usb_device_put(akai_usb_device akai_dev,
    char *src_filename, char *dest_filename, int location, int timeout)
{
    char *buf, *command, *reply_buf;
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

    // TODO: fix ppc
    command = (char*) calloc(dest_filename_length+6,  sizeof(char));
    command[0] = (location)?Z48_MEMORY_PUT:Z48_DISK_PUT;
    command[1] = (char)(filesize >> 24);
    command[2] = (char)(filesize >> 16);
    command[3] = (char)(filesize >> 8);
    command[4] = (char)filesize;
    memcpy(command+5, dest_filename, dest_filename_length * sizeof(char));

    rc = usb_bulk_write(akai_dev->dev, EP_OUT, command, dest_filename_length+6, 1000);

    if (rc < 0)
    {
        return AKAI_TRANSMISSION_ERROR;
    }

    reply_buf = (char*) calloc(64, sizeof(char));

#ifdef _POSIX_SOURCE
      gettimeofday(&t1, NULL); // timeval, timezone struct
#endif

    fp = fopen(src_filename, "rb");

    if (!fp)
    {
        return AKAI_FILE_READ_ERROR;;
    }

    buf = calloc(init_blocksize, sizeof(char));

    do
    {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, reply_buf, 64, 1000);

#if (AKSY_DEBUG == 1)
        log_hex(reply_buf, rc, "return code: %i\n", rc);
#endif
        if (rc == 1) {
	    if (akai_dev->sysex_id == S56K_ID) {
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
#if (AKSY_DEBUG == 1)
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
        bytes_read = fread(buf, sizeof(char), blocksize, fp);
#if (AKSY_DEBUG == 1)
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


