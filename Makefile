INC_DIR= /opt/ARToolKit/include
LIB_DIR= /opt/ARToolKit/lib

LDFLAG=-pthread -lgstreamer-0.10 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lxml2 -lglib-2.0 -L/usr/X11R6/lib -L/usr/local/lib -L$(LIB_DIR)
LIBS= -lARgsub -lARvideo -lAR -lpthread -lglut -lGLU -lGL -lXi -lX11 -lm -pthread -lgstreamer-0.10 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lxml2 -lglib-2.0
CFLAG= -O -pthread -I/usr/include/gstreamer-0.10 -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/libxml2 -I/usr/X11R6/include -g -I$(INC_DIR) -I/usr/include/python2.7

all: temp lib lib/artoolkitmodule.o

temp:
	mkdir temp

lib:
	mkdir lib

lib/artoolkitmodule.o: temp/artoolkitmodule.o
	g++ -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro temp/artoolkitmodule.o -lboost_python -o lib/artoolkit.so $(LDFLAG) $(LIBS)

temp/artoolkitmodule.o: src/artoolkitmodule.cpp
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -fPIC -I/usr/include/python2.7 -c $(CFLAG) src/artoolkitmodule.cpp -o temp/artoolkitmodule.o

clean:
	rm -f *.o
	rm -rf lib
	rm -rf temp
