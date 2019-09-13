#include "mserial.h"
#include "get_rssi.h"
#include "main.h"

int main()
{
	 data_frame frame;
	 data_frame7 frame7;
     char r_buf[1024];
	 uint16_t a;
     bzero(r_buf,1024);
     fd = uart_open(fd, PATHS);//选择的是ttsY1串口
     if(fd == -1)
     {
         fprintf(stderr,"open failed!\n");
         exit(EXIT_FAILURE);
     }
	 printf("open success1!\n");
     if(uart_config(fd,115200,'h',8,'N',1) == -1)
     {
         fprintf(stderr,"configure failed!\n");
         exit(EXIT_FAILURE);
     }
	 printf("open success2!\n");
	 while (1) 
	 {
		 tcflush(fd,TCIOFLUSH);
		 a=(uint16_t)get_rssi_int();
		 frame_set(&frame,0x55,0xAA,0x7E,0x07,a|0x8000);
//		 frame_set7(&frame,0x55,0XAA,0X7E,0X07,0X80,a); 
		 get_rssi_char(r_buf);
		 uart_write(fd,&(frame.head1),sizeof(data_frame));
//		 uart_write(fd,&(frame7.head1),sizeof(data_frame7));
		 printf("%d\n",a);
		 usleep(200000);
     }
     ret = close(fd);
     if(ret == -1)
     {
         fprintf(stderr, "close failed!\n");
         exit(EXIT_FAILURE);
     }
     exit(EXIT_SUCCESS);
 }
 
 void frame_set(data_frame* src, uint8_t head1,uint8_t head2,uint8_t head3,uint8_t type,uint16_t data)
{
	src->head1=head1;
	src->head2=head2;
	src->head3=head3;
	src->type=type;
	src->data=data;
}
void frame_set7(data_frame7* src, uint8_t head1,uint8_t head2,uint8_t head3,uint8_t type,uint8_t symbol,uint16_t data)
{
        src->head1=head1;
        src->head2=head2;
        src->head3=head3;
        src->type=type;
	src->symbol=symbol;
        src->data=data;
}

