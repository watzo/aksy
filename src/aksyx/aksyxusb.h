#define VENDOR_ID 0x9E8 
#define S56K_PRODUCT_ID 0x05E
#define PRODUCT_ID 0x05F
#define EP_OUT 0x82
#define EP_IN 0x02
#define USB_TIMEOUT 2000
#define Z48_DISK_GET 0x41
#define Z48_MEMORY_GET 0x22
#define Z48_MEMORY_PUT 0x20
#define Z48_DISK_PUT 0x40
#define GET_BLOCK_SIZE(buffer) (buffer[7] | buffer[6] << 8 | buffer[5] << 16 | buffer[4] << 24)
#define GET_BYTES_TRANSFERRED(buffer) (buffer[3] | buffer[2] << 8 | buffer[1] << 16 | buffer[0] << 24)
extern void initaksyxusb(void);
