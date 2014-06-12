# Makefile 
#

CC         = g++
DBG_SODIR  = ./debug
DBG_SONAME = liboqr_d.so  
DBG_OBJS   = \
	$(DBG_SODIR)/option.o \
	$(DBG_SODIR)/euro_option.o \
	$(DBG_SODIR)/am_option.o \
	$(DBG_SODIR)/greeks.o  \
	$(DBG_SODIR)/utility.o \
	$(DBG_SODIR)/test_kit.o \
	

REL_SODIR  = ./release
REL_SONAME = liboqr.so  
REL_OBJS   = $(subst $(DBG_SODIR), $(REL_SODIR), $(DBG_OBJS))

INC        = -I/usr/include
DBG_CPPFLAGS = -g -ggdb -DDEBUG -pthread -fPIC $(INC)
REL_CPPFLAGS = -O3 -pthread -fPIC $(INC)
CFLAGS     = -fPIC -fpermissive -shared

all: $(DBG_SODIR)/$(DBG_SONAME) $(REL_SODIR)/$(REL_SONAME)

$(DBG_SODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(DBG_CPPFLAGS)
 
$(DBG_SODIR)/$(DBG_SONAME): $(DBG_OBJS)
	$(CC) -o $@ $^ $(CFLAGS)
	cp -avf $(DBG_SODIR)/$(DBG_SONAME) /usr/local/lib/
	cp -avf *.hpp /usr/local/include/oqr/pricing/

$(REL_SODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(REL_CPPFLAGS)

$(REL_SODIR)/$(REL_SONAME): $(REL_OBJS)
	$(CC) -o $@ $^ $(CFLAGS)
	cp -avf $(REL_SODIR)/$(REL_SONAME) /usr/local/lib/

clean:
	rm -f $(DBG_SODIR)/*.o $(DBG_SODIR)/*.so 
	rm -f $(REL_SODIR)/*.o $(REL_SODIR)/*.so 
	
