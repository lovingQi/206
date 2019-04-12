CC := gcc

CFLAG += -lm
CFLAG += -lfftw3
CFLAG += -liio
CFLAG += -lpthread
#CFLAG += -O2
objs += main.o
objs += ad9365.o
objs += iio_fm_radio.o
objs += iio_utils.o
target = fmdc 

$(target): $(objs)
	$(CC) $^ $(CFLAG) -o $@

main.o: main.c
	$(CC) -c $^ $(CFLAG) -o $@
ad9365.o: ad9365.c
	$(CC) -c $^ $(CFLAG) -o $@
iio_fm_radio.o: iio_fm_radio.c 
	$(CC) -c $^ $(CFLAG) -o $@
iio_utils.o: iio_utils.c
	$(CC) -c $^ $(CFLAG) -o $@

clean:
	rm *.o
	rm fmdc

