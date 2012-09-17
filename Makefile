ARTOOLKIT_INC_DIR = /opt/ARToolKit/include
ARTOOLKIT_LIB_DIR = /opt/ARToolKit/lib

INC_DIR = -I$(ARTOOLKIT_INC_DIR)
INC_DIR += -I/usr/include/gstreamer-0.10
INC_DIR += -I/usr/include/glib-2.0
INC_DIR += -I/usr/lib/x86_64-linux-gnu/glib-2.0/include
INC_DIR += -I/usr/include/libxml2
INC_DIR += -I/usr/X11R6/include
INC_DIR += -I/usr/include/python2.7

LIB_DIR = -L$(ARTOOLKIT_LIB_DIR)
LIB_DIR += -L/usr/X11R6/lib
LIB_DIR += -L/usr/local/lib

LDFLAGS = -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lxml2 -lglib-2.0 -lARgsub -lARvideo -lAR -lpthread -lglut -lGLU -lGL -lXi -lX11 -lm -lgstreamer-0.10 -lboost_python
CPPFLAGS = -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -fPIC -O -pthread -g -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro

SOURCE_FOLDER = src
TEMP_FOLDER = temp
LIB_FOLDER = lib

SOURCES = $(SOURCE_FOLDER)/artoolkitmodule.cpp
TEMP_OBJECT = $(TEMP_FOLDER)/artoolkitmodule.o
LIB_OBJECT = $(LIB_FOLDER)/artoolkit.so

MKDIR = mkdir
RM = rm

all: $(TEMP_FOLDER) $(LIB_FOLDER) $(LIB_OBJECT)

$(TEMP_FOLDER):
	@$(MKDIR) $(TEMP_FOLDER)

$(LIB_FOLDER):
	@$(MKDIR) $(LIB_FOLDER)

$(LIB_OBJECT): $(TEMP_OBJECT)
	$(CXX) $(CPPFLAGS) $(LIB_DIR) $(TEMP_OBJECT) -o $(LIB_OBJECT) $(LDFLAGS)

$(TEMP_OBJECT): $(SOURCES)
	$(CXX) $(CPPFLAGS) $(INC_DIR) -c $(SOURCES) -o $(TEMP_OBJECT)

clean:
	$(warning Cleaning...)
	@$(RM) -rf $(LIB_FOLDER)
	@$(RM) -rf $(TEMP_FOLDER)