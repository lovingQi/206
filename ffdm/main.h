
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "iio_fm_radio.h"
#include "ad9365.h"

#define CRTL_PORT 10102
#define NET_PORT 10101
#define FFT_PORT 10103
void control_process(void *arg);
