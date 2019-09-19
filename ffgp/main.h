
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "iio_fm_radio.h"
#include "ad9365.h"

#define MAX_CLI 20
#define CRTL_PORT 10102
#define NET_PORT 10101
#define FFT_PORT 10103

void control_process(void *arg);
void gsend(int* dst,void* val,int len,int num);
void get_client();
//客户集
static int fft_cli[MAX_CLI]={0};
static int fm_cli[MAX_CLI]={0};
static int fft_cli_num=0;
static int fm_cli_num=0;
//static int ;
