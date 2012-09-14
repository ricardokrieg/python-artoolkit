#include <boost/python.hpp>

#include <AR/gsub.h>
#include <AR/video.h>
#include <AR/param.h>
#include <AR/ar.h>

namespace BP = boost::python;

class ARToolKit {
    public:
        ARToolKit(void) {
            char vconf[] = "v4l2src device=/dev/video0 ! ffmpegcolorspace ! capsfilter caps=video/x-raw-rgb,bpp=24 ! identity name=artoolkit ! fakesink";
            if(arVideoOpen( vconf ) < 0) exit(0);

            if(arVideoInqSize(&this->xsize, &this->ysize) < 0) exit(0);

            ARParam  wparam, cparam;
            char cparam_name[] = "Data/camera_para.dat";
            if(arParamLoad(cparam_name, 1, &wparam) < 0) {
                printf("Camera parameter load error !!\n");
                exit(0);
            }
            arParamChangeSize(&wparam, this->xsize, this->ysize, &cparam);
            arInitCparam(&cparam);
            printf("*** Camera Parameter ***\n");
            arParamDisp(&cparam);
        }

        void close(void) {
            arVideoClose();
        }

        BP::tuple get_size(void) {
            BP::tuple ret = BP::make_tuple(this->xsize, this->ysize);

            return ret;
        }

    private:
        int xsize, ysize;
};

BOOST_PYTHON_MODULE(artoolkit) {
    using namespace boost::python;

    class_<ARToolKit>("ARToolKit", init<>())
        .def("close", &ARToolKit::close)

        .add_property("size", &ARToolKit::get_size);
    ;
}