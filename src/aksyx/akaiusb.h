#include <usb.h>
#include <stdio.h>

#define VENDOR_ID 0x9e8
#define S56K_ID 0x05e
#define Z48_ID 0x05f
#define MPC4K_ID 0x061

#define EP_IN 0x82
#define EP_OUT 0x02
#define LOC_DISK 0
#define LOC_MEMORY 1

/* transfer commands */
#define Z48_DISK_GET 0x41
#define Z48_DISK_PUT 0x40
#define Z48_MEMORY_PUT 0x20
#define Z48_MEMORY_GET_SAMPLE 0x21
#define Z48_MEMORY_GET_PROGRAM 0x22
#define Z48_MEMORY_GET_MULTI 0x23
#define Z48_MEMORY_GET_MIDI 0x24

/* gives a z48_ok reply */
#define Z48_ABORT 0xff

/* XXX: this retrieves current handles, there is no get_handle_by_name cmd for S56K */
#define S56K_GET_SAMPLE_HANDLE "\x0e\x13"
#define S56K_GET_PROGRAM_HANDLE "\x10\x12"
#define S56K_GET_MULTI_HANDLE "\x0c\x42"
#define S56K_GET_MIDI_HANDLE "\x16\x13"

/* sysex defs */
#define SYSEX_OK 0x4f
#define SYSEX_REPLY 0x52
#define SYSEX_ERROR 0x45

/* sysex commands */
#define Z48_GET_SAMPLE_HANDLE "\x1c\x08"
#define Z48_GET_PROGRAM_HANDLE "\x14\x08"
#define Z48_GET_MULTI_HANDLE "\x18\x08"
#define Z48_GET_MIDI_HANDLE "\x28\x08"

#define GET_BLOCK_SIZE(buffer) (buffer[7] | buffer[6] << 8 | buffer[5] << 16 | buffer[4] << 24)
#define GET_BYTES_TRANSFERRED(buffer) (buffer[3] | buffer[2] << 8 | buffer[1] << 16 | buffer[0] << 24)

/* error codes */
#define AKAI_SUCCESS 0
#define AKAI_USB_INIT_ERROR 5000
#define AKAI_NO_SAMPLER_FOUND 5001
#define AKAI_UNSUPPORTED_DEVICE 5002
#define AKAI_TRANSMISSION_ERROR 5003
#define AKAI_SYSEX_ERROR 5004
#define AKAI_SYSEX_UNEXPECTED 5005
#define AKAI_INVALID_FILENAME 5006
#define AKAI_FILE_NOT_FOUND 5007
#define AKAI_FILE_STAT_ERROR 5008
#define AKAI_FILE_READ_ERROR 5009
#define AKAI_EMPTY_FILE_ERROR 5010

#define ENDSWAP_INT(x) ((((x)>>24)&0xFF)+(((x)>>8)&0xFF00)+(((x)&0xFF00)<<8)+(((x)&0xFF)<<24))

#define IS_MULTI_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "akm") == 0)
#define IS_SAMPLE_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "wav") == 0)
#define IS_PROGRAM_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "akp") == 0)
#define IS_MIDI_FILE(filename) (strlen(filename)  > 4 && strcasecmp(filename + strlen(filename) - 3, "mid") == 0)

typedef struct _sysex_commands {
	char* get_multi_handle;
	char* get_sample_handle;
	char* get_midi_handle;
	char* get_program_handle;
} sysex_commands;

typedef struct _akai_usb_device {
    usb_dev_handle *dev;
    int usb_product_id;
    int sysex_id;
    sysex_commands commands;
    int userref_length;
    char *userref;

} *akai_usb_device;

/*
 * akaiusb public api methods
 *
 */

/* opens a akai usb device. allocated memory is freed in case the
 * device initialisation goes wrong
 */
int akai_usb_device_init(akai_usb_device akai_dev);

/* resets a akai usb device */
int akai_usb_device_reset(akai_usb_device akai_dev);

/* closes a akai usb device */
int akai_usb_device_close(akai_usb_device akai_dev);

int akai_usb_device_send_bytes(akai_usb_device akai_dev, unsigned char* bytes,
    int byte_length, int timeout);

int akai_usb_device_recv_bytes(akai_usb_device akai_dev, unsigned char* buff,
    int buff_length, int timeout);

/* executes a system exclusive string on the sampler.
 * the return code is the return code of the underlying usb reads/writes
 */
int akai_usb_device_exec_sysex(akai_usb_device akai_dev,
    unsigned char *sysex, int sysex_length,
    unsigned char *result_buff, int result_buff_length, int timeout);

/* get a handle for a specified name
 * handle should be a pointer to a preallocated 4 byte value
 */
int akai_usb_device_get_handle_by_name(akai_usb_device akai_dev,
    unsigned char* name, unsigned char* handle, int timeout);

/* uploads a file to the sampler. location is Z48_MEMORY or Z48_DISK
 * The current path must be set explicitly if the file is transferred to
 * disk
 */
int akai_usb_device_put(akai_usb_device akai_dev,
    unsigned char *src_filename, unsigned char *dest_filename, int location, int timeout);

/* transfers a file from the current path from the sampler.
 * Location can be either LOC_MEMORY or LOC_DISK.
 * The current path must be set to the folder where the file is
 * located before calling this function in case of disk transfers
 */
int akai_usb_device_get(akai_usb_device akai_dev,
    unsigned char *src_filename, unsigned char *dest_filename, int location, int timeout);
