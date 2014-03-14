# Makefile for the socket programming example
#

CC        = g++
DBG_SODIR     = ./debug
DBG_SONAME    = libqr_d.so  
DBG_OBJS      = \
	$(DBG_SODIR)/option.o \
	$(DBG_SODIR)/euro_option.o \
	$(DBG_SODIR)/greeks.o 

REL_SODIR     = ./release
REL_SONAME    = libqr.so  
REL_OBJS      = \
	$(REL_SODIR)/option.o \
	$(REL_SODIR)/euro_option.o \
	$(REL_SODIR)/greeks.o 

INC       = -I/usr/local/include/ql -I/usr/local/boost_1_53_0/include/boost-1_53
DBG_CPPFLAGS  = -g -ggdb -DDEBUG -pthread -fPIC $(INC)
REL_CPPFLAGS  = -O3 -pthread -fPIC $(INC)
CFLAGS    = -fPIC -fpermissive -shared

all: $(DBG_SODIR)/$(DBG_SONAME) $(REL_SODIR)/$(REL_SONAME)

$(DBG_SODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(DBU_CPPFLAGS)
 
$(DBG_SODIR)/$(DBG_SONAME): $(DBG_OBJS)
	$(CC) -o $@ $^ $(CFLAGS)

$(REL_SODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(REL_CPPFLAGS)

$(REL_SODIR)/$(REL_SONAME): $(REL_OBJS)
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -f $(DBG_SODIR)/*.o $(DBG_SODIR)/*.so 
	rm -f $(REL_SODIR)/*.o $(REL_SODIR)/*.so 
	
