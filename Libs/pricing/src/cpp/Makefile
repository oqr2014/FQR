# Makefile for the socket programming example
#

CC        = g++
SODIR     = ./debug
SONAME    = libqr_d.so  
OBJS      = \
	$(SODIR)/option.o \
	$(SODIR)/euro_option.o \
	$(SODIR)/greeks.o 

INC       = -I/usr/local/include/ql -I/usr/local/boost_1_53_0/include/boost-1_53
CPPFLAGS  = -g -ggdb -DDEBUG -pthread -fPIC $(INC)
CFLAGS    = -fPIC -fpermissive -shared

all: $(SODIR)/$(SONAME)

$(SODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(CPPFLAGS)
 
$(SODIR)/$(SONAME): $(OBJS)
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -f $(SODIR)/*.o $(SODIR)/*.so 
