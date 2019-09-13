#ifndef MAIN_H
#define MAIN_H

#include "mserial.h"
#include "get_rssi.h"
#include "stdlib.h"
#include "stdint.h"

typedef struct {
	uint8_t head1;
	uint8_t head2;
	uint8_t head3;
	uint8_t type;
	uint16_t data;
}data_frame;
typedef struct {
        uint8_t head1;
        uint8_t head2;
        uint8_t head3;
        uint8_t type;
	uint8_t symbol;
        uint16_t data;
}data_frame7;

void frame_set7(data_frame7* src, uint8_t head1,uint8_t head2,uint8_t head3,uint8_t type,uint8_t symbol,uint16_t data);
void frame_set(data_frame* src, uint8_t head1,uint8_t head2,uint8_t head3,uint8_t type,uint16_t data);

#endif

