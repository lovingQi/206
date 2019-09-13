#ifndef MSERIAL_H
#define MSERIAL_H

#include <stdio.h>
#include <fcntl.h>
#include <assert.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <errno.h>
//用到了两个全局变量：
#define PATHS "/dev/ttyUSB0"

static int fd;
static int ret;

//所需要的函数为：

int uart_open(int fd,const char *pathname);
int uart_config(int fd,int baude,int c_flow, int bits, char parity, int stop);
int safe_read(int fd, char *vptr, size_t len);
int uart_read(int fd, char *r_buf, size_t lenth);//串口读取数据
void uart_write(int fd, void *r_buf, size_t lenth);
int uart_close(int fd);

#endif
