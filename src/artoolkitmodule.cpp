#include <boost/python.hpp>

#include <GL/glut.h>
#include <GL/glext.h>

#include <AR/gsub.h>
#include <AR/video.h>
#include <AR/param.h>
#include <AR/ar.h>

namespace BP = boost::python;

class ARToolKit {
    public:
        ARToolKit(void) {
            char vconf[] = "v4l2src device=/dev/video0 ! video/x-raw-yuv,width=640,height=480 ! ffmpegcolorspace ! capsfilter caps=video/x-raw-rgb,bpp=24 ! identity name=artoolkit ! fakesink";
            // char vconf[] = "v4l2src device=/dev/video0 ! ffmpegcolorspace ! capsfilter caps=video/x-raw-rgb,bpp=24 ! identity name=artoolkit ! fakesink";
            if (arVideoOpen( vconf ) < 0) exit(0);

            if (arVideoInqSize(&this->xsize, &this->ysize) < 0) exit(0);

            char cparam_name[] = "Data/camera_para.dat";
            ARParam wparam, cparam;
            if (arParamLoad(cparam_name, 1, &wparam) < 0) {
                printf("Camera parameter load error !!\n");
                exit(0);
            }

            arParamChangeSize(&wparam, this->xsize, this->ysize, &cparam);
            arInitCparam(&cparam);
            printf("*** Camera Parameter ***\n");
            arParamDisp(&cparam);

            char patt_name[] = "Data/patt.hiro";
            if ((this->patt_id=arLoadPatt(patt_name)) < 0) {
                printf("pattern load error !!\n");
                exit(0);
            }

            static ARParam  gCparam;
            gCparam = cparam;
            for (int i = 0; i < 4; ++i) {
                gCparam.mat[1][i] = (gCparam.ysize-1)*(gCparam.mat[2][i]) - gCparam.mat[1][i];
            }
            argConvGLcpara( &gCparam, AR_GL_CLIP_NEAR, AR_GL_CLIP_FAR, this->gl_cpara );

            arVideoCapStart();

            this->count = 0;
            this->patt_center[0] = 0.0;
            this->patt_center[1] = 0.0;

            this->init();
        }

        void init() {
            glMatrixMode(GL_PROJECTION);
            glLoadIdentity();
            gluPerspective(100, 1, 0.5, 500);
            glMatrixMode(GL_MODELVIEW);
            glLoadIdentity();
            gluLookAt(0, 0, 100, 0, 0, 0, 0, 1, 0);
        }

        void update() {
            ARMarkerInfo *marker_info;
            int marker_num;
            int j, k;

            if ((this->dataPtr = (ARUint8 *)arVideoGetImage()) == NULL) {
                arUtilSleep(2);
                return;
            }
            if (count == 0) arUtilTimerReset();
            count++;

            if (arDetectMarker(this->dataPtr, this->thresh, &marker_info, &marker_num) < 0) {
                this->close();
                exit(0);
            }

            arVideoCapNext();

            k = -1;
            for (j = 0; j < marker_num; j++) {
                if (this->patt_id == marker_info[j].id) {
                    if (k == -1) k = j;
                    else if (marker_info[k].cf < marker_info[j].cf) k = j;
                }
            }
            if (k == -1) return;

            arGetTransMat(&marker_info[k], this->patt_center, this->patt_width, this->patt_trans);
            argConvGlpara(this->patt_trans, this->gl_para);
        }

        void draw2d() {
            argDrawMode2D();
            argDispImage(this->dataPtr, 0, 0);
        }

        void draw3d(void) {
            glMatrixMode(GL_MODELVIEW);
            glLoadIdentity();

            glMatrixMode(GL_PROJECTION);
            glLoadMatrixd(this->gl_cpara);

            glClear(GL_DEPTH_BUFFER_BIT);
            glClearDepth(1.0);

            glMatrixMode(GL_MODELVIEW);
            glLoadMatrixd(this->gl_para);
        }

        void close(void) {
            arVideoCapStop();
            arVideoClose();
        }

        BP::tuple get_size(void) {
            BP::tuple ret = BP::make_tuple(this->xsize, this->ysize);

            return ret;
        }

        BP::tuple get_pos(void) {
            BP::tuple ret = BP::make_tuple(this->patt_trans[0][3]+this->xsize/2, this->patt_trans[1][3]+this->ysize/2);

            return ret;
        }

        BP::tuple get_matrix(void) {
            BP::tuple ret_0 = BP::make_tuple(this->patt_trans[0][0], this->patt_trans[0][1], this->patt_trans[0][2], this->patt_trans[0][3]);
            BP::tuple ret_1 = BP::make_tuple(this->patt_trans[1][0], this->patt_trans[1][1], this->patt_trans[1][2], this->patt_trans[1][3]);
            BP::tuple ret_2 = BP::make_tuple(this->patt_trans[2][0], this->patt_trans[2][1], this->patt_trans[2][2], this->patt_trans[2][3]);

            BP::tuple ret = BP::make_tuple(ret_0, ret_1, ret_2);

            return ret;
        }

        BP::list get_gl_matrix(void) {
            BP::list ret;
            for (int i=0; i < 16; ++i) {
                ret.append(this->gl_para[i]);
            }

            return ret;
        }

        BP::list get_frame(void) {
            BP::list ret;

            for (unsigned int i=0; i<(this->xsize*this->ysize*3); i++) {
                ret.append(this->dataPtr[i]);
            }

            return ret;
        }

    private:
        int xsize, ysize;
        int patt_id;
        int count;
        static const int thresh = 100;
        static const double patt_width = 80.0;
        double patt_center[2];
        double patt_trans[3][4];
        double gl_para[16], gl_cpara[16];
        ARUint8 *dataPtr;
};

BOOST_PYTHON_MODULE(artoolkit) {
    using namespace boost::python;

    class_<ARToolKit>("ARToolKit", init<>())
        .def("update", &ARToolKit::update)
        .def("draw2d", &ARToolKit::draw2d)
        .def("draw3d", &ARToolKit::draw3d)
        .def("close", &ARToolKit::close)

        .add_property("size", &ARToolKit::get_size)
        .add_property("pos", &ARToolKit::get_pos)
        .add_property("matrix", &ARToolKit::get_matrix)
        .add_property("frame", &ARToolKit::get_frame);
    ;
}