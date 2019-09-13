#ifndef GET_RSSI_H
#define GET_RSSI_H
#include "math.h"
#include "stdlib.h"
#include "stdio.h"
#define FILE_PATH "/sys/bus/iio/devices/iio:device0/in_voltage0_rssi" 

int get_rssi_char(char *buffer);
int string_to_int(char *buffer);
int get_rssi_int();
#endif
