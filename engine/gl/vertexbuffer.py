from ctypes import *
from OpenGL.GL import *

class VertexBuffer:
    _plain: POINTER(c_float)
    _buffer: GLuint

    def __init__(self, plain: list[float]):
        self.plain = plain
        self._plain = (c_float * len(self.plain))(*self.plain)
        self._buffer = GLuint()
        
        glGenBuffers(1, byref(self._buffer))
        self.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(c_float) * len(self.plain), self._plain, GL_STATIC_DRAW)

    def __del__(self):
        glDeleteBuffers(1, byref(self._buffer))

    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self._buffer)

        return self

class ArrayBuffer(VertexBuffer):
    def __init__(self, plain: tuple[int]):
        self.plain = plain
        self._plain = (c_int * len(self.plain))(*self.plain)
        self._buffer = GLuint()
        
        glGenBuffers(1, byref(self._buffer))
        self.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(c_float) * len(self.plain), self._plain, GL_STATIC_DRAW)
    
    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._buffer)

        return self