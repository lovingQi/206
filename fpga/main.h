
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "iio_fm_radio.h"
#include "ad9365.h"
#define SERVER_ADDR "119.29.209.127"
//#define SERVER_ADDR "192.168.3.19"
#define CRTL_PORT 10106
#define NET_PORT 10103
#define SOUND_PORT 10103
#define FFT_PORT 10101
void control_process(void *arg);
