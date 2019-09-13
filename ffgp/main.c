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
	pthread_t thread_command;
	pthread_t thread_client;
    int thread_cli;
	int arg[2];
	int thread_cmd;
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
	listen(fftsock,MAX_CLI);
	listen(fmsock,MAX_CLI);
	
	thread_cmd = pthread_create(&thread_command, NULL, (void *)&control_process, (void *)arg);
	thread_cli = pthread_create(&thread_client, NULL, (void *)&get_client, (void *)arg);
	

	while(arg[0])
	{

			if(arg[1]==1)
				ffts(&arg[1],fft_cli,fft_cli_num);
			else if(arg[1]==2)
				fmdm(&arg[1],fm_cli,fm_cli_num);
	}
	printf("bye bye!");
	exit(0);
}
void gsend(int* dst,void* val,int len,int num)
{
	int i;
	int ret;
	for(i=0;i<num;i++)
	{
		if(dst[i])
		{
			ret=send(dst[i],val,len,0);
			if(ret<0)
				dst[i]=0;
		}
		
	}
}

void get_client()
{
	while (1&&fft_cli_num<MAX_CLI&&fm_cli_num<MAX_CLI)
	{
		printf("waitting for other client %d  %d\n",fft_cli_num,fm_cli_num);
        fmdst=accept(fmsock,(struct sockaddr*)&their_addr,&sin_size);
		if(fmdst)
		{
			fm_cli[fm_cli_num++]=fmdst;
			printf("find fm client %d\n",fmdst);
		}
        fftdst=accept(fftsock,(struct sockaddr*)&fft_their,&sin_size);
		if(fftdst)
		{
			fft_cli[fft_cli_num++]=fftdst;
			printf("find fft client %d\n",fftdst);
		}
	}
	printf("\nreach max client....exit\n");
	exit(0);
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
				write_devattr_int("out_altvoltage0_RX_LO_frequency", data*100000+70000000);//data*0.1M +88M
				break;//set fm freq
			}
			case 3:fm_cli_num>0?((int *)arg)[1]=2:printf("no client");break;//start fmod 
			case 4:fft_cli_num>0?((int *)arg)[1]=1:printf("no client");break;//start fft
			case 5:((int *)arg)[1]=0;gsend(fft_cli,"\xaa\xbb\xcc\xdd",4,fft_cli_num);break;//kill sub
			case 6:((int *)arg)[0]=0;exit(0);break;//kill all
			case 7:
			{
				
				((int *)arg)[1]=0;
				printf("reserve option!!\n");
				break;
			}
		}
    }
    close(sockcmd);
}

