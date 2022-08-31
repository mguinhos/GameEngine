from ctypes import c_void_p
from OpenGL.GL import glViewport

from time import sleep
import glfw

from .key import Key

glfw.init()

class Window:
    _window: c_void_p=None

    def __init__(self, title: str, width=800, height=600, parent: "Window"=None):
        self.title = title
        self.width = width
        self.height = height
        self.parent = parent
    
    def on_update(self):
        return self
    
    def on_press(self, keys: dict[str, Key]):
        return self
    
    def on_begin(self):
        return self
    
    def on_end(self):
        return self
    
    def show(self):
        glfw.show_window(self._window)
        return self
    
    def hide(self):
        glfw.hide_window(self._window)
        return self
    
    def update(self):
        self.on_update()

        pressed_keys: dict[str, Key] = {}
        
        for key in Key.__members__.values():
            if glfw.get_key(self._window, key.value):
                pressed_keys[key] = True 

        if pressed_keys:
            self.on_press(pressed_keys)

        glfw.swap_buffers(self._window)

        return self

    def run(self):
        self._window = glfw.create_window(self.width, self.height, self.title, None, self.parent._window if self.parent else None)
        glfw.make_context_current(self._window)


        if self.width > self.height:
            glViewport(0,  (self.height - self.width) // 2, self.width, self.width)
        else:
            glViewport((self.width - self.height) // 2, 0, self.height, self.height)

        self.on_begin()

        while not self.closed:
            glfw.poll_events()
            self.update()
            sleep(0.01)
        
        self.on_end()
        
        return self

    @property
    def closed(self):
        if self._window:
            return bool(glfw.window_should_close(self._window))
        
        return False