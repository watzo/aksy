/* akai usb device api */
#include <usb.h>
#include <stdio.h>

#define VENDOR_ID 0x9e8 
#define S56K 0x05e
#define Z48 0x05f
#define EP_OUT 0x82
#define EP_IN 0x02
#define LOC_DISK 0
#define LOC_MEMORY 1
/* commands */
#define Z48_DISK_GET 0x41
#define Z48_MEMORY_GET_SAMPLE 0x21
#define Z48_MEMORY_GET_PROGRAM 0x22
#define Z48_MEMORY_GET_MULTI 0x23
#define Z48_MEMORY_GET_MIDI 0x24
#define Z48_MEMORY_PUT 0x20
#define Z48_DISK_PUT 0x40
/* sysex defs */
#define SYSEX_OK 0x4f
#define SYSEX_REPLY 0x52
#define SYSEX_ERROR 0x45
/* gives a z48_ok reply */
#define Z48_ABORT 0xff
#define GET_BLOCK_SIZE(buffer) (buffer[7] | buffer[6] << 8 | buffer[5] << 16 | buffer[4] << 24)
#define GET_BYTES_TRANSFERRED(buffer) (buffer[3] | buffer[2] << 8 | buffer[1] << 16 | buffer[0] << 24)

/* error codes */
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

#define ENDSWAP_INT(x) ((((x)>>24)&0xFF)+(((x)>>8)&0xFF00)+(((x)&0xFF00)<<8)+(((x)&0xFF)<<24))

typedef struct _akai_usb_device {
    usb_dev_handle *dev;
    int id;
} *akai_usb_device;

/* opens a akai usb device. allocated memory is freed in case the
 * device initialisation goes wrong  
 */
int akai_usb_device_init(akai_usb_device akai_dev);

/* resets a akai usb device */
int akai_usb_device_reset(akai_usb_device akai_dev);

/* closes a akai usb device */
int akai_usb_device_close(akai_usb_device akai_dev);

int akai_usb_device_send_bytes(akai_usb_device akai_dev, char* bytes, 
    int byte_length, int timeout);

int akai_usb_device_recv_bytes(akai_usb_device akai_dev, char* buff, 
    int buff_length, int timeout);

/* executes a system exclusive string on the sampler.
 * the return code is the return code of the underlying usb reads/writes 
 */
int akai_usb_device_exec_sysex(akai_usb_device akai_dev,  
    char *sysex, int sysex_length, 
    char *result_buff, int result_buff_length, int timeout);

/* get a handle for a specified name
 * handle should be a pointer to a preallocated 4 byte value
 * cmd_id may be NULL - if specified it will be set to the command id used
 * by file transfers from the sampler
 */
int akai_usb_device_get_handle_by_name(akai_usb_device akai_dev,
    char* name, char* handle, char* cmd_id, int timeout);

/* uploads a file to the sampler. location is Z48_MEMORY or Z48_DISK
 * The current path must be set explicitly if the file is transferred to
 * disk
 */
int akai_usb_device_put(akai_usb_device akai_dev, 
    char *src_filename, char *dest_filename, int location, int timeout);

/* transfers a file from the current path from the sampler. 
 * Location can be either LOC_MEMORY or LOC_DISK.
 * The current path must be set to the folder where the file is
 * located before calling this function in case of disk transfers
 */
int akai_usb_device_get(akai_usb_device akai_dev, 
    char *src_filename, char *dest_filename, int location, int timeout);
