#include "main.h"
#include "unistd.h"
//
int fmsock,fmdst,fftsock,fftdst;
int sin_size;
struct sockaddr_in my_addr,fft_addr;
struct sockaddr_in their_addr,fft_their;


int main()
{
	void *retval;
	pthread_t thread1;
	int arg[2];
	int ret_thrd1;
	arg[0]=1;
	arg[1]=0;
	fmsock=socket(AF_INET,SOCK_STREAM,0);
	fftsock=socket(AF_INET,SOCK_STREAM,0);
	my_addr.sin_family=AF_INET;
	my_addr.sin_port=htons(SERVER_SOUND_PORT);
	my_addr.sin_addr.s_addr=SERVER_SOUND_ADDR;
	
	fft_addr.sin_family=AF_INET;
	fft_addr.sin_port=htons(SERVER_SPECTRUM_PORT);
	fft_addr.sin_addr.s_addr=SERVER_SPECTRUM_ADDR;
	
	connect(fmsock, (struct sockaddr *)&my_addr, sizeof(my_addr));
	connect(fftsock, (struct sockaddr *)&fft_addr, sizeof(fft_addr));
	printf("CONNECT STATE : SOUND %d\n",fmsock);
	printf("CONNECT STATE : SPECTRUM %d\n",fftsock);
	ret_thrd1 = pthread_create(&thread1, NULL, (void *)&control_process, (void *)arg);
		

	while(arg[0])
	{
//			printf("%d\n",arg[0]);
			if(arg[1]==1)
				ffts(&arg[1],fftsock);
			else if(arg[1]==2)
				fmdm(&arg[1],fmsock);
	}
	printf("bye bye!");
	exit(0);
}

void control_process(void *arg)
{
    pthread_t thread_client;
    // create socket project
    int sockcmd=socket(AF_INET,SOCK_STREAM,0);
    // set socket attr
    struct sockaddr_in addr;
    addr.sin_family =AF_INET;
    addr.sin_port =htons(SERVER_CMD_PORT);
    addr.sin_addr.s_addr=SERVER_CMD_ADDR;

    //bind address
    int cmd_ret =connect(sockcmd,(struct sockaddr*)&addr,sizeof(addr));
	int *buf;
	buf=(int *)malloc(8);
    if(0>cmd_ret)
    {
        printf("CONNECT CMD SERVER FAILED \n");
        return ;
    }
    printf("CONNECT CMD SERVER SUCCESS\n");
	while(((int *)arg)[0])//main loop
    {
        recv(sockcmd,buf,4,0);
		short cmd,data;
		cmd=*buf>>16;
		data=*buf&0xffff;
		printf("cmd recv :%d %d %d\n",cmd,data,((int *)arg)[0]);
		switch (cmd)
		{
			case 1:
			{
				set_dev_paths("ad9361-phy");
				write_devattr_int("out_altvoltage0_RX_LO_frequency", data*100000+88000000);//data*0.1M +88M
				break;//set fm freq
			}
			case 3:((int *)arg)[1]=2;break;//start fmod 
			case 4:((int *)arg)[1]=1;break;//start fft
			case 5:((int *)arg)[1]=0;send(fftdst,"\xaa\xbb\xcc\xdd",4,0);break;//kill sub
			case 6:((int *)arg)[0]=0;exit(0);break;//kill all
		}
    }
    close(sockcmd);
}

