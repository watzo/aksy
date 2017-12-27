#include <stdio.h>
#include <string.h>
#include <usb.h>
#include <assert.h>
#include <errno.h>
#include "aksyxusb.h"
#include <stdarg.h>

/* work around the issue that _POSIX_SOURCE is not defined in python builds on Tiger */  
#if defined(_POSIX_SOURCE) || defined(MACOSX)
#include <sys/stat.h>
#include <sys/time.h>
#include <time.h>
#endif

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#define strcasecmp stricmp
#endif
#ifdef __MSC_VER
#define inline _inline
#endif

static inline int is_sysex_reply_ok(char* sysex_reply, int sysex_reply_length) {
    if (sysex_reply[0] != (char)SYSEX_START) {
        return 0;
    }

    int userref_length = (sysex_reply[3] >> 4);
    int index = userref_length + 4;
    if (sysex_reply_length < index) {
        return 0;
    }
    assert(userref_length >=0&& userref_length <= 3);
    return sysex_reply[index] == SYSEX_OK;
}

static void print_transfer_stats(long timedelta, long filesize) {
    float elapsed, kbps;
    // get elapsed time in seconds.
    elapsed = timedelta/1000.0f;
    kbps = filesize/(1024*elapsed);
    printf("Transfered %li bytes in elapsed %6f (%6f kB/s)\n", filesize,
            elapsed, kbps);
}

static void log_debug(char* template, ...) {
#if (AKSY_DEBUG == 1)
    va_list ap;
    fprintf(stderr, "DEBUG:%s: ", __FILE__);
    va_start(ap, template);
    vfprintf(stderr, template, ap);
    va_end(ap);
#endif
}

static void log_hex(char* buf, int buf_len, char* template, ...) {
#if (AKSY_DEBUG == 1)
    int i;
    va_list ap;
    fprintf(stderr, "DEBUG:%s: ", __FILE__);
    va_start(ap, template);
    vfprintf(stderr, template, ap);
    va_end(ap);

    for (i = 0; i < buf_len; i++) {
        fprintf(stderr, "%02X ", buf[i]);
    }
    fprintf(stderr, "\n");
#endif
}

static void log_error(int code, long lineno) {
    fprintf(stderr, "ERROR:%s:%li %i",__FILE__ , lineno, code);
}

static int init_akai_usb(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc;

    akai_dev->dev = usb_open(dev);

    if (!akai_dev->dev) {
        return AKSY_USB_INIT_ERROR;
    }

    rc = usb_set_configuration(akai_dev->dev, 1);
    if (rc < 0) {
        usb_close(akai_dev->dev);
        return AKSY_USB_INIT_ERROR;
    }

    rc = usb_claim_interface(akai_dev->dev, 0);
    if (rc < 0) {
        usb_close(akai_dev->dev);
        return AKSY_USB_INIT_ERROR;
    }

    return AKSY_SUCCESS;
}

static int init_z48(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc = init_akai_usb(akai_dev, dev);
    if (rc)
        return rc;

    /* setup sequence, snooped from ak.Sys */
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x01", 2, 1000);
    if (rc < 0) {
        return AKSY_USB_INIT_ERROR;
    }

    akai_dev->sysex_id = Z48_ID;
    akai_dev->userref = "";
    akai_dev->userref_length = 0;
    akai_dev->get_program_cmd_id = Z48_CMD_MEMORY_GET_PROGRAM;
    akai_dev->get_multi_cmd_id = Z48_CMD_MEMORY_GET_MULTI;
    akai_dev->get_handle_by_name = &z48_get_handle_by_name;
    akai_dev->get_sysex_error_msg = &z48_get_sysex_error_msg;
    return AKSY_SUCCESS;
}

static int init_s56k(akai_usb_device akai_dev, struct usb_device *dev) {
    int rc = init_akai_usb(akai_dev, dev);
    if (rc) {
        return rc;
    }

    /* setup sequence, snooped from ak.Sys */
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x03\x14", 2, 1000);
    if (rc < 0) {
        return AKSY_USB_INIT_ERROR;
    }
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, "\x04\x03", 2, 1000);
    if (rc < 0) {
        return AKSY_USB_INIT_ERROR;
    }

    akai_dev->sysex_id = S56K_ID;
    akai_dev->userref = "\x00\x00";
    akai_dev->userref_length = 2;
    akai_dev->get_program_cmd_id = S56K_CMD_MEMORY_GET_PROGRAM;
    akai_dev->get_multi_cmd_id = S56K_CMD_MEMORY_GET_MULTI;
    akai_dev->get_handle_by_name = &s56k_get_handle_by_name;
    akai_dev->get_sysex_error_msg = &s56k_get_sysex_error_msg;
    return AKSY_SUCCESS;
}

static int init_mpc4k(akai_usb_device akai_dev, struct usb_device *dev) {
    return init_z48(akai_dev, dev);
}

int aksyxusb_device_init(const akai_usb_device akai_dev) {
    struct usb_bus *bus;
    struct usb_device *dev;
    int usb_product_id;
    int rc;

    usb_init();

    usb_find_busses();
    usb_find_devices();

    for (bus = usb_get_busses(); bus; bus = bus->next) {
        for (dev = bus->devices; dev; dev = dev->next) {
            if (dev->descriptor.idVendor == VENDOR_ID) {
                usb_product_id = dev->descriptor.idProduct;
                if (akai_dev->usb_product_id &&akai_dev->usb_product_id
                        != usb_product_id) {
                    continue;
                }
                switch (usb_product_id) {
                case Z48_ID:
                    rc = init_z48(akai_dev, dev);
                    break;
                case S56K_ID:
                    rc = init_s56k(akai_dev, dev);
                    break;
                case MPC4K_ID:
                    rc = init_mpc4k(akai_dev, dev);
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

int aksyxusb_device_close(const akai_usb_device akai_dev) {
    int rc = usb_release_interface(akai_dev->dev, 0);
    rc = usb_close(akai_dev->dev)|rc;
    return rc < 0 ? AKSY_USB_CLOSE_ERROR : AKSY_SUCCESS;
}

int aksyxusb_device_reset(const akai_usb_device akai_dev) {
    int rc = usb_reset(akai_dev->dev);
    return rc < 0 ? AKSY_USB_RESET_ERROR : AKSY_SUCCESS;
}

int aksyxusb_device_exec_cmd(const akai_usb_device akai_dev, const char *cmd,
        const byte_array arg_data, const byte_array response, int* sysex_error,
        const int timeout) {
    int rc, i, bytes_read = 0;
    struct byte_array sysex;
    struct byte_array resp_buff;
    resp_buff.length = 9+akai_dev->userref_length+response->length;
    resp_buff.bytes = (char*)malloc(resp_buff.length);
    sysex.length = 7 + akai_dev->userref_length+ arg_data->length;
    sysex.bytes = (char*)malloc(sysex.length);

    memset(sysex.bytes, SYSEX_START, 1);
    memset(sysex.bytes+1, SYSEX_AKAI_ID, 1);
    memcpy(sysex.bytes+2, &akai_dev->sysex_id, 1);
    memset(sysex.bytes+3, akai_dev->userref_length << 4, 1);
    memcpy(sysex.bytes+4, akai_dev->userref, akai_dev->userref_length);
    i = akai_dev->userref_length+4;
    memcpy(sysex.bytes+i, cmd, 2);
    i += 2;
    memcpy(sysex.bytes+i, arg_data->bytes, arg_data->length);
    i += arg_data->length;
    memset(sysex.bytes+i, SYSEX_END, 1);

    rc = aksyxusb_device_exec_sysex(akai_dev, &sysex, &resp_buff, &bytes_read,
            timeout);
    free(sysex.bytes);

    if (!rc) {
        switch (resp_buff.bytes[4+akai_dev->userref_length]) {
        case SYSEX_REPLY:
            memcpy(response->bytes, resp_buff.bytes+7+akai_dev->userref_length,
                    response->length);
            rc = AKSY_SUCCESS;
            break;
        case SYSEX_ERROR:
            rc = AKSY_SYSEX_ERROR;
            *sysex_error = *(resp_buff.bytes+8)<<7|*(resp_buff.bytes+7);
            break;
        case SYSEX_DONE:
            rc = AKSY_SUCCESS;
            break;
        default:
            log_error(AKSY_SYSEX_UNEXPECTED, __LINE__);
            rc = AKSY_SYSEX_UNEXPECTED;
        }
    }
    free(resp_buff.bytes);
    return rc;
}

char* z48_get_sysex_error_msg(int code) {
    switch (code) {
    case 0x00:
        return "The <Section> <Item> supplied are not supported";
    case 0x01:
        return "Checksum invalid";
    case 0x02:
        return "Unknown error";
    case 0x03:
        return "Invalid message format";
    case 0x04:
        return "Parameter out of range";
    case 0x05:
        return "Operation is pending";
    case 0x80:
        return "Unknown system error";
    case 0x81:
        return "Operation had no effect";
    case 0x82:
        return "Fatal error";
    case 0x83:
        return "CPU memory is full";
    case 0x84:
        return "WAVE memory is full";
    case 0x100:
        return "Unknown item error";
    case 0x101:
        return "Item not found";
    case 0x102:
        return "Item in use";
    case 0x103:
        return "Invalid item handle";
    case 0x104:
        return "Invalid item name";
    case 0x105:
        return "Maximum number of items of a particular type reached";
    case 0x120:
        return "Keygroup not found";
    case 0x180:
        return "Unknown disk error";
    case 0x181:
        return "No Disks";
    case 0x182:
        return "Disk is invalid";
    case 0x183:
        return "Load error";
    case 0x184:
        return "Create error";
    case 0x185:
        return "Directory not empty";
    case 0x186:
        return "Delete error";
    case 0x187:
        return "Disk is write-protected";
    case 0x188:
        return "Disk is not writable";
    case 0x189:
        return "Disk full";
    case 0x18A:
        return "Disk abort";
    case 0x200:
        return "Unknown file error";
    case 0x201:
        return "File format is not supported";
    case 0x202:
        return "WAV format is incorrect";
    case 0x203:
        return "File not found";
    case 0x204:
        return "File already exists";
    default:
        return "Unknown error code";
    }
}

char* s56k_get_sysex_error_msg(int code) {
    switch (code) {
    case 0x00:
        return "The <Section> <Item> supplied are not supported";
    case 0x01:
        return "Invalid Message Format — insufficient data supplied";
    case 0x02:
        return "Parameter out of Range";
    case 0x03:
        return "Unknown Error — could not complete command for some reason";
    case 0x04:
        return "Requested program/multi/sample/etc., could not be found";
    case 0x05:
        return "new element could not be created";
    case 0x06:
        return "Deletion of requested item could not be completed";
    case 0x81:
        return "Checksum Invalid";
    case 0x101:
        return "Disk Error — Selected Disk is Invalid";
    case 0x102:
        return "Disk Error — Error During Load";
    case 0x103:
        return "Disk Error — Item Not Found";
    case 0x104:
        return "Disk Error — Unable to Create";
    case 0x105:
        return "Disk Error — Folder Not Empty";
    case 0x106:
        return "Disk Error — Unable to Delete";
    case 0x107:
        return "Disk Error — Unknown Error";
    case 0x108:
        return "Disk Error — Error During Save";
    case 0x109:
        return "Disk Error — Insufficient disk space";
    case 0x10A:
        return "Disk Error — Error During Save";
    case 0x10B:
        return "Disk Error — Media is write-protected";
    case 0x10C:
        return "Disk Error — Invalid Disk Handle";
    case 0x10D:
        return "Disk Error — Disk is Empty";
    case 0x10E:
        return "Disk Error — Disk Operation was Aborted";
    case 0x10F:
        return "Disk Error — Failed on Open";
    case 0x110:
        return "Disk Error — Read Error";
    case 0x111:
        return "Disk Error — Disk Not Ready";
    case 0x112:
        return "Disk Error — SCSI Error";
    case 0x181:
        return "Requested Keygroup Does not exist in Current Program";
    default:
        return "Unknown error code";
    }
}

int aksyxusb_device_exec_sysex(const akai_usb_device akai_dev,
        const byte_array sysex, const byte_array result_buff,
        int* const bytes_read, const int timeout) {
    struct byte_array request;
    int rc;
    char byte1 = (char)sysex->length;
    char byte2 = (char)(sysex->length>>8);
    request.length = sysex->length+3;
    request.bytes = (char*) malloc(request.length);
    memset(request.bytes, CMD_EXEC_SYSEX, 1);
    memcpy(request.bytes+1, &byte1, 1);
    memcpy(request.bytes+2, &byte2, 1);
    memcpy(request.bytes+3, sysex->bytes, sysex->length);

    rc = aksyxusb_device_exec(akai_dev, &request, result_buff, bytes_read,
            timeout);

    free(request.bytes);

    return rc;
}

int aksyxusb_device_get_panel_state(const akai_usb_device akai_dev,
        char* pixel_data, char* control_data, const int timeout) {
    struct byte_array request;
    int replies = 0;
    int rc;

    request.length = 2;
    request.bytes = CMD_LCD_GET;

    rc = aksyxusb_device_write(akai_dev, &request, timeout);

    if (rc) {
        return rc;
    }

    do {
        if (replies == 0) {
            rc = usb_bulk_read(akai_dev->dev, EP_IN, pixel_data,
                    PANEL_PIXEL_DATA_LENGTH, timeout);
            log_hex(pixel_data, 16,
                    "Pixel data - first 16 bytes (length: %i): ", rc);
        }

        if (replies == 1) {
            rc = usb_bulk_read(akai_dev->dev, EP_IN, control_data,
                    PANEL_CONTROL_DATA_LENGTH, timeout);
            log_hex(control_data, PANEL_CONTROL_DATA_LENGTH,
                    "Panel Control data (length: %i): ", rc);
        }

        if (rc <= 0) {
            return AKSY_TRANSMISSION_ERROR;
        }

        if (IS_SAMPLER_BUSY(pixel_data, rc)) {
            continue;
        }

        replies++;

    } while (replies < 2);

    return AKSY_SUCCESS;
}

int aksyxusb_device_exec(const akai_usb_device akai_dev,
        const byte_array request, const byte_array result_buff,
        int* const bytes_read, const int timeout) {
    int rc;

    rc = aksyxusb_device_write(akai_dev, request, timeout);
    if (rc) {
        return rc;
    }
    return aksyxusb_device_read(akai_dev, result_buff, bytes_read, timeout);
}

int aksyxusb_device_write(const akai_usb_device akai_dev,
        const byte_array request, const int timeout) {
    int rc;

    log_hex(request->bytes, request->length, "Request: ");

    rc = usb_bulk_write(akai_dev->dev, EP_OUT, request->bytes, request->length,
            timeout);

    return rc < 0 ? AKSY_TRANSMISSION_ERROR : AKSY_SUCCESS;
}

int aksyxusb_device_read(const akai_usb_device akai_dev,
        const byte_array result_buff, int* const bytes_read, const int timeout) {
    char* curr_index = NULL;
    int rc;

    do {
        curr_index = result_buff->bytes + *bytes_read;
        rc = usb_bulk_read(akai_dev->dev, EP_IN, curr_index,
                result_buff->length - *bytes_read, timeout);
        log_hex(curr_index, rc, "Reply (length: %i): ", rc);

        if (rc <= 0) {
            return AKSY_TRANSMISSION_ERROR;
        }

        if (IS_SAMPLER_BUSY(curr_index, rc)|| is_sysex_reply_ok(curr_index, rc)) {
            continue;
        }

        *bytes_read += rc;

        if (CONTAINS_SYSEX_MSG_END(curr_index, rc)) {
            return AKSY_SUCCESS;
        }

        if (*bytes_read == result_buff->length) {
            result_buff->length *= 2;
            result_buff->bytes = (char*)realloc(result_buff->bytes,
                    result_buff->length * sizeof(char));
        }
    } while (1);

    return AKSY_TRANSMISSION_ERROR;
}

int z48_get_handle_by_name(akai_usb_device akai_dev, const char* name,
        byte_array handle, int* sysex_error, const int timeout) {
    char *cmd_id;
    struct byte_array basename, resp_data;
    int retval, tmp_handle = 0;
    basename.length = (int)strlen(name) - 3; // exclude extension, include terminator
    resp_data.length = 5;

    if (basename.length <= 0) {
        return AKSY_INVALID_FILENAME;
    }

    if (IS_MULTI_FILE(name)) {
        cmd_id = Z48_GET_MULTI_HANDLE;
    } else if (IS_SAMPLE_FILE(name)) {
        cmd_id = Z48_GET_SAMPLE_HANDLE;
    } else if (IS_PROGRAM_FILE(name)) {
        cmd_id = Z48_GET_PROGRAM_HANDLE;
    } else if (IS_MIDI_FILE(name)) {
        cmd_id = Z48_GET_MIDI_HANDLE;
    } else {
        return AKSY_INVALID_FILENAME;
    }

    basename.bytes = (char*)calloc(basename.length, sizeof(char));
    resp_data.bytes = (char*)calloc(resp_data.length, sizeof(char));
    sprintf(basename.bytes, "%.*s", basename.length - 1, name);
    retval = aksyxusb_device_exec_cmd(akai_dev, cmd_id, &basename, &resp_data,
            sysex_error, timeout);

    free(basename.bytes);

    if (retval == AKSY_SUCCESS) {
        /* convert the handle into an integer value, skipping the type byte */
        tmp_handle = ((resp_data.bytes[4] << 21) |(resp_data.bytes[3] << 14)
                |(resp_data.bytes[2] << 7)|(resp_data.bytes[1]));

#if (_BIG_ENDIAN != 1)
        tmp_handle = ENDSWAP_INT(tmp_handle);
#endif
        memcpy(handle->bytes, &tmp_handle, handle->length);
        log_hex(handle->bytes, handle->length, "Handle ");
    }

    free(resp_data.bytes);
    return retval;
}

int s56k_get_handle_by_name(akai_usb_device akai_dev, const char* name,
        byte_array handle, int* sysex_error, const int timeout) {
    char *set_curr_item_cmd, *get_curr_index_cmd;
    struct byte_array arg, basename, resp_data;

    int retval;
    short tmp_handle;
    basename.length = (int)strlen(name) - 3;
    /* s56k handles only use 2 bytes */
    handle->length = 2;
    handle->bytes = (char*)realloc(handle->bytes, 2);

    if (basename.length <= 0) {
        return AKSY_INVALID_FILENAME;
    }
    if (IS_MULTI_FILE(name)) {
        set_curr_item_cmd = S56K_SET_CURR_MULTI_BY_NAME;
        get_curr_index_cmd = S56K_GET_CURR_MULTI_INDEX;
    } else if (IS_SAMPLE_FILE(name)) {
        set_curr_item_cmd = S56K_SET_CURR_SAMPLE_BY_NAME;
        get_curr_index_cmd = S56K_GET_CURR_SAMPLE_INDEX;
    } else if (IS_PROGRAM_FILE(name)) {
        set_curr_item_cmd = S56K_SET_CURR_PROGRAM_BY_NAME;
        get_curr_index_cmd = S56K_GET_CURR_PROGRAM_INDEX;
    } else if (IS_MIDI_FILE(name)) {
        set_curr_item_cmd = S56K_SET_CURR_MIDI_BY_NAME;
        get_curr_index_cmd = S56K_GET_CURR_MIDI_INDEX;
    } else {
        return AKSY_UNSUPPORTED_FILETYPE;
    }

    // set the current item
    basename.bytes = malloc(basename.length * sizeof(char));
    sprintf(basename.bytes, "%.*s", basename.length - 1, name);
    resp_data.length = 0;
    resp_data.bytes = NULL;

    retval = aksyxusb_device_exec_cmd(akai_dev, set_curr_item_cmd, &basename,
            &resp_data, sysex_error, timeout);

    free(basename.bytes);
    if (retval) {
        return retval;
    } else {
        // get index of current item
        arg.bytes = NULL;
        arg.length = 0;
        resp_data.length = 2;
        resp_data.bytes = malloc(resp_data.length);

        retval = aksyxusb_device_exec_cmd(akai_dev, get_curr_index_cmd, &arg,
                &resp_data, sysex_error, timeout);

        if (retval == AKSY_SUCCESS) {
            /* convert the handle into an integer value */
            tmp_handle = (((resp_data.bytes[0]&0x7f) << 7)|((resp_data.bytes[1]
                    &0x7f)));

#if (_BIG_ENDIAN != 1)
            tmp_handle = ENDSWAP_SHORT(tmp_handle);
#endif
            memcpy(handle->bytes, &tmp_handle, handle->length);
            log_hex(handle->bytes, handle->length, "Handle ");
        }
    }

    free(resp_data.bytes);
    return retval;
}

int aksyxusb_device_exec_get_request(akai_usb_device akai_dev,
        byte_array request, char *dest_filename, const int timeout) {
    char* data;
    int blocksize = 4096*4, rc = 0, read_transfer_status = 0;
    unsigned long filesize, bytes_transferred = 0, actually_transferred = 0,
            tdelta = 0, file_written;
#if defined(_POSIX_SOURCE) || defined(MACOSX)
    struct timeval tv1, tv2;
#endif
#ifdef _WIN32
    unsigned long t1;
#endif

    FILE *dest_file;
    rc = usb_bulk_write(akai_dev->dev, EP_OUT, request->bytes, request->length,
            timeout);
    if (rc < 0) {
        return AKSY_TRANSMISSION_ERROR;
    }

    dest_file = fopen(dest_filename, "w+b");

    if (!dest_file) {
        return errno;
    }

    data = calloc(blocksize, sizeof(char));
#if defined(_POSIX_SOURCE) || defined(MACOSX) 
    gettimeofday(&tv1, NULL);
#endif
#ifdef _WIN32
    t1 = GetTickCount();
#endif

    read_transfer_status = 1;
    do {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, data, blocksize, timeout);

        if (rc == blocksize && !read_transfer_status) {
            bytes_transferred+= rc;

            /* actually transferred bytes are only known in z48 protocol */
            if (actually_transferred > 0) {
                fseek(dest_file, actually_transferred, 0);
            }

            /* write to file */
            file_written = fwrite(data, sizeof(char), rc, dest_file);
            /* TODO test if file_written < rc, then error */

            /* sent continue request */
            usb_bulk_write(akai_dev->dev, EP_OUT, "\x00", 1, timeout);
            blocksize = 8;
            read_transfer_status = 1;
            continue;
        } else if (rc == 8) {
            /* get the number of bytes to read */
            log_hex(data, rc, "Reply block: ");
            actually_transferred = GET_BYTES_TRANSFERRED(data);
            if (actually_transferred == 1) {
                rc = AKSY_FILE_NOT_FOUND;
                break;
            }

            log_debug(
                    "Current block size: %i. Bytes read now: %i, Total bytes read: %li. Actually transferred: %li\n",
                    blocksize, rc, bytes_transferred, actually_transferred);

            blocksize = GET_BLOCK_SIZE(data);
            if (blocksize == 0) {
                /* file transfer completed */
                rc = AKSY_SUCCESS;
                break;
            }

            read_transfer_status = 0;
            continue;
        } else if (rc == 4) {
            if (IS_SAMPLER_BUSY(data, rc)) {
                continue;
            }
            /* s56k protocol only returns block size */
            blocksize = GET_S56K_BLOCK_SIZE(data);
            if (blocksize == 0) {
                /* file transfer completed */
                rc = AKSY_SUCCESS;
                break;
            }

            read_transfer_status = 0;
            continue;
        } else {
            log_debug(
                    "At bulk read: Unexpected reply, rc %i or unexpected end of transmission.\n",
                    rc);
            rc = AKSY_TRANSMISSION_ERROR;
            break;
        }
    } while (rc > 0);

#if defined(_POSIX_SOURCE) || defined(MACOSX)
    gettimeofday(&tv2, NULL);
    tdelta = TIMEVAL_DELTA_MILLIS(tv1, tv2);
#endif
#ifdef _WIN32
    tdelta = GetTickCount() - t1;
#endif
    filesize = ftell(dest_file);
    fclose(dest_file);
    free(data);

    if (!rc) {
        print_transfer_stats(tdelta, filesize);
        return AKSY_SUCCESS;
    } else {
        // remove(dest_filename);
        return rc;
    }
}

int aksyxusb_device_get(const akai_usb_device akai_dev, char *src_filename,
        char *dest_filename, const int location, int* sysex_error,
        const int timeout) {
    int rc = 0; 
    int src_filename_length = (int)strlen(src_filename) + 1;
    struct byte_array get_request, handle;

    /* create get request */
    if (location == LOC_MEMORY) {
        handle.length = 4;
        handle.bytes = (char*) malloc(handle.length);
        rc = akai_dev->get_handle_by_name(akai_dev, src_filename, &handle,
                sysex_error, timeout);

        if (rc) {
            free(handle.bytes);
            return rc;
        }

        get_request.length = handle.length + 1;
        get_request.bytes = (char*) malloc(get_request.length);

        if (IS_SAMPLE_FILE(src_filename)) {
            get_request.bytes[0] = CMD_MEMORY_GET_SAMPLE;
        } else if (IS_PROGRAM_FILE(src_filename)) {
            get_request.bytes[0] = akai_dev->get_program_cmd_id;
        } else if (IS_MULTI_FILE(src_filename)) {
            get_request.bytes[0] = akai_dev->get_multi_cmd_id;
        } else if (IS_MIDI_FILE(src_filename)) {
            get_request.bytes[0] = Z48_CMD_MEMORY_GET_MIDI;
        } else {
            log_error(AKSY_UNSUPPORTED_FILETYPE, __LINE__);
        }

        memcpy(get_request.bytes+1, handle.bytes, handle.length);
        free(handle.bytes);
        log_hex(get_request.bytes, get_request.length, "Request cmd ");
        rc = aksyxusb_device_exec_get_request(akai_dev, &get_request,
                dest_filename, timeout);
        free(get_request.bytes);
        return rc;
    } else {
        get_request.length = src_filename_length+1;
        get_request.bytes = (char*) malloc(get_request.length * sizeof(char));
        get_request.bytes[0] = CMD_DISK_GET;
        memcpy(get_request.bytes+1, src_filename, src_filename_length
                * sizeof(char));
        log_hex(get_request.bytes, get_request.length, "Request cmd ");
        rc = aksyxusb_device_exec_get_request(akai_dev, &get_request,
                dest_filename, timeout);
        free(get_request.bytes);
        return rc;
    }
}

/* uploads a file to the sampler. */
int aksyxusb_device_put(const akai_usb_device akai_dev, const char *src_filename,
        const char *dest_filename, const int location, const int timeout) {
    char *buf, *command, *reply_buf, *tmp;
    unsigned long filesize = 0, transferred = 0, tdelta = 0;
    int rc, retval = 0, blocksize = 0, init_blocksize = 4096 * 8,
            bytes_read = 0, command_len = 0;
    int dest_filename_length = (int)strlen(dest_filename) + 1;
    FILE* fp;

#if defined(_POSIX_SOURCE) || defined(MACOSX)
    struct stat* st;
    struct timeval tv1, tv2;
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
    long t1;
    HANDLE tmp_fp = CreateFile(
            src_filename,
            GENERIC_READ,
            FILE_SHARE_READ,
            NULL,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            NULL);

    if (tmp_fp == INVALID_HANDLE_VALUE) {
        return AKSY_FILE_STAT_ERROR;
    }

    filesize = GetFileSize(tmp_fp, NULL);

    CloseHandle(tmp_fp);

    if (filesize == INVALID_FILE_SIZE) {
        return AKSY_FILE_STAT_ERROR;
    }
#endif

    if (filesize == 0) {
        return AKSY_EMPTY_FILE_ERROR;
    }

#if (AKSY_DEBUG == 1)
    printf("File name to upload %s, Size of file: %li bytes\n", dest_filename, filesize);
#endif
    command_len = dest_filename_length+5;  //5 is the header size
    
    command = (char*) calloc(command_len, sizeof(char));
    if (akai_dev->sysex_id == S56K_ID)
       {
       if (IS_MULTI_FILE(dest_filename))
          { // TODO:  DISK put untested
          command[0] = (location) ? S56K_CMD_MEMORY_PUT_MULTI : CMD_DISK_PUT;
          }
       if (IS_SAMPLE_FILE(dest_filename))
          {
          command[0] = (location) ? CMD_MEMORY_PUT : CMD_DISK_PUT;
          }
       if (IS_PROGRAM_FILE(dest_filename))
          {
          command[0] = (location) ? S56K_CMD_MEMORY_PUT_PROGRAM : CMD_DISK_PUT;
          }
       if (IS_MIDI_FILE(dest_filename))
          {
          command[0] = (location) ? S56K_CMD_MEMORY_PUT_MIDI : CMD_DISK_PUT;
          }
       if (IS_SCENE_FILE(dest_filename))
          {
          command[0] = (location) ? S56K_CMD_MEMORY_PUT_SCENE : CMD_DISK_PUT;
          }
       
       
       }
    else  // Z
       {
       command[0] = (location) ? CMD_MEMORY_PUT : CMD_DISK_PUT;
       }
    // TODO: check ppc
    command[1] = (char)(filesize >> 24);
    command[2] = (char)(filesize >> 16);
    command[3] = (char)(filesize >> 8);
    command[4] = (char)filesize;

    memcpy(command+5, dest_filename, dest_filename_length * sizeof(char));

    rc = usb_bulk_write(akai_dev->dev, EP_OUT, command, command_len,
            timeout);

    if (rc < 0) {
        free(command);
        return AKSY_TRANSMISSION_ERROR;
    }

    reply_buf = (char*) calloc(64, sizeof(char));

#if defined(_POSIX_SOURCE) || defined(MACOSX)
    gettimeofday(&tv1, NULL);
#endif
#ifdef _WIN32
    t1 = GetTickCount();
#endif

    fp = fopen(src_filename, "rb");

    if (!fp) {
        free(command);
        free(reply_buf);
        return AKSY_FILE_READ_ERROR;;
    }

    buf = calloc(init_blocksize, sizeof(char));

    do {
        rc = usb_bulk_read(akai_dev->dev, EP_IN, reply_buf, 64, timeout);

        log_hex(reply_buf, rc, "return code: %i\n", rc);

        if (rc == 1) {
            if (IS_INVALID_FILE_ERROR(reply_buf)) {
                retval = AKSY_INVALID_FILE;
                break;
            }

            if (IS_TRANSFER_FINISHED(reply_buf)) {
                if (akai_dev->sysex_id == S56K_ID) {
                    // S56k transfer ends here
                    break;
                }
                continue;
            }
            printf("Unexpected return value %i\n", reply_buf[0]);
            break;
        }

        if (IS_SAMPLER_BUSY(reply_buf, rc)) {
            continue;
        } else if (rc == 8) {
            blocksize = GET_BLOCK_SIZE(reply_buf);
            if (blocksize > init_blocksize) {
               tmp = realloc(buf, blocksize * sizeof(char));
               if (tmp != NULL) {
                  buf = tmp;
               } else {
                  /* exit ? */
               }
            }
            transferred = GET_BYTES_TRANSFERRED(reply_buf);
            log_debug("blocksize: %i\n", blocksize);
            log_debug("transferred: %li\n", transferred);

            if (transferred == filesize) {
                // continue reading last reply
                continue;
            }
        } else if (rc == 5) {
            break; // finished TODO: check contents of buffer...
        }
        // seek to the position in the file for the next block of data
        // could be duplicated depending on what the amount transferred return
        fseek(fp, transferred, 0);
        bytes_read = fread(buf, sizeof(char), blocksize, fp);

        log_debug("writing %i bytes\n", bytes_read);

        usb_bulk_write(akai_dev->dev, EP_OUT, buf, bytes_read, timeout);

        /* continue */
        usb_bulk_write(akai_dev->dev, EP_OUT, "\x00", 1, timeout);
    } while (bytes_read > 0&& rc > 0);

#if defined(_POSIX_SOURCE) || defined(MACOSX)
    gettimeofday(&tv2, NULL);
    tdelta = TIMEVAL_DELTA_MILLIS(tv1, tv2);
#endif
#ifdef _WIN32
    tdelta = GetTickCount() - t1;
#endif

    if (ferror(fp)) {
        retval = AKSY_FILE_READ_ERROR;
    }

    fclose(fp);
    free(reply_buf);
    free(buf);
    free(command);

    if (!retval) {
        print_transfer_stats(tdelta, filesize);
    }
    return retval;
}
