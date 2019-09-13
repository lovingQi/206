#ifndef iio_fm_radio
#define iio_fm_radio

#include <errno.h>
#include <signal.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/ioctl.h>
#include <linux/types.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include "iio_utils.h"

#define IIO_BLOCK_ALLOC_IOCTL   _IOWR('i', 0xa0, struct iio_buffer_block_alloc_req)
#define IIO_BLOCK_FREE_IOCTL    _IO('i', 0xa1)
#define IIO_BLOCK_QUERY_IOCTL   _IOWR('i', 0xa2, struct iio_buffer_block)
#define IIO_BLOCK_ENQUEUE_IOCTL _IOWR('i', 0xa3, struct iio_buffer_block)
#define IIO_BLOCK_DEQUEUE_IOCTL _IOWR('i', 0xa4, struct iio_buffer_block)
#define DECIMATION_FACTOR 48
#define AUDIO_SAMPLE_RATE 48000
#define ALIGN(x, y) ((x) / (y)) * (y)

struct iio_buffer_block_alloc_req {
	__u32 type;
	__u32 size;
	__u32 count;
	__u32 id;
};

struct iio_buffer_block {
	__u32 id;
	__u32 size;
	__u32 bytes_used;
	__u32 type;
	__u32 flags;
	union {
		__u32 offset;
	} data;
	__u64 timestamp;
};

struct block {
	struct iio_buffer_block block;
	short *addr;
};


static int demodulate(struct iio_buffer_block *block,int* dst,int cnum,int* life);
static void terminate(int signal);
static void setup_sigterm_handler(void);
int fmdm(int* life,int* dst,int cnum);
static struct block blocks[5];

/* Min and max are used for automatic gain control and DC offset control */
static int min = 0xfffffff;
static int max = -0xfffffff;
#endif
