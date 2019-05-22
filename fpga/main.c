#include "main.h"
//
int sockfd,dst,fftsock,fftdst;
int sin_size;
struct sockaddr_in my_addr,fft_addr;
struct sockaddr_in their_addr,fft_their;


int main()
{
    void *retval;
    pthread_t thread1;
    int arg[2];
    int ret_thrd1;
	int sta=0;
	arg[0]=1;
	arg[1]=0;
	
	sockfd=socket(AF_INET,SOCK_STREAM,0);
	fftsock=socket(AF_INET,SOCK_STREAM,0);
	
	my_addr.sin_family=AF_INET;
	my_addr.sin_port=htons(NET_PORT);
	my_addr.sin_addr.s_addr=inet_addr(SERVER_ADDR);

	sta=connect(sockfd, (struct sockaddr *)&my_addr, sizeof(my_addr));

	printf("ssslinl %d\n",sta);
	
	fft_addr.sin_family=AF_INET;
	fft_addr.sin_port=htons(FFT_PORT);
	fft_addr.sin_addr.s_addr=inet_addr(SERVER_ADDR);
	sta=connect(fftsock, (struct sockaddr *)&fft_addr, sizeof(fft_addr));

	//listen(sockfd,1);
	ret_thrd1 = pthread_create(&thread1, NULL, (void *)&control_process, (void *)arg);
    printf("start main loop  %d\n",ret_thrd1);

	while(arg[0])
	{
//			printf("%d\n",arg[0]);
			if(arg[1]==1)
				ffts(&arg[1],fftsock);
			else if(arg[1]==2)
				fmdm(&arg[1],sockfd);
	}
	printf("bye bye!");
	exit(0);
}
void control_process(void *arg)
{
    // create socket project
    int sockfd=socket(AF_INET,SOCK_STREAM,0);
    // set socket attr
    struct sockaddr_in addr;
    addr.sin_family =AF_INET;
    addr.sin_port =htons(CRTL_PORT);
    addr.sin_addr.s_addr=inet_addr(SERVER_ADDR);
	struct sockaddr_in cli;
    socklen_t len=sizeof(cli);
    //bind address
    int ret = connect(sockfd,(struct sockaddr*)&addr,sizeof(addr));
    if(0>ret)
    {
        printf("bind addr failed \n");
        return ;
    }
	int *buf;
	buf=(int *)malloc(8);
    printf("start cmd loop\n");
	while(((int *)arg)[0])//main loop
    {
        recv(sockfd,buf,4,0);
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
    close(sockfd);
}

