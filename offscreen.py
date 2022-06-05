import os
os.environ['PYOPENGL_PLATFORM'] = 'egl'

from OpenGL.EGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from ctypes import pointer
import cv2


class OffScreen(object):

    def __init__(self,width, height) -> None:
        self.width = width
        self.height = height
        configAttribs = [
                        EGL_SURFACE_TYPE, EGL_PBUFFER_BIT,
                        EGL_BLUE_SIZE, 8,
                        EGL_GREEN_SIZE, 8,
                        EGL_RED_SIZE, 8,
                        EGL_DEPTH_SIZE, EGL_DONT_CARE,
                        EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT,
                        EGL_NONE] 

        pbufferAttribs = [EGL_WIDTH, width,
                        EGL_HEIGHT, height,
                        EGL_NONE]

        self.disp = eglGetDisplay(EGL_DEFAULT_DISPLAY)

        major = EGLint()
        minor = EGLint()
        eglInitialize(self.disp,pointer(major),pointer(minor))

        #2. Select an appropriate configuration
        numConfigs=EGLint()
        eglCfg=EGLConfig()

        eglChooseConfig(self.disp, configAttribs, pointer(eglCfg), 1,  pointer(numConfigs))
        
        #3. Create a surface
        eglSurf = eglCreatePbufferSurface(self.disp, eglCfg, pbufferAttribs)

        #4. Bind the API
        eglBindAPI(EGL_OPENGL_API)


        # 5. Create a context and make it current
        eglCtx = eglCreateContext(self.disp, eglCfg, EGL_NO_CONTEXT, None)

        eglMakeCurrent(self.disp, eglSurf, eglSurf, eglCtx)
        # 6. Init OpenGL 
        glEnable(GL_TEXTURE_2D)
    
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        gluPerspective(45, (width / height), 0.1, 300.0)
       
        gluLookAt(3, 4, -5, 0, 0, 0, 0, -1, 0)

    def drawScene(self):
    #Change or add your custom drawing statments here
        vertices=[(1, -1, -1),
                    (1, 1, -1),
                    (-1, 1, -1),
                    (-1, -1, -1),
                    (1, -1, 1),
                    (1, 1, 1),
                    (-1, -1, 1),
                    (-1, 1, 1)]
    
        edges = [(0,1),(0,3),
                (0,4),(2,1),
                (2,3),(2,7),
                (6,3),(6,4),
                (6,7),(5,1),
                (5,4),(5,7)]

        glBegin(GL_LINES)
        for edge in edges:
                for index in edge:
                    glVertex3fv(vertices[index])
        glEnd()

    def saveScene(self):
    
        #gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
        img_buf = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        img = np.frombuffer(img_buf, np.uint8).reshape(self.height, self.width, 3)[::-1]
        img = img[:, :, ::-1].copy() 
        cv2.imwrite("testEGL.jpg",img)
    
    def terminate(self):
        eglTerminate(self.disp)

WIDTH =200
HEIGHT = 200
offscreen = OffScreen(WIDTH,HEIGHT)
offscreen.drawScene()
offscreen.saveScene()
offscreen.terminate()
