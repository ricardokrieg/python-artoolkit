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
            this->count = 0;
            this->patt_center[0] = 0.0;
            this->patt_center[1] = 0.0;
            static GLuint glid[4];

            char argv0[] = "artoolkit";
            char *argv[] = {argv0};
            int argc = 1;
            glutInit(&argc, argv);

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

            static int gImXsize = cparam.xsize;
            static int gImYsize = cparam.ysize;

            static ARParam gCparam;
            gCparam = cparam;
            for (int i = 0; i < 4; i++) {
                gCparam.mat[1][i] = (gCparam.ysize-1)*(gCparam.mat[2][i]) - gCparam.mat[1][i];
            }
            argConvGLcpara(&gCparam, AR_GL_CLIP_NEAR, AR_GL_CLIP_FAR, this->gl_cpara);

            static int    tex1Xsize1 = 1;
            static int    tex1Xsize2 = 1;
            static int    tex1Ysize  = 1;
            static int    tex2Xsize  = 1;
            static int    tex2Ysize  = 1;

            glGenTextures(4, glid);
            glBindTexture( GL_TEXTURE_2D, glid[0] );
            glPixelStorei( GL_UNPACK_ALIGNMENT, 1 );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );
            glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL );
            glBindTexture( GL_TEXTURE_2D, glid[1] );
            glPixelStorei( GL_UNPACK_ALIGNMENT, 1 );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );
            glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL );
            glBindTexture( GL_TEXTURE_2D, glid[2] );
            glPixelStorei( GL_UNPACK_ALIGNMENT, 1 );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );
            glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL );

            if( gImXsize > 512 ) {
                tex1Xsize1 = 512;
                tex1Xsize2 = 1;
                while( tex1Xsize2 < gImXsize - tex1Xsize1 ) tex1Xsize2 *= 2;
            }
            else {
                tex1Xsize1 = 1;
                while( tex1Xsize1 < gImXsize ) tex1Xsize1 *= 2;
            }
            tex1Ysize  = 1;
            while( tex1Ysize < gImYsize ) tex1Ysize *= 2;

            tex2Xsize = 1;
            while( tex2Xsize < gImXsize/2 ) tex2Xsize *= 2;
            tex2Ysize = 1;
            while( tex2Ysize < gImYsize/2 ) tex2Ysize *= 2;

            arVideoCapStart();

            // glMatrixMode(GL_PROJECTION);
            // glLoadIdentity();
            // gluPerspective(100, 1, 0.5, 500);
            // glMatrixMode(GL_MODELVIEW);
            // glLoadIdentity();
            // gluLookAt(0, 0, 100, 0, 0, 0, 0, 1, 0);
        }

        void update() {
            ARMarkerInfo *marker_info;
            int marker_num;
            int j, k;

            if ((this->dataPtr = (ARUint8 *)arVideoGetImage()) == NULL) {
                arUtilSleep(2);
                return;
            }
            if (this->count == 0) arUtilTimerReset();
            this->count++;

            argDrawMode2D();
            argDispImage(dataPtr, 0, 0);

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
            // argConvGlpara(this->patt_trans, this->gl_para);

            argDrawMode3D();
            argDraw3dCamera(0, 0);
            glClearDepth(1.0);
            glClear(GL_DEPTH_BUFFER_BIT);
            // glEnable(GL_DEPTH_TEST);
            // glDepthFunc(GL_LEQUAL);

            argConvGlpara(this->patt_trans, this->gl_para);
            glMatrixMode(GL_MODELVIEW);
            glLoadMatrixd(this->gl_para);

            // glEnable(GL_LIGHTING);
            // glEnable(GL_LIGHT0);
            // glLightfv(GL_LIGHT0, GL_POSITION, light_position);
            // glLightfv(GL_LIGHT0, GL_AMBIENT, ambi);
            // glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor);
            // glMaterialfv(GL_FRONT, GL_SPECULAR, mat_flash);
            // glMaterialfv(GL_FRONT, GL_SHININESS, mat_flash_shiny);  
            // glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient);
            // glMatrixMode(GL_MODELVIEW);
            // glTranslatef( 0.0, 0.0, 25.0 );
            // glutSolidCube(50.0);
            // glDisable( GL_LIGHTING );

            // glDisable( GL_DEPTH_TEST );
        }

        void close(void) {
            arVideoCapStop();
            arVideoClose();
            argCleanup();
        }

        BP::tuple get_size(void) {
            BP::tuple ret = BP::make_tuple(this->xsize, this->ysize);

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
        .def("close", &ARToolKit::close)

        .add_property("size", &ARToolKit::get_size)
    ;
}