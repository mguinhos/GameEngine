from ctypes import *
from OpenGL.GL import *

class TextureBuffer:
    _texture: GLuint
    _image: POINTER(c_ubyte)
    
    def __init__(self, pixels: bytes, width: int, height: int):
        self.pixels = pixels
        self.width = width
        self.height = height

        self._texture = GLuint()
        self._image = (c_ubyte * len(pixels))(*self.pixels)

        glGenTextures(1, byref(self._texture))
        self.bind()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self._image)
        glGenerateMipmap(GL_TEXTURE_2D)
    
    def __del__(self):
        glDeleteTextures(1, byref(self._texture))

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self._texture)

        return self
