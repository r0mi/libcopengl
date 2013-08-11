
def glBegin(GLenum mode):
    c_copengl.glBegin(mode)
    if _ERROR_CHECKING: _GET_GL_ERROR = 0


def glEnd():
    c_copengl.glEnd()
    if _ERROR_CHECKING:
        _GET_GL_ERROR = 1
        _CheckError()


# TODO: also test glTexImage2D & co with buffer objects..

def glTexImage1D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLint border, GLenum format, GLenum type, pixels):
    cdef char* c_pixels
    c_pixels = pixels
    c_copengl.glTexImage21(target, level, internalformat, width, border, format, type, c_pixels)
    if _GET_GL_ERROR: _CheckError()

def glTexImage2D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, pixels):
    cdef char* c_pixels
    c_pixels = pixels
    c_copengl.glTexImage2D(target, level, internalformat, width, height, border, format, type, c_pixels)
    if _GET_GL_ERROR: _CheckError()

def glTexSubImage1D(GLenum target, GLint level, GLint xoffset, GLsizei width, GLenum format, GLenum type, pixels):
    cdef char* c_pixels
    c_pixels = pixels
    c_copengl.glTexSubImage1D(target, level, xoffset, width, format, type, c_pixels)
    if _GET_GL_ERROR: _CheckError()

def glTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLenum type, pixels):
    cdef char* c_pixels
    c_pixels = pixels
    c_copengl.glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, c_pixels)
    if _GET_GL_ERROR: _CheckError()


def glGenTextures(GLsizei n):
    cdef GLuint* textures
    textures = <GLuint*>malloc(n*sizeof(GLuint*))
    c_copengl.glGenTextures(n, textures)
    if n == 1:
        ret = textures[0]
    else:
        ret = []
        for i from 0 < i < n:
            ret.append(textures[i])
    free(textures)
    if _GET_GL_ERROR: _CheckError()
    return ret

def glLightModelfv(GLenum pname, params):
    cdef GLfloat _p[4]
    if type(params) == float: _p[0] = params
    else: _p[0], _p[1], _p[2], _p[3] = params
    c_copengl.glLightModelfv(pname, _p)
    if _GET_GL_ERROR: _CheckError()

def glLightModeliv(GLenum pname, params):
    cdef GLint _p[4]
    if type(params) == int: _p[0] = params
    else: _p[0], _p[1], _p[2], _p[3] = params
    c_copengl.glLightModeliv(pname, _p)
    if _GET_GL_ERROR: _CheckError()

def glLightfv(GLenum light, GLenum pname, params):
    cdef GLfloat _p[4]
    if type(params) == float: _p[0] = params
    elif len(params) == 3: _p[0], _p[1], _p[2] = params ; _p[3] = 1
    else: _p[0], _p[1], _p[2], _p[3] = params
    c_copengl.glLightfv(light, pname, _p)
    if _GET_GL_ERROR: _CheckError()

def glLightiv(GLenum light, GLenum pname, params):
    cdef GLint _p[4]
    if type(params) == int: _p[0] = params
    elif len(params) == 3: _p[0], _p[1], _p[2] = params ; _p[3] = 1
    else: _p[0], _p[1], _p[2], _p[3] = params
    c_copengl.glLightiv(light, pname, _p)
    if _GET_GL_ERROR: _CheckError()


def glMaterialfv(GLenum face, GLenum pname, params):
    # pyglet replacement version
    #cdef GLfloat _p[4]
    #try:
    #    _p[0], _p[1], _p[2], _p[3] = params
    #except TypeError:
    #    if type(params) == float: _p[0] = params
    #    else: _p[0] = params.value # ctypes.c_float
    #c_copengl.glMaterialfv(face, pname, _p)
    #if _GET_GL_ERROR: _CheckError()

    # original version
    cdef GLfloat _p[4]
    if type(params) == float: _p[0] = params
    else: _p[0], _p[1], _p[2], _p[3] = params
    c_copengl.glMaterialfv(face, pname, _p)
    if _GET_GL_ERROR: _CheckError()

def glMaterialiv(GLenum face, GLenum pname, params):
    cdef GLint _p[4]
    if type(params) == int: _p[0] = params
    else: _p[0], _p[1], _p[2], _p[3] = params
    c_copengl.glMaterialiv(face, pname, _p)
    if _GET_GL_ERROR: _CheckError()


def glMultMatrixd(m):
    cdef GLdouble _p[16]
    assert len(m) == 16
    _p[0], _p[1], _p[2], _p[3], _p[4], _p[5], _p[6], _p[7], _p[8], _p[9], _p[10], _p[11], _p[12], _p[13], _p[14], _p[15] = m
    c_copengl.glMultMatrixd(_p)
    if _GET_GL_ERROR: _CheckError()

def glMultMatrixf(m):
    cdef GLfloat _p[16]
    assert len(m) == 16
    _p[0], _p[1], _p[2], _p[3], _p[4], _p[5], _p[6], _p[7], _p[8], _p[9], _p[10], _p[11], _p[12], _p[13], _p[14], _p[15] = m
    c_copengl.glMultMatrixf(_p)
    if _GET_GL_ERROR: _CheckError()
