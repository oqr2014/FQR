# Makefile 
#

CC        = g++
DBG_DLODIR     = ./debug
DBG_DLONAME    = liboqr_py_d.so  
DBG_OBJS      = \
	$(DBG_DLODIR)/py_export.o  \
	$(DBG_DLODIR)/py_greeks.o  \
	$(DBG_DLODIR)/py_option.o  \
	$(DBG_DLODIR)/py_euro_option.o  \
	$(DBG_DLODIR)/py_am_option.o  \
	$(DBG_DLODIR)/py_utility.o  \

REL_DLODIR     = ./release
REL_DLONAME    = liboqr_py.so  
REL_OBJS      = \
	$(REL_DLODIR)/py_export.o  \
	$(REL_DLODIR)/py_greeks.o  \
	$(DBG_DLODIR)/py_option.o  \
	$(DBG_DLODIR)/py_euro_option.o  \
	$(REL_DLODIR)/py_am_option.o  \
	$(REL_DLODIR)/py_utility.o  \

INC       = -I/usr/local/boost_1_53_0/include/boost-1_53 -I/usr/include/python2.7
DBG_CPPFLAGS  = -g -ggdb -DDEBUG -pthread -fPIC $(INC)
LIBPATH = -L/usr/local/boost_1_53_0/lib -L/usr/local/lib -L/usr/lib/python2.7/config
DBG_LIBS      = $(LIBPATH) -lboost_python-gcc46-mt-d-1_53 -lQuantLib -loqr_d -lpython2.7
REL_CPPFLAGS  = -O3 -pthread -fPIC $(INC)
REL_LIBS      = $(LIBPATH) -lboost_python-gcc46-mt-1_53 -lQuantLib -loqr -lpython2.7
CFLAGS    = -fpermissive -shared -rdynamic

all: $(DBG_DLODIR)/$(DBG_DLONAME) $(REL_DLODIR)/$(REL_DLONAME)

$(DBG_DLODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(DBG_CPPFLAGS)
 
$(DBG_DLODIR)/$(DBG_DLONAME): $(DBG_OBJS)
	$(CC) -o $@ $^ $(CFLAGS) $(DBG_LIBS)
	cp -avf $(DBG_DLODIR)/$(DBG_DLONAME) /usr/local/lib/

$(REL_DLODIR)/%.o: %.cpp 
	$(CC) -c -o $@ $< $(REL_CPPFLAGS)

$(REL_DLODIR)/$(REL_DLONAME): $(REL_OBJS)
	$(CC) -o $@ $^ $(CFLAGS) $(REL_LIBS)
	cp -avf $(REL_DLODIR)/$(REL_DLONAME) /usr/local/lib/

clean:
	rm -f $(DBG_DLODIR)/*.o $(DBG_DLODIR)/*.so 
	rm -f $(REL_DLODIR)/*.o $(REL_DLODIR)/*.so 
	
