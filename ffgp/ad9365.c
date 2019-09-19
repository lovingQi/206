/*
 * libiio - AD9361 IIO streaming example
 *
 * Copyright (C) 2014 IABG mbH
 * Author: Michael Feilen <feilen_at_iabg.de>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 **/
#include "ad9365.h"
/* RX is input, TX is output */

/* static scratch mem for strings */
static char tmpstr[64];

/* IIO structs required for streaming */
static struct iio_context *ctx   = NULL;
static struct iio_channel *rx0_i = NULL;
static struct iio_channel *rx0_q = NULL;
static struct iio_channel *tx0_i = NULL;
static struct iio_channel *tx0_q = NULL;
static struct iio_buffer  *rxbuf = NULL;
static struct iio_buffer  *txbuf = NULL;

static bool stop;

/* cleanup and exit */
static void iio_shutdown()
{
	printf("* Destroying buffers\n");
	if (rxbuf) { iio_buffer_destroy(rxbuf); }

	printf("* Disabling streaming channels\n");
	if (rx0_i) { iio_channel_disable(rx0_i); }
	if (rx0_q) { iio_channel_disable(rx0_q); }

	printf("* Destroying context\n");
	if (ctx) { iio_context_destroy(ctx); }
	//exit(0);
}

static void handle_sig(int sig)
{
	printf("Waiting for process to finish...\n");
	stop = true;
}

/* check return value of attr_write function */
static void errchk(int v, const char* what) {
	 if (v < 0) { fprintf(stderr, "Error %d writing to channel \"%s\"\nvalue may not be supported.\n", v, what); iio_shutdown(); }
}

/* write attribute: long long int */
static void wr_ch_lli(struct iio_channel *chn, const char* what, long long val)
{
	errchk(iio_channel_attr_write_longlong(chn, what, val), what);
}

/* write attribute: string */
static void wr_ch_str(struct iio_channel *chn, const char* what, const char* str)
{
	errchk(iio_channel_attr_write(chn, what, str), what);
}

/* helper function generating channel names */
static char* get_ch_name(const char* type, int id)
{
	snprintf(tmpstr, sizeof(tmpstr), "%s%d", type, id);
	return tmpstr;
}

/* returns ad9361 phy device */
static struct iio_device* get_ad9361_phy(struct iio_context *ctx)
{
	struct iio_device *dev =  iio_context_find_device(ctx, "ad9361-phy");
	ASSERT(dev && "No ad9361-phy found");
	return dev;
}

/* finds AD9361 streaming IIO devices */
static bool get_ad9361_stream_dev(struct iio_context *ctx, enum iodev d, struct iio_device **dev)
{
	switch (d) {
	case TX: *dev = iio_context_find_device(ctx, "cf-ad9361-dds-core-lpc"); return *dev != NULL;
	case RX: *dev = iio_context_find_device(ctx, "cf-ad9361-lpc");  return *dev != NULL;
	default: ASSERT(0); return false;
	}
}

/* finds AD9361 streaming IIO channels */
static bool get_ad9361_stream_ch(struct iio_context *ctx, enum iodev d, struct iio_device *dev, int chid, struct iio_channel **chn)
{
	*chn = iio_device_find_channel(dev, get_ch_name("voltage", chid), d == TX);
	if (!*chn)
		*chn = iio_device_find_channel(dev, get_ch_name("altvoltage", chid), d == TX);
	return *chn != NULL;
}

/* finds AD9361 phy IIO configuration channel with id chid */
static bool get_phy_chan(struct iio_context *ctx, enum iodev d, int chid, struct iio_channel **chn)
{
	switch (d) {
	case RX: *chn = iio_device_find_channel(get_ad9361_phy(ctx), get_ch_name("voltage", chid), false); return *chn != NULL;
	case TX: *chn = iio_device_find_channel(get_ad9361_phy(ctx), get_ch_name("voltage", chid), true);  return *chn != NULL;
	default: ASSERT(0); return false;
	}
}

/* finds AD9361 local oscillator IIO configuration channels */
static bool get_lo_chan(struct iio_context *ctx, enum iodev d, struct iio_channel **chn)
{
	switch (d) {
	 // LO chan is always output, i.e. true
	case RX: *chn = iio_device_find_channel(get_ad9361_phy(ctx), get_ch_name("altvoltage", 0), true); return *chn != NULL;
	case TX: *chn = iio_device_find_channel(get_ad9361_phy(ctx), get_ch_name("altvoltage", 1), true); return *chn != NULL;
	default: ASSERT(0); return false;
	}
}

/* applies streaming configuration through IIO */
bool cfg_ad9361_streaming_ch(struct iio_context *ctx, struct stream_cfg *cfg, enum iodev type, int chid)
{
	struct iio_channel *chn = NULL;

	// Configure phy and lo channels
	printf("* Acquiring AD9361 phy channel %d\n", chid);
	if (!get_phy_chan(ctx, type, chid, &chn)) {	return false; }
	wr_ch_str(chn, "rf_port_select",     cfg->rfport);
	wr_ch_lli(chn, "rf_bandwidth",       cfg->bw_hz);
	wr_ch_lli(chn, "sampling_frequency", cfg->fs_hz);

	// Configure LO channel
	printf("* Acquiring AD9361 %s lo channel\n", type == TX ? "TX" : "RX");
	if (!get_lo_chan(ctx, type, &chn)) { return false; }
	wr_ch_lli(chn, "frequency", cfg->lo_hz);
	return true;
}

/* simple configuration and streaming */

/*

函数 ffts
int *life 进程管理 1 进入循环 0 退出循环结束子程序
int *dst  tcp socket
int cnum  已连接客户端数目

*/

int ffts (int *life,int* dst,int cnum)
{
	
	ssize_t nbytes_rx;
	char *p_dat, *p_end;
	ptrdiff_t p_inc;
	unsigned int i=0;
	fftw_complex *in, *out;  	//fft 数据缓存区
	fftw_plan p; 			//fft计划
	// Streaming devices
	struct iio_device *rx;		//iio设备
	// RX and TX sample counters
	// Stream configurations
	struct stream_cfg rxcfg;
	//
	in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);  
	out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
	p = fftw_plan_dft_1d(N,in,out, FFTW_FORWARD, FFTW_ESTIMATE);
	// Listen to ctrl+c and ASSERT
	signal(SIGINT, handle_sig);

	// RX stream config
	rxcfg.bw_hz = MHZ(20);   // 2 MHz rf bandwidth
	rxcfg.fs_hz = MHZ(40);   // 2.5 MS/s rx sample rate
	rxcfg.lo_hz = MHZ(88); // 2.5 GHz rf frequency
	rxcfg.rfport = "A_BALANCED"; // port A (select for rf freq.)


	printf("* Acquiring IIO context\n");
	ASSERT((ctx = iio_create_default_context()) && "No context");
	ASSERT(iio_context_get_devices_count(ctx) > 0 && "No devices");

	printf("* Acquiring AD9361 streaming devices\n");
	ASSERT(get_ad9361_stream_dev(ctx, RX, &rx) && "No rx dev found");

	printf("* Configuring AD9361 for streaming\n");
	ASSERT(cfg_ad9361_streaming_ch(ctx, &rxcfg, RX, 0) && "RX port 0 not found");

	printf("* Initializing AD9361 IIO streaming channels\n");
	ASSERT(get_ad9361_stream_ch(ctx, RX, rx, 0, &rx0_i) && "RX chan i not found");
	ASSERT(get_ad9361_stream_ch(ctx, RX, rx, 1, &rx0_q) && "RX chan q not found");
	printf("* Enabling IIO streaming channels\n");
	iio_channel_enable(rx0_i);
	iio_channel_enable(rx0_q);

	printf("* Creating non-cyclic IIO buffers with 8192 iS\n");
	rxbuf = iio_device_create_buffer(rx, N, false);
	if (!rxbuf) {
		perror("Could not create RX buffer");
		iio_shutdown();
	}

	printf("* Starting IO streaming (press CTRL+C to cancel)\n");
	while (*life)//主循环
	{
		nbytes_rx = iio_buffer_refill(rxbuf);//从ad9361读取数据填入接收缓冲区
		if (nbytes_rx < 0) { printf("Error refilling buf %d\n",(int) nbytes_rx); iio_shutdown(); }
		// READ: Get pointers to RX buf and read IQ from RX buf port 0
		p_inc = iio_buffer_step(rxbuf);
		p_end = iio_buffer_end(rxbuf);
		i=0;
		
		//将数据存入fft输入缓存
		for (p_dat = (char *)iio_buffer_first(rxbuf, rx0_i); p_dat < p_end; p_dat += p_inc) {
			//  I and Q
			in[i][0] = (double)((int16_t*)p_dat)[0];
			in[i][1] = (double)((int16_t*)p_dat)[1];
			i++;
		}
		fftw_execute(p);//执行fft
		
		int head;
		static int temp_int;
		double temp_double;
		head=0xfedcba00;//同步帧，表示上一帧数据已发送完毕，开始发送下一帧数据。
		gsend(dst,&head,4,cnum);
		for(i = 0;i < N;i++)  
		{  
			temp_double=sqrt(out[i][0]*out[i][0]+out[i][1]*out[i][1]);//取绝对值
			temp_int=(int)(temp_double*100);
			gsend(dst,&temp_int,4,cnum);//群发程序目前只支持单客户端不断重连。

		}
	}
	//释放缓冲区
	fftw_free(in);
	fftw_free(out);
	//销毁fft计划
	fftw_destroy_plan(p);
	//关闭iio设备
	iio_shutdown();
	return 0;
} 

