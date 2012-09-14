INC_DIR= /opt/ARToolKit/include
LIB_DIR= /opt/ARToolKit/lib

LDFLAG=-pthread -lgstreamer-0.10 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lxml2 -lglib-2.0 -L/usr/X11R6/lib -L/usr/local/lib -L$(LIB_DIR)
LIBS= -lARgsub -lARvideo -lAR -lpthread -lglut -lGLU -lGL -lXi -lX11 -lm -pthread -lgstreamer-0.10 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lxml2 -lglib-2.0
CFLAG= -O -pthread -I/usr/include/gstreamer-0.10 -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/libxml2 -I/usr/X11R6/include -g -I$(INC_DIR) -I/usr/include/python2.7

all: build/temp.linux-x86_64-2.7 build/lib.linux-x86_64-2.7 build/lib.linux-x86_64-2.7/artoolkitmodule.o

build/temp.linux-x86_64-2.7:
	mkdir -p build/temp.linux-x86_64-2.7

build/lib.linux-x86_64-2.7:
	mkdir -p build/lib.linux-x86_64-2.7

build/lib.linux-x86_64-2.7/artoolkitmodule.o: build/temp.linux-x86_64-2.7/artoolkitmodule.o
	g++ -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro build/temp.linux-x86_64-2.7/artoolkitmodule.o -lboost_python -o build/lib.linux-x86_64-2.7/artoolkit.so $(LDFLAG) $(LIBS)

build/temp.linux-x86_64-2.7/artoolkitmodule.o: artoolkitmodule.cpp
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -fPIC -I/usr/include/python2.7 -c $(CFLAG) artoolkitmodule.cpp -o build/temp.linux-x86_64-2.7/artoolkitmodule.o

clean:
	rm -f *.o

allclean:
	rm -f *.o
	rm -f Makefile
