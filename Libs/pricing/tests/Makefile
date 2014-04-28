# Makefile

CC        = g++
DBG_SODIR     = ./debug
DBG_SONAME    = test_option_d 
DBG_OBJS      = \
	$(DBG_SODIR)/test_option.o \

REL_SODIR     = ./release
REL_SONAME    = test_option
REL_OBJS      = \
	$(REL_SODIR)/test_option.o \

INC       = -I/usr/local/include -I/usr/include
DBG_CPPFLAGS  = -g -ggdb -DDEBUG -pthread -fPIC $(INC)
REL_CPPFLAGS  = -O3 -pthread -fPIC $(INC)
DBG_LIBS  = -lQuantLib -loqr_d
REL_LIBS  = -lQuantLib -loqr
CFLAGS    = -fPIC -fpermissive 

all: $(DBG_SODIR)/$(DBG_SONAME) $(REL_SODIR)/$(REL_SONAME)

$(DBG_SODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(DBG_CPPFLAGS)
 
$(DBG_SODIR)/$(DBG_SONAME): $(DBG_OBJS)
	$(CC) -o $@ $^ $(CFLAGS) $(DBG_LIBS)

$(REL_SODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(REL_CPPFLAGS)

$(REL_SODIR)/$(REL_SONAME): $(REL_OBJS)
	$(CC) -o $@ $^ $(CFLAGS) $(REL_LIBS)

clean:
	rm -f $(DBG_SODIR)/*.o $(DBG_SODIR)/* 
	rm -f $(REL_SODIR)/*.o $(REL_SODIR)/* 
	
