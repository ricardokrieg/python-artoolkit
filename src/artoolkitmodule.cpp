#include <boost/python.hpp>

#include <GL/glut.h>
#include <GL/glext.h>

#include <AR/gsub.h>
#include <AR/video.h>
#include <AR/param.h>
#include <AR/ar.h>

namespace BP = boost::python;

int xsize, ysize;
double gl_cpara[16];
ARUint8 *dataPtr;

void artoolkit_init(void) {
    char vconf[] = "v4l2src device=/dev/video1 ! video/x-raw-yuv,width=1280,height=720 ! ffmpegcolorspace ! capsfilter caps=video/x-raw-rgb,bpp=24 ! identity name=artoolkit ! fakesink";
    if (arVideoOpen( vconf ) < 0) exit(0);

    if (arVideoInqSize(&xsize, &ysize) < 0) exit(0);

    char cparam_name[] = "Data/hd.dat";
    ARParam wparam, cparam;
    if (arParamLoad(cparam_name, 1, &wparam) < 0) {
        printf("Camera parameter load error !!\n");
        exit(0);
    }

    arParamChangeSize(&wparam, xsize, ysize, &cparam);
    arInitCparam(&cparam);
    printf("*** Camera Parameter ***\n");
    arParamDisp(&cparam);

    static ARParam  gCparam;
    gCparam = cparam;
    for (int i = 0; i < 4; ++i) {
        gCparam.mat[1][i] = (gCparam.ysize-1)*(gCparam.mat[2][i]) - gCparam.mat[1][i];
    }
    argConvGLcpara( &gCparam, AR_GL_CLIP_NEAR, AR_GL_CLIP_FAR, gl_cpara );

    arVideoCapStart();

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(100, 1, 0.5, 500);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(0, 0, 100, 0, 0, 0, 0, 1, 0);
}

void artoolkit_next_frame(void) {
    if ((dataPtr = (ARUint8 *)arVideoGetImage()) == NULL) {
        arUtilSleep(2);
        return;
    }
    
    arVideoCapNext();
}

void artoolkit_load_projection_matrix(void) {
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glMatrixMode(GL_PROJECTION);
    glLoadMatrixd(gl_cpara);

    glClearDepth( 1.0 );
    glClear(GL_DEPTH_BUFFER_BIT);
    glDepthFunc(GL_LEQUAL);
}

BP::tuple artoolkit_size(void) {
    BP::tuple ret = BP::make_tuple(xsize, ysize);

    return ret;
}

void artoolkit_close(void) {
    arVideoCapStop();
    arVideoClose();
}

BP::list artoolkit_frame(void) {
    BP::list ret;

    for (unsigned int i=0; i<(xsize*ysize*3); i++) {
        ret.append(dataPtr[i]);
    }

    return ret;
}

class ARToolKit {
    public:
        ARToolKit(const std::string patt_name) {
            if ((this->patt_id=arLoadPatt(patt_name.c_str())) < 0) {
                printf("pattern load error !!\n");
                exit(0);
            }

            this->count = 0;
            this->patt_center[0] = 0.0;
            this->patt_center[1] = 0.0;
            this->visible = false;
            this->thresh = 100;
            this->patt_width = 80.0;
        }

        void update(void) {
            ARMarkerInfo *marker_info;
            int marker_num;

            if (this->count == 0) arUtilTimerReset();
            this->count++;

            if (arDetectMarker(dataPtr, this->thresh, &marker_info, &marker_num) < 0) {
                artoolkit_close();
                exit(0);
            }

            this->visible = true;
            int k = -1;
            for (int j = 0; j < marker_num; j++) {
                if (this->patt_id == marker_info[j].id) {
                    if (k == -1) k = j;
                    else if (marker_info[k].cf < marker_info[j].cf) k = j;
                }
            }

            if (k == -1) {
                this->visible = false;
                return;
            }

            arGetTransMat(&marker_info[k], this->patt_center, this->patt_width, this->patt_trans);
            argConvGlpara(this->patt_trans, this->gl_para);
        }

        void load_matrix(void) {
            glMatrixMode(GL_MODELVIEW);
            glLoadMatrixd(this->gl_para);
        }

        bool is_visible(void) {
            return visible;
        }

    private:
        int patt_id;
        int thresh;
        double patt_width;
        double patt_center[2];
        double patt_trans[3][4];
        bool visible;
        double gl_para[16];
        int count;
};

BOOST_PYTHON_MODULE(artoolkit) {
    using namespace boost::python;

    def("artoolkit_init", &artoolkit_init);
    def("artoolkit_close", &artoolkit_close);
    def("artoolkit_size", &artoolkit_size);
    def("load_projection_matrix", &artoolkit_load_projection_matrix);
    def("next_frame", &artoolkit_next_frame);

    def("artoolkit_frame", &artoolkit_frame);

    class_<ARToolKit>("ARToolKit", init<const std::string>())
        .def("update", &ARToolKit::update)
        .def("load_matrix", &ARToolKit::load_matrix)

        .add_property("visible", &ARToolKit::is_visible);
    ;
}