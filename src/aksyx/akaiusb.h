/* akai usb device api */
#include <usb.h>
#include <stdio.h>

#define VENDOR_ID 0x9E8 
#define S56K 0x05E
#define Z48 0x05F
#define EP_OUT 0x82
#define EP_IN 0x02
#define USB_TIMEOUT 2000
#define Z48_DISK 0
#define Z48_MEMORY 1
#define Z48_DISK_GET 0x41
#define Z48_MEMORY_GET 0x22
#define Z48_MEMORY_PUT 0x20
#define Z48_DISK_PUT 0x00
#define GET_BLOCK_SIZE(buffer) (buffer[7] | buffer[6] << 8 | buffer[5] << 16 | buffer[4] << 24)
#define GET_BYTES_TRANSFERRED(buffer) (buffer[3] | buffer[2] << 8 | buffer[1] << 16 | buffer[0] << 24)
#define AKAI_NO_USB_HANDLE -5000
#define AKAI_NO_SAMPLER_FOUND -5001
#define AKAI_UNSUPPORTED_DEVICE -5002
#define AKAI_TRANSMISSION_ERROR -5003

typedef struct _akai_usb_device {
    usb_dev_handle *dev;
    int type;
} *akai_usb_device;

/* opens a akai usb device */
int akai_usb_device_init(akai_usb_device akai_dev);
/* closes a akai usb device */
int akai_usb_device_close(akai_usb_device akai_dev);

int akai_usb_device_send_bytes(akai_usb_device akai_dev, char* bytes, 
    int byte_length, int timeout);

int akai_usb_device_recv_bytes(akai_usb_device akai_dev, char* buff, 
    int buff_length, int timeout);

int akai_usb_device_exec_sysex(akai_usb_device akai_dev,  
    char *sysex, int sysex_length, 
    char *result_buff, int result_buff_length, int timeout);

/* uploads a file to the sampler. location is Z48_MEMORY or Z48_DISK */
int akai_usb_device_put(akai_usb_device akai_dev, 
    char *src_filename, char *dest_filename, int timeout);

/* transfers a file from the sampler. */
int akai_usb_device_get(akai_usb_device akai_dev, 
    char *src_filename, char *dest_filename, int location, int timeout);
