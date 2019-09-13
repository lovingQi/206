#include "get_rssi.h"


#include "get_rssi.h"

int get_rssi_char(char *buffer)
{
	//char buffer[10]={0};
	FILE *fp;
	fp=fopen(FILE_PATH,"r");
	if(NULL==fp)
	{
		printf("fail to open rssi file!\n");
		return 0;
	}
	else
	{	
		fgets(buffer,10,fp);
		buffer[9]='\n';
		fclose(fp);
		return 1;
	}
}

int string_to_int(char *buffer)
{
	int a;
	double b;
	int size,power;
	
	size=strlen(buffer)-6;
	power=size+1;
	b=0;
	//printf("%d\n%s\n",size,buffer);	
	for(a=0;;a++)
	{
		if(buffer[a]!='.')
		{
			if(buffer[a]==' ')
				break;
			b+=pow10(power--)*(buffer[a]-'0');		
		}
	}
	if(a==5)
		b/=10;
//	printf("%d\n%s\n",a,buffer);
	return (int)b;
}

int get_rssi_int()
{
	char buffer[10]={0};
	FILE *fp;
	fp=fopen(FILE_PATH,"r");
	if(NULL==fp)
	{
		printf("fail to open rssi file!\n");
		return 0;
	}
	else
	{
		memset(buffer,0,10);	
		fgets(buffer,10,fp);
		fclose(fp);
		return string_to_int(buffer);;
	}
}

