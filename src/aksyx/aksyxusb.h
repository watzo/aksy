#include <usb.h>
#include <stdio.h>

#define VENDOR_ID 0x9e8
#define S56K_ID 0x05e
#define Z48_ID 0x05f
#define MPC4K_ID 0x061

#define EP_IN 0x82
#define EP_OUT 0x02

/*
 transfer commands
 */
#define CMD_EXEC_SYSEX 0x10
#define CMD_DISK_GET 0x41
#define CMD_DISK_PUT 0x40
#define CMD_MEMORY_PUT 0x20
#define CMD_MEMORY_GET_SAMPLE 0x21

#define CMD_LCD_GET "\x01\x00"

#define Z48_CMD_MEMORY_GET_PROGRAM 0x22
#define Z48_CMD_MEMORY_GET_MULTI 0x23
#define Z48_CMD_MEMORY_GET_MIDI 0x24

#define S56K_CMD_MEMORY_PUT_PROGRAM 0x22
#define S56K_CMD_MEMORY_GET_PROGRAM 0x23
#define S56K_CMD_MEMORY_PUT_MULTI 0x24
#define S56K_CMD_MEMORY_GET_MULTI 0x25
#define S56K_CMD_MEMORY_PUT_SCENE 0x26
#define S56K_CMD_MEMORY_PUT_MIDI 0x28
#define S56K_CMD_MEMORY_GET_MIDI 0x29

/* abort an operation, returns a busy reply on success */
#define Z48_ABORT 0xff

#define S56K_SET_CURR_SAMPLE_BY_NAME "\x0e\x05"
#define S56K_SET_CURR_PROGRAM_BY_NAME "\x0a\x05"
#define S56K_SET_CURR_MULTI_BY_NAME "\x0c\x05"
#define S56K_SET_CURR_MIDI_BY_NAME "\x16\x05"

#define S56K_GET_CURR_SAMPLE_INDEX "\x0e\x13"
#define S56K_GET_CURR_PROGRAM_INDEX "\x0a\x12"
#define S56K_GET_CURR_MULTI_INDEX "\x0c\x42"
#define S56K_GET_CURR_MIDI_INDEX "\x16\x13"

/* sysex defs */
#define SYSEX_START 0xf0
#define SYSEX_AKAI_ID 0x47
#define SYSEX_END 0xf7
#define SYSEX_OK 0x4f
#define SYSEX_DONE 0x44
#define SYSEX_REPLY 0x52
#define SYSEX_ERROR 0x45

/* sysex commands */
#define Z48_GET_SAMPLE_HANDLE "\x1c\x08"
#define Z48_GET_PROGRAM_HANDLE "\x14\x08"
#define Z48_GET_MULTI_HANDLE "\x18\x08"
#define Z48_GET_MIDI_HANDLE "\x28\x08"

/* constants*/

#define PANEL_PIXEL_DATA_LENGTH 1860
#define PANEL_CONTROL_DATA_LENGTH 18

/* macros */
#define GET_BLOCK_SIZE(buffer) ((buffer[7]&0xFF) | ((buffer[6]&0xFF) << 8) | ((buffer[5]&0xFF) << 16) | ((buffer[4]&0xFF) << 24))
#define GET_BYTES_TRANSFERRED(buffer) ((buffer[3]&0xFF) | ((buffer[2]&0xFF) << 8) | ((buffer[1]&0XFF) << 16) | ((buffer[0]&0xFF) << 24))
#define GET_S56K_BLOCK_SIZE GET_BYTES_TRANSFERRED

/* Useless facts: 0x41 0x6b 0x61 0x49: AkaI in ascii */
#define IS_SAMPLER_BUSY(buffer, length) (length == 4 && buffer[0] == 0x41 && buffer[1] == 0x6b && buffer[2] == 0x61 && buffer[3] == 0x49)
#define IS_INVALID_FILE_ERROR(buffer) (buffer[0] == 0x1)
#define IS_TRANSFER_FINISHED(buffer) (buffer[0] == 0x0)
#define CONTAINS_SYSEX_MSG_END(buffer, length) (buffer[length - 1] == (char)SYSEX_END)

#define ENDSWAP_INT(x) ((((x)>>24)&0xFF)+(((x)>>8)&0xFF00)+(((x)&0xFF00)<<8)+(((x)&0xFF)<<24))
#define ENDSWAP_SHORT(x) ((((x)>>8)&0xFF)+(((x)&0xFF)<<8))

#define IS_MULTI_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "akm") == 0)
#define IS_SAMPLE_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "wav") == 0)
#define IS_PROGRAM_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "akp") == 0)
#define IS_MIDI_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "mid") == 0)
#define IS_SCENE_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "asc") == 0)

#define TIMEVAL_DELTA_MILLIS(t1, t2) ((t2.tv_sec-t1.tv_sec)*1000 + (t2.tv_usec-t1.tv_usec)/1000)

enum TRANSFER_LOCATIONS {
    LOC_DISK,
    LOC_MEMORY,
};

enum RETURN_CODES {
    AKSY_SUCCESS=0,
    AKSY_USB_INIT_ERROR=5000,
    AKSY_USB_RESET_ERROR,
    AKSY_USB_CLOSE_ERROR,
    AKSY_NO_SAMPLER_FOUND,
    AKSY_UNSUPPORTED_DEVICE,
    AKSY_TRANSMISSION_ERROR,
    AKSY_SYSEX_ERROR,
    AKSY_SYSEX_UNEXPECTED,
    AKSY_INVALID_FILENAME,
    AKSY_UNSUPPORTED_FILETYPE,
    AKSY_INVALID_FILE, /* corrupt file, invalid file name/type */
    AKSY_FILE_NOT_FOUND,
    AKSY_FILE_STAT_ERROR,
    AKSY_FILE_READ_ERROR,
    AKSY_EMPTY_FILE_ERROR,
};

/* General Errors */
// The <Section> <Item> supplied are not supported
#define SERR_CMD_UNSUPPORTED 0x00
// "Checksum invalid"
#define SERR_CHECKSUM_INVALID 0x01
// "Unknown error"
#define SERR_UNKNOWN 0x02
// "Invalid message format"
#define SERR_MSG_INVALID 0x03
// "Parameter out of range"
#define SERR_PARAM_VALUE 0x04
// "Operation is pending"
#define SERR_OPER_PENDING 0x05
// "Unknown system error"
#define SERR_SYSTEM 0x80
// Operation had no effect
#define SERR_NOOP 0x81
// Fatal error
#define SERR_FATAL 0x82
// CPU memory is full
#define SERR_CPU_MEM_FULL 0x83
// WAVE memory is full
#define SERR_WAV_MEM_FULL 0x84
// Unknown item error
#define SERR_ITEM_UNKNOWN 0x100
// Item not found
#define SERR_ITEM_NOT_FOUND 0x101
// Item in use
#define SERR_ITEM_IN_USE 0x102
// Invalid item handle
#define SERR_HANDLE_INVALID 0x103
// Invalid item name
#define SERR_ITEM_NAME_INVALID 0x104
// Maximum number of items of a particular type reached
#define SERR_MAX_ITEMS 0x105
// Keygroup not found
#define SERR_KG_NOT_FOUND 0x120
// Unknown disk error
#define SERR_DISK_UNKNOWN 0x180
// No Disks
#define SERR_NO_DISKS 0x181
// Disk is invalid
#define SERR_DISK_INVALID 0x182
// Load error
#define SERR_LOAD 0x183
// Create error
#define SERR_CREATE 0x184
// Directory not empty
#define SERR_DIR_NOT_EMPTY 0x185
// Delete error
#define SERR_DELETE 0x186
// Disk is write-protected
#define SERR_DISK_READONLY 0x187
// Disk is not writable
#define SERR_DISK_WRITABLE 0x188
// Disk full
#define SERR_DISK_FULL 0x189
// Disk abort
#define SERR_DISK_ABORT 0x18A
// Unknown file error
#define SERR_FILE_UNKNOWN 0x200
// File format is not supported
#define SERR_FILE_FMT 0x201
// WAV format is incorrect
#define SERR_WAVE_FMT 0x202
// File not found
#define SERR_FILE_NOT_FOUND 0x203
// File already exists
#define SERR_FILE_EXISTS 0x204

typedef struct byte_array {
    char *bytes;
    int length;
} *byte_array;

typedef struct akai_usb_device {
    usb_dev_handle *dev;
    int usb_product_id;
    int sysex_id;
    int userref_length;
    char *userref;
    int get_program_cmd_id;
    int get_multi_cmd_id;
    int (*get_handle_by_name)(struct akai_usb_device*, const char*, byte_array,
            int*, const int);
    char* (*get_sysex_error_msg)(int code);
} *akai_usb_device;


/*
 * akaiusb public API functions
 *
 * all methods return AKSY_SUCCESS on success
 */

/* opens a akai usb device
 *
 * returns AKSY_USB_INIT_ERROR if the usb setup failed or AKSY_NO_SAMPLER_FOUND
 * if no supported samplers were found
 *
 */
int aksyxusb_device_init(const akai_usb_device akai_dev);

/* resets a akai usb device */
int aksyxusb_device_reset(const akai_usb_device akai_dev);

/* closes a akai usb device */
int aksyxusb_device_close(const akai_usb_device akai_dev);

/* executes a system exclusive string on the sampler.
 *
 * returns AKSY_TRANSMISSION_ERROR if the usb reads or writes failed
 *
 */
int aksyxusb_device_exec_sysex(const akai_usb_device akai_dev,
        const byte_array sysex, const byte_array reply, int* const bytes_read,
        const int timeout);

/* retrieves raw front panel state (pixel data and raw values of controls)
 *
 * returns AKSY_TRANSMISSION_ERROR if the usb reads or writes failed
 *
 */
int aksyxusb_device_get_panel_state(const akai_usb_device akai_dev,
        char* pixel_data, char* control_data, const int timeout);

/* executes a system exclusive command on the sampler.
 *
 * the caller is responsible to allocate enough memory to contain the response data, including type bytes
 * returns AKSY_SYSEX_ERROR if the command yielded an error on the sampler
 *
 */
int aksyxusb_device_exec_cmd(const akai_usb_device akai_dev, const char* cmd,
        const byte_array arg_data, const byte_array response, int* error,
        const int timeout);

/* executes a a raw request on the sampler. */
int aksyxusb_device_exec(const akai_usb_device akai_dev,
        const byte_array request, const byte_array result_buff,
        int* const bytes_read, const int timeout);

/* writes a a raw request to the sampler. */
int aksyxusb_device_write(const akai_usb_device akai_dev,
        const byte_array request, const int timeout);

/* reads a raw response from the sampler. */
int aksyxusb_device_read(const akai_usb_device akai_dev,
        const byte_array result_buff, int* const bytes_read, const int timeout);

/* get a handle for a specified name
 * handle should be a pointer to a preallocated byte_array
 */
int z48_get_handle_by_name(akai_usb_device akai_dev, const char* name,
        byte_array handle, int* sysex_error, const int timeout);
int s56k_get_handle_by_name(akai_usb_device akai_dev, const char* name,
        byte_array handle, int* sysex_error, const int timeout);

/*
 * Return an error message corresponding to the specified code.
 */
char* z48_get_sysex_error_msg(int code);
char* s56k_get_sysex_error_msg(int code);

/* uploads a file to the sampler. location is LOC_MEMORY or LOC_DISK
 * The current path must be set explicitly if the file is transferred to
 * disk
 */
int aksyxusb_device_put(const akai_usb_device akai_dev, const char *src_filename,
        const char *dest_filename, const int location, const int timeout);

/* transfers a file from the current path from the sampler.
 * Location can be either LOC_MEMORY or LOC_DISK.
 * The current path must be set to the folder where the file is
 * located before calling this function if location is LOC_DISK
 */
int aksyxusb_device_get(const akai_usb_device akai_dev, char *src_filename,
        char *dest_filename, const int location, int* sysex_error,
        const int timeout);
