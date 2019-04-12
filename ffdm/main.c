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
	my_addr.sin_port=htons(NET_PORT);
	my_addr.sin_addr.s_addr=INADDR_ANY;
	fft_addr.sin_family=AF_INET;
	fft_addr.sin_port=htons(FFT_PORT);
	fft_addr.sin_addr.s_addr=INADDR_ANY;
	bind(fmsock, (struct sockaddr *)&my_addr, sizeof(my_addr));
	bind(fftsock, (struct sockaddr *)&fft_addr, sizeof(fft_addr));
	listen(fftsock,100);
	listen(fmsock,100);
	ret_thrd1 = pthread_create(&thread1, NULL, (void *)&control_process, (void *)arg);
	fmdst=accept(fmsock,(struct sockaddr*)&their_addr,&sin_size);
	printf("find client %d\n",fmdst);
	fftdst=accept(fftsock,(struct sockaddr*)&fft_their,&sin_size);
	printf("find client %d\n",fftdst);	

	while(arg[0])
	{
//			printf("%d\n",arg[0]);
			if(arg[1]==1)
				ffts(&arg[1],fftdst);
			else if(arg[1]==2)
				fmdm(&arg[1],fmdst);
	}
	printf("bye bye!");
	exit(0);
}
void get_client()
{
	printf("waitting for client \n");
        fmdst=accept(fmsock,(struct sockaddr*)&their_addr,&sin_size);
        printf("find fm client %d\n",fmdst);
        fftdst=accept(fftsock,(struct sockaddr*)&fft_their,&sin_size);
        printf("find fft client %d\n",fftdst);
}
void control_process(void *arg)
{
    pthread_t thread_client;
    // create socket project
    int sockcmd=socket(AF_INET,SOCK_DGRAM,0);
    int thread_cli;
    // set socket attr
    struct sockaddr_in addr;
    addr.sin_family =AF_INET;
    addr.sin_port =htons(CRTL_PORT);
    addr.sin_addr.s_addr=INADDR_ANY;
	struct sockaddr_in cli;
    socklen_t len=sizeof(cli);
    //bind address
    int cmd_ret =bind(sockcmd,(struct sockaddr*)&addr,sizeof(addr));
	int *buf;
	buf=(int *)malloc(8);
    if(0>cmd_ret)
    {
        printf("bind cmd addr failed \n");
        return ;
    }
    printf("start cmd detect loop\n");
	while(((int *)arg)[0])//main loop
    {
        recvfrom(sockcmd,buf,4,0,(struct sockaddr*)&cli,&len);
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
			case 7:
			{
				((int *)arg)[1]=0;
				printf("close all sockets\n");
				sleep(2);
				thread_cli = pthread_create(&thread_client, NULL, (void *)&get_client, (void *)arg);
				break;
			}
		}
    }
    close(sockcmd);
}

