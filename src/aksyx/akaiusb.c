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
aksyxusb_reply_ok(char* buffer)
{
    if (buffer[0] != 0x41) return 0;
    if (buffer[1] != 0x6b) return 0;
    if (buffer[2] != 0x61) return 0;
    if (buffer[3] != 0x49) return 0;
    return 1;
}

inline int
aksyxusb_sysex_reply_ok(char* sysex_reply)
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
    // get elapsed time in seconds.
    elapsed = (t2.tv_sec - t1.tv_sec) + (t2.tv_usec - t1.tv_usec)/1000000.0f;
    kbps = bytes_transferred/(1024*elapsed);
    printf("Transfered %i bytes in elapsed %6f (%6f kB/s)\n", bytes_transferred, elapsed, kbps);
}
#endif
#ifdef _WIN32
void
print_transfer_stats(long t1, long t2, int bytes_transferred)
{
    float elapsed, kbps;
    // get elapsed time in seconds.
    elapsed = (t2 - t1)/1000.0f;
    kbps = bytes_transferred/(1024*elapsed);
    printf("Transfered %i bytes in elapsed %6f (%6f kB/s)\n", bytes_transferred, elapsed, kbps);
}
#endif

char*
aksyx_get_sysex_error_msg(int code) {
    switch (code) {
	case 0x00: return "The <Section> <Item> supplied are not supported";
	case 0x01: return "Checksum invalid";
	case 0x02: return "Unknown error";
	case 0x03: return "Invalid message format";
	case 0x04: return "Parameter out of range";
	case 0x05: return "Operation is pending";
	case 0x80: return "Unknown system error";
	case 0x81: return "Operation had no effect";
	case 0x82: return "Fatal error";
	case 0x83: return "CPU memory is full";
	case 0x84: return "WAVE memory is full";
	case 0x100: return "Unknown item error";
	case 0x101: return "Item not found";
	case 0x102: return "Item in use";
	case 0x103: return "Invalid item handle";
	case 0x104: return "Invalid item name";
	case 0x105: return "Maximum number of items of a particular type reached";
	case 0x120: return "Keygroup not found";
	case 0x180: return "Unknown disk error";
	case 0x181: return "No Disks";
	case 0x182: return "Disk is invalid";
	case 0x183: return "Load error";
	case 0x184: return "Create error";
	case 0x185: return "Directory not empty";
	case 0x186: return "Delete error";
	case 0x187: return "Disk is write-protected";
	case 0x188: return "Disk is not writable";
	case 0x189: return "Disk full";
	case 0x18A: return "Disk abort";
	case 0x200: return "Unknown file error";
	case 0x201: return "File format is not supported";
	case 0x202: return "WAV format is incorrect";
	case 0x203: return "File not found";
	case 0x204: return "File already exists";
	default: return "Unknown error code";
    }
}

void
log_debug(char* template, ...) {
    va_list ap;
    fprintf(stderr, "DEBUG:%s: ", __FILE__);
    va_start(ap, template);
    vfprintf(stderr, template, ap);
    va_end(ap);
}

void
log_hex(char* buf, int buf_len, char* template, ...) {
    int i;
    va_list ap;
    fprintf(stderr, "DEBUG:%s: ", __FILE__);
    va_start(ap, template);
    vfprintf(stderr, template, ap);
    va_end(ap);
    for(i=0;i<buf_len;i++)
	fprintf(stderr, "%02X ", buf[i]);
    printf("\n");
}
void
log_error(int code, long lineno) {
    fprintf(stderr, "ERROR:%s:%d %i", __FILE__, lineno, code);
}

int _init_akai_usb(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc;

    akai_dev->dev = usb_open(dev);

    if (! akai_dev->dev)
    {
	return AKSY_USB_INIT_ERROR;
    }

    rc = usb_set_configuration(akai_dev->dev, 1);
    if (rc < 0)
    {
	usb_close(akai_dev->dev);
	return AKSY_USB_INIT_ERROR;
    }

    rc = usb_claim_interface(akai_dev->dev, 0);
    if (rc < 0)
    {
	usb_close(akai_dev->dev);
	return AKSY_USB_INIT_ERROR;
    }

    return AKSY_SUCCESS;
}

int _init_z48(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc = _init_akai_usb(akai_dev, dev);
    if (rc) return rc;

    /* setup sequence, snooped from ak.Sys */
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x01", 2, 1000);
    if (rc < 0) return AKSY_USB_INIT_ERROR;

    akai_dev->sysex_id = Z48_ID;
    akai_dev->userref = "";
    akai_dev->userref_length = 0;
    akai_dev->get_handle_by_name = &z48_get_handle_by_name;
    return AKSY_SUCCESS;
}

int _init_s56k(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc = _init_akai_usb(akai_dev, dev);
    if (rc) return rc;

    /* setup sequence, snooped from ak.Sys */
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x14", 2, 1000);
    if (rc < 0) return AKSY_USB_INIT_ERROR;
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x04\x03", 2, 1000);
    if (rc < 0) return AKSY_USB_INIT_ERROR;

    akai_dev->sysex_id = S56K_ID;
    akai_dev->userref = "\x00\x00";
    akai_dev->userref_length = 2;
    akai_dev->get_handle_by_name = &s56k_get_handle_by_name;
    return AKSY_SUCCESS;
}

int _init_mpc4k(akai_usb_device akai_dev, struct usb_device *dev) {
    return _init_z48(akai_dev, dev);
}

int aksyxusb_device_init(const akai_usb_device akai_dev)
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

    return AKSY_NO_SAMPLER_FOUND;
}

int aksyxusb_device_close(const akai_usb_device akai_dev)
{
    int rc = usb_release_interface(akai_dev->dev, 0);
    rc = usb_close(akai_dev->dev)|rc;
    return rc < 0? AKSY_USB_CLOSE_ERROR: AKSY_SUCCESS;
}

int aksyxusb_device_reset(const akai_usb_device akai_dev)
{
   int rc = usb_reset(akai_dev->dev);
   return rc < 0? AKSY_USB_RESET_ERROR: AKSY_SUCCESS;

}

int aksyxusb_device_exec_cmd(const akai_usb_device akai_dev, const char *cmd, const byte_array arg_data,
			     const byte_array response, int* error, const int timeout)
{
    int rc, i, bytes_read = 0;
    struct byte_array sysex;
    struct byte_array resp_buff;
    char device_id =  akai_dev->userref_length << 4;
    resp_buff.length = 9+akai_dev->userref_length+response->length;
    resp_buff.bytes = (char*)calloc(resp_buff.length, sizeof(char));
    sysex.length = 7 + akai_dev->userref_length + arg_data->length;
    sysex.bytes = (char*)calloc(sysex.length, sizeof(char));

    sprintf(sysex.bytes, "\xf0\x47%c%c",akai_dev->sysex_id, device_id);
    memcpy(sysex.bytes+4,  &akai_dev->userref, akai_dev->userref_length);
    i = akai_dev->userref_length+4;
    memcpy(sysex.bytes+i, cmd, 2);
    i += 2;
    memcpy(sysex.bytes+i, arg_data->bytes, arg_data->length);
    i += arg_data->length;
    sprintf(sysex.bytes+i, "\xf7");

    rc = aksyxusb_device_exec_sysex(akai_dev, &sysex, &resp_buff, &bytes_read, timeout);
    free(sysex.bytes);

    if (! rc) {
	switch(resp_buff.bytes[4+akai_dev->userref_length]) {
	    case SYSEX_REPLY:
		memcpy(response->bytes, resp_buff.bytes+7+akai_dev->userref_length, response->length);
		rc = AKSY_SUCCESS;
		break;
	    case SYSEX_ERROR:
		rc = AKSY_SYSEX_ERROR;
		*error = *(resp_buff.bytes+7)<<7|*(resp_buff.bytes+8);
		break;
	    case SYSEX_DONE:
		rc = AKSY_SUCCESS;
		break;
	    default:
		rc = AKSY_SYSEX_UNEXPECTED;
	}
    }
    free(resp_buff.bytes);
    return rc;
}

int aksyxusb_device_exec_sysex(const akai_usb_device akai_dev,
    const byte_array sysex, const byte_array result_buff, int* const bytes_read, const int timeout)
{
    int rc;
    struct byte_array request;
    char byte1 = (char)sysex->length;
    char byte2 = (char)(sysex->length>>8);
    request.length = sysex->length+3;
    request.bytes = (char*) calloc(request.length, sizeof(char));
    sprintf(request.bytes, "%c%c%c", CMD_EXEC_SYSEX, byte1, byte2);
    memcpy(request.bytes+3, sysex->bytes, sysex->length);

#if (AKSY_DEBUG == 1)
    log_hex(request.bytes, request.length, "Request: ");
#endif

    rc = usb_bulk_write(akai_dev->dev, EP_OUT, request.bytes, request.length, timeout);

    free(request.bytes);

    if (rc < 0)
    {
        return AKSY_TRANSMISSION_ERROR;
    }

    rc = usb_bulk_read(akai_dev->dev, EP_IN, result_buff->bytes, result_buff->length, timeout);

    if (rc < 0)
    {
        return AKSY_TRANSMISSION_ERROR;
    }

#if (AKSY_DEBUG == 1)
    log_hex(result_buff->bytes, rc, "Reply 1: ");
#endif

    while (rc == 4 && aksyxusb_reply_ok(result_buff->bytes)) {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, result_buff->bytes, result_buff->length, timeout);
	log_hex(result_buff->bytes, rc, "Reply: ");
    }

    if (rc > 4 && aksyxusb_sysex_reply_ok(result_buff->bytes))
    {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, result_buff->bytes, result_buff->length, timeout);

	if (rc < 0) {
	    return AKSY_TRANSMISSION_ERROR;
	}

#if (AKSY_DEBUG == 1)
	log_hex(result_buff->bytes, rc, "Reply 2: ");
#endif

    }

    *bytes_read = rc;
    return AKSY_SUCCESS;
}

int z48_get_handle_by_name(akai_usb_device akai_dev,
    const char* name, byte_array handle, const int timeout)
{
    char *cmd_id;
    struct byte_array basename, resp_data;
    int retval, bytes_read = 0, error_code = 0;
    basename.length = strlen(name) - 3; // exclude extension, include terminator
    resp_data.length = 5;

    if (basename.length <= 0)
    {
        /* invalid name */
        return AKSY_INVALID_FILENAME;
    }

    if (IS_MULTI_FILE(name))
    {
        cmd_id = Z48_GET_MULTI_HANDLE;
    }
    else if (IS_SAMPLE_FILE(name))
    {
        cmd_id = Z48_GET_SAMPLE_HANDLE;
    }
    else if (IS_PROGRAM_FILE(name))
    {
        cmd_id = Z48_GET_PROGRAM_HANDLE;
    }
    else if (IS_MIDI_FILE(name))
    {
        cmd_id = Z48_GET_MIDI_HANDLE;
    }
    else
    {
        /* invalid name */
        return AKSY_INVALID_FILENAME;
    }

    basename.bytes = (char*)calloc(basename.length, sizeof(char));
    resp_data.bytes = (char*)calloc(resp_data.length, sizeof(char));
    sprintf(basename.bytes, "%.*s", basename.length - 1, name);
    retval = aksyxusb_device_exec_cmd(akai_dev, cmd_id, &basename,
				      &resp_data, &error_code, timeout);

    free(basename.bytes);

    if (retval == AKSY_SYSEX_ERROR && error_code == SERR_FILE_NOT_FOUND)
    {
	retval = AKSY_FILE_NOT_FOUND;
    }
    else if (retval == AKSY_SUCCESS)
    {
	// skip the type byte
	memcpy(handle->bytes, resp_data.bytes+1, handle->length);
	log_hex(handle->bytes, handle->length, "Handle ");
    }
    else {
	retval = AKSY_SYSEX_UNEXPECTED;
    }

    free(resp_data.bytes);
    return retval;
}

int
s56k_get_handle_by_name(akai_usb_device akai_dev,
			const char* name, byte_array sysex_handle, const int timeout)
{
    char *set_curr_item_cmd, *get_curr_index_cmd;
    struct byte_array arg, basename, resp_data;

    int BUF_SIZE = 64;
    int no_items = 0, bytes_read = 0;
    int retval;
    int error_code;
    basename.length = strlen(name) - 3;

    if (basename.length <= 0)
    {
        /* invalid name */
        return AKSY_INVALID_FILENAME;
    }
    if (IS_MULTI_FILE(name))
    {
	set_curr_item_cmd =  S56K_SET_CURR_MULTI_BY_NAME;
        get_curr_index_cmd = S56K_GET_CURR_MULTI_INDEX;
    }
    else if (IS_SAMPLE_FILE(name))
    {
	set_curr_item_cmd = S56K_SET_CURR_SAMPLE_BY_NAME;
        get_curr_index_cmd = S56K_GET_CURR_SAMPLE_INDEX;
    }
    else if (IS_PROGRAM_FILE(name))
    {
	set_curr_item_cmd = S56K_SET_CURR_PROGRAM_BY_NAME;
        get_curr_index_cmd = S56K_GET_CURR_PROGRAM_INDEX;
    }
    else if (IS_MIDI_FILE(name))
    {
	set_curr_item_cmd = S56K_SET_CURR_MIDI_BY_NAME;
        get_curr_index_cmd = S56K_GET_CURR_MIDI_INDEX;
    }
    else
    {
        /* invalid name */
        return AKSY_INVALID_FILETYPE;
    }

    // set the current item
    basename.bytes = malloc(basename.length * sizeof(char));
    sprintf(basename.bytes, "%.*s", basename.length - 1, name);
    resp_data.length = 0;
    resp_data.bytes = NULL;

    retval = aksyxusb_device_exec_cmd(
	akai_dev, set_curr_item_cmd, &basename, &resp_data, &error_code, timeout);

    free(basename.bytes);
    if (retval) {
	return (retval == SYSEX_ERROR)? error_code: retval;
    } else {
	// get index of current item
	arg.bytes = NULL;
	arg.length = 0;
	resp_data.length = 2;
	resp_data.bytes = calloc(resp_data.length, sizeof(char));

	retval = aksyxusb_device_exec_cmd(
	    akai_dev, get_curr_index_cmd, &arg, &resp_data, &error_code, timeout);

	if (retval)
	{
	    free(resp_data.bytes);
	    return (retval == SYSEX_ERROR)? error_code: retval;
	}
    }

    memcpy(sysex_handle->bytes, resp_data.bytes, sysex_handle->length);
    free(resp_data.bytes);
    return AKSY_SUCCESS;
}

int _init_get_request(byte_array get_request, char *filename, byte_array handle) {
    int native_int_handle;
    int be_handle;

    if (IS_SAMPLE_FILE(filename)) {
	get_request->bytes[0] = CMD_MEMORY_GET_SAMPLE;
    }
    else if (IS_PROGRAM_FILE(filename)) {
	get_request->bytes[0] = CMD_MEMORY_GET_PROGRAM;
    }
    else if (IS_MULTI_FILE(filename)) {
	get_request->bytes[0] = CMD_MEMORY_GET_MULTI;
    }
    else if (IS_MIDI_FILE(filename)) {
	get_request->bytes[0] = CMD_MEMORY_GET_MIDI;
    } else {
	return AKSY_INVALID_FILENAME;
    }

    /* convert the handle into an integer value */
    native_int_handle = ((handle->bytes[3] << 21) |
			 (handle->bytes[2] << 14) |
			 (handle->bytes[1] << 7) |
			  handle->bytes[0]);

#if (_BIG_ENDIAN == 1)
    be_handle = native_int_handle;
#else
    be_handle = ENDSWAP_INT(native_int_handle);
#endif

    memcpy(get_request->bytes+1, &be_handle, handle->length);
    return AKSY_SUCCESS;
}

int aksyxusb_device_exec_get_request(akai_usb_device akai_dev, byte_array request,
				  char *dest_filename, const int timeout) {
    char* data;
    int blocksize = 4096*4, bytes_transferred = 0, actually_transferred = 0, rc = 0;
    int read_transfer_status;
#ifdef _POSIX_SOURCE
    struct timeval t1, t2;
#endif
#ifdef _WIN32
    DWORD t1, t2;
#endif

    FILE *dest_file;
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, request->bytes, request->length, timeout);
    if (rc < 0)
    {
	return AKSY_TRANSMISSION_ERROR;
    }

    dest_file = fopen(dest_filename, "w+b");

    if (!dest_file)
    {
	return errno;
    }

    data = calloc(blocksize, sizeof(char));
#ifdef _POSIX_SOURCE
    gettimeofday(&t1, NULL);
#endif
#ifdef _WIN32
    t1 = GetTickCount();
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
	    log_hex(data, 8, "Reply block: ");
#endif
	    actually_transferred = GET_BYTES_TRANSFERRED(data);
	    if (actually_transferred == 1)
	    {
		rc =  AKSY_FILE_NOT_FOUND;
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
		rc = AKSY_SUCCESS;
		break;
	    }

	    read_transfer_status = 0;
	    continue;
	}
	else if (rc == 4 && aksyxusb_reply_ok(data))
	{
	    continue;
	}
	else
	{
#if (AKSY_DEBUG == 1)
	    printf("At bulk read: Unexpected reply, rc %i or unexpected end of transmission.\n", rc);
#endif
	    rc = AKSY_TRANSMISSION_ERROR;
	    break;
	}

    } while(rc > 0);

#ifdef _POSIX_SOURCE
    gettimeofday(&t2, NULL);
#endif
#ifdef _WIN32
    t2 = GetTickCount();
#endif
    fclose(dest_file);
    free(data);

    if (!rc)
    {
	print_transfer_stats(t1, t2, bytes_transferred);
	return AKSY_SUCCESS;
    }
    else
    {
	// remove(dest_filename);
	return rc;
    }
}

int aksyxusb_device_get(const akai_usb_device akai_dev, char *src_filename,
    char *dest_filename, const int location, const int timeout)
{
    int rc = 0, src_filename_length = strlen(src_filename) + 1;
    struct byte_array get_request, handle;
    get_request.length=5, handle.length=4;

    /* create get request */
    if (location == LOC_MEMORY)
    {
        handle.bytes = (char*) calloc(handle.length, sizeof(char));
        rc = akai_dev->get_handle_by_name(akai_dev, src_filename, &handle, timeout);

        if (rc)
        {
            free(handle.bytes);
            return rc;
        }
        else
        {
	    get_request.bytes = (char*) calloc(get_request.length, sizeof(char));
	    rc = _init_get_request(&get_request, src_filename, &handle);
	    free(handle.bytes);

	    if (rc) {
		free(get_request.bytes);
		return rc;
	    }
	    log_hex(get_request.bytes, get_request.length, "Request cmd ");
	    rc = aksyxusb_device_exec_get_request(akai_dev, &get_request, dest_filename, timeout);
	    free(get_request.bytes);
            return rc;
        }
    }
    else
    {
	get_request.length = src_filename_length+1;
	get_request.bytes = (char*) malloc(get_request.length * sizeof(char));
	get_request.bytes[0] = CMD_DISK_GET;
	memcpy(get_request.bytes+1, src_filename, src_filename_length * sizeof(char));
	log_hex(get_request.bytes, get_request.length, "Request cmd ");
	rc = aksyxusb_device_exec_get_request(akai_dev, &get_request, dest_filename, timeout);
	free(get_request.bytes);
	return rc;
    }
}

/* uploads a file to the sampler. */
int aksyxusb_device_put(const akai_usb_device akai_dev,
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
        return (err == ENOENT)? AKSY_FILE_NOT_FOUND : AKSY_FILE_STAT_ERROR;
    }

    filesize = st->st_size;
    free(st);
#endif
#ifdef _WIN32
    DWORD t1, t2;
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
        return AKSY_FILE_STAT_ERROR;
    }

    filesize = GetFileSize(tmp_fp, NULL);

    CloseHandle(tmp_fp);

    if (filesize == INVALID_FILE_SIZE)
    {
        return AKSY_FILE_STAT_ERROR;
    }
#endif

    if (filesize == 0)
    {
        return AKSY_EMPTY_FILE_ERROR;
    }

    printf("File name to upload %s, Size of file: %li bytes\n", dest_filename, filesize);

    // TODO: fix ppc
    command = (char*) calloc(dest_filename_length+6,  sizeof(char));
    command[0] = (location)?CMD_MEMORY_PUT:CMD_DISK_PUT;
    command[1] = (char)(filesize >> 24);
    command[2] = (char)(filesize >> 16);
    command[3] = (char)(filesize >> 8);
    command[4] = (char)filesize;
    memcpy(command+5, dest_filename, dest_filename_length * sizeof(char));

    rc = usb_bulk_write(akai_dev->dev, EP_OUT, command, dest_filename_length+6, 1000);

    if (rc < 0)
    {
        return AKSY_TRANSMISSION_ERROR;
    }

    reply_buf = (char*) calloc(64, sizeof(char));

#ifdef _POSIX_SOURCE
    gettimeofday(&t1, NULL);
#endif
#ifdef _WIN32
    t1 = GetTickCount();
#endif

    fp = fopen(src_filename, "rb");

    if (!fp)
    {
        return AKSY_FILE_READ_ERROR;;
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

        if (rc == 4 && aksyxusb_reply_ok(reply_buf))
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

#ifdef _POSIX_SOURCE
    gettimeofday(&t2, NULL);
#endif
#ifdef _WIN32
    t2 = GetTickCount();
#endif

    if (ferror(fp))
    {
        retval = AKSY_FILE_READ_ERROR;
    }

    fclose(fp);
    free(reply_buf);
    free(buf);

    print_transfer_stats(t1, t2, filesize);
    return retval;
}


