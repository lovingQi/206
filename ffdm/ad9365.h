#ifndef ad9365
#define ad9365
#define FMDM 1
#define FFT_PORT 10103
#define DECIMATION_FACTOR 48
#define AUDIO_SAMPLE_RATE 48000
#include <math.h>
#include <stdbool.h>
#define N 8192
#define NFM 8192
#include <stdint.h>
#include <string.h>
#include <signal.h>
#include <stdio.h>
#include "fftw3.h"  
#include<netinet/in.h>
#include<sys/socket.h>
#include <arpa/inet.h>
#include <iio.h>
#include <unistd.h>
/* helper macros:wq
 */
#define MHZ(x) ((long long)(x*1000000.0 + .5))
#define GHZ(x) ((long long)(x*1000000000.0 + .5))

#define ASSERT(expr) { \
	if (!(expr)) { \
		(void) fprintf(stderr, "assertion failed (%s:%d)\n", __FILE__, __LINE__); \
		(void) abort(); \
	} \
}

enum iodev { RX, TX };

/* common RX and TX streaming params */
struct stream_cfg {
	long long bw_hz; // Analog banwidth in Hz
	long long fs_hz; // Baseband sample rate in Hz
	long long lo_hz; // Local oscillator frequency in Hz
	const char* rfport; // Port name
};

static void iio_shutdown();
static void handle_sig(int sig);
static void errchk(int v, const char* what);
static void wr_ch_lli(struct iio_channel *chn, const char* what, long long val);
static void wr_ch_str(struct iio_channel *chn, const char* what, const char* str);
static char* get_ch_name(const char* type, int id);
static struct iio_device* get_ad9361_phy(struct iio_context *ctx);
static bool get_ad9361_stream_dev(struct iio_context *ctx, enum iodev d, struct iio_device **dev);
static bool get_ad9361_stream_ch(struct iio_context *ctx, enum iodev d, struct iio_device *dev, int chid, struct iio_channel **chn);
static bool get_phy_chan(struct iio_context *ctx, enum iodev d, int chid, struct iio_channel **chn);
static bool get_lo_chan(struct iio_context *ctx, enum iodev d, struct iio_channel **chn);
bool cfg_ad9361_streaming_ch(struct iio_context *ctx, struct stream_cfg *cfg, enum iodev type, int chid);
int ffts (int *life,int dst);

#endif
