
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "iio_fm_radio.h"
#include "ad9365.h"

#define SERVER_CMD_PORT inet_addr("127.0.0.1")
#define SERVER_CMD_ADDR 10106
#define SERVER_SOUND_ADDR inet_addr("127.0.0.1")
#define SERVER_SOUND_PORT 10103
#define SERVER_SPECTRUM_ADDR inet_addr("127.0.0.1")
#define SERVER_SPECTRUM_PORT 10101

void control_process(void *arg);
