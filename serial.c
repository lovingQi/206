

#include "mserial.h"
 


//打开串口：

int uart_open(int fd,const char *pathname)
{
    assert(pathname);//检测串口路径是否存在
    fd = open(pathname,O_RDWR|O_NOCTTY|O_NDELAY);//以只读形式、不将此终端作为此进程的终端控制器、非阻塞的形式打开串口
    if(fd == -1)
    {
        perror("uart open failed!");
        return -1;
    }
    if(fcntl(fd,F_SETFL,0)<0)//设置串口非阻塞，因为这里是以非阻塞形式打开的，所以第三个参数为0，后面会详细介绍fcntl函数
    {
        perror("fcntl failed!");
        return -1;
    }
    return fd;
}


int uart_config(int fd,int baude,int c_flow, int bits, char parity, int stop)
{
    struct termios uart;
    if(tcgetattr(fd,&uart)!=0)
    {
        perror("tcgetattr failed!");
        return -1;
    }
    bzero(&uart,sizeof(struct termios));
    cfsetispeed(&uart,B115200);
    cfsetospeed(&uart,B115200);
	//uart.c_cflag |= CRTSCTS;
	uart.c_cflag |= CS8;
	uart.c_iflag &= ~ISTRIP;
	
     
   if(tcsetattr(fd,TCSANOW,&uart)<0)//激活配置，失败返回-1
    {
        return -1;
    }
    uart.c_cflag |= CREAD;
    uart.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG );//使串口工作在原始模式下
    uart.c_cc[VTIME] = 10;//设置等待时间为0
    uart.c_cc[VMIN] = 10;//设置最小接受字符为1
    tcflush(fd,TCIFLUSH);//清空输入缓冲区
    if(tcsetattr(fd,TCSANOW,&uart)<0)//激活配置
    {
        perror("tcgetattr failed!");
        return -1;
    }
    return 0;
}

int safe_read(int fd, char *vptr, size_t len)
{
    size_t left;
    left = len;
    ssize_t nread;
    char *ptr;
    ptr = vptr;
    while(left > 0)
    {
        if ((nread = read(fd, ptr, left)) < 0)
        {
                nread = 0;
                break;
        }
        left -= nread;//read成功后，剩余要读取的字节自减
        ptr += nread;//指针向后移，避免后读到的字符覆盖先读到的字符
    }
    return (len - left);
}

int uart_read(int fd, char *r_buf, size_t lenth)
{
    fd_set rfds;
    struct timeval time;
    ssize_t cnt = 0;
    /*将读文件描述符加入描述符集合*/

        cnt = safe_read(fd, r_buf, lenth);
        if(cnt == -1)
        {
            fprintf(stderr, "safe read failed!\n");
            return -1;
        }
        return cnt;
}


void uart_write(int fd, void *r_buf, size_t lenth)
{
    char *ptr;
	int a;
    ptr = r_buf;
        if (write(fd, r_buf, lenth) < 0)
        {
                printf("serial write failed!\n");
                
        }
//	write(fd,"\x00\x00\xff\xff",4);
	for(a=0;a<lenth;a++)
	{
//		printf("write :%x\n",ptr[a]);
	//	write(fd, ptr[a], 1);
	}
}



int uart_close(int fd)
{
    assert(fd);//assert先检查文件描述符是否存在
    close(fd);
    return 0;
}



