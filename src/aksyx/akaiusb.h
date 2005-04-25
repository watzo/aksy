/* akai usb device api */
#include <usb.h>
#include <stdio.h>

#define VENDOR_ID 0x9E8 
#define S56K 0x05E
#define Z48 0x05F
#define EP_OUT 0x82
#define EP_IN 0x02
#define Z48_DISK 0
#define Z48_MEMORY 1
/* commands */
#define Z48_DISK_GET 0x41
#define Z48_MEMORY_GET 0x22
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
#define AKAI_SUCCESS 1 
#define AKAI_NO_USB_HANDLE 5000
#define AKAI_NO_SAMPLER_FOUND 5001
#define AKAI_UNSUPPORTED_DEVICE 5002
#define AKAI_TRANSMISSION_ERROR 5003
#define AKAI_SYSEX_ERROR 5004
#define AKAI_SYSEX_UNEXPECTED 5005

typedef struct _akai_usb_device {
    usb_dev_handle *dev;
    unsigned char id;
} *akai_usb_device;

/* opens a akai usb device. allocated memory is freed in case the
 * device initialisation goes wrong  
 */
int akai_usb_device_init(akai_usb_device akai_dev);

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
 */
int akai_usb_device_get_handle_by_name(akai_usb_device akai_dev,
    char* name, char* handle, int timeout);

/* uploads a file to the sampler. location is Z48_MEMORY or Z48_DISK
 * The current path must be set explicitly if the file is transferred to
 * disk
 */
int akai_usb_device_put(akai_usb_device akai_dev, 
    char *src_filename, char *dest_filename, int timeout);

/* transfers a file from the current path from the sampler. 
 * Location can be either Z48_MEMORY or Z48_DISK.
 * The current path must be set explicitly if the file is transferred from
 * disk
 */
int akai_usb_device_get(akai_usb_device akai_dev, 
    char *src_filename, char *dest_filename, int location, int timeout);
