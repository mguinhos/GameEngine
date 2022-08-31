from PIL import Image
from engine.camera import Camera
from engine.position import Position, Size

from engine.util import wavefront

from engine.mesh import Mesh
from engine.texture import Texture

from engine.ui.window import Window
from engine.ui.key import Key

from OpenGL.GL import *

class RootWindow(Window):
    def on_begin(self):
        self.camera = Camera()
        self.camera.position.y = 8
        self.camera.position.z = 8
        self.camera.position.x = -8
        
        self.mesh = wavefront.parse(open('models/cube.obj'))
        self.mesh.texture = Texture(Image.open('models/blocks.jpg'))

        self.skydome = wavefront.parse(open('models/skydome.obj'))
        self.skydome.texture = Texture(Image.open('models/sky.png'))

        self.skydome = self.skydome.instanciate()
        self.skydome.size = Size(100, 100, 100)

        self.rocket = wavefront.parse(open('models/rocket.obj'))
        self.rocket.texture = Texture(Image.open('models/rocket_texture.png'))

        self.terrain = wavefront.parse(open('models/terrain.obj'))
        self.terrain.texture = Texture(Image.open('models/terrain_texture.png'))
        self.terrain = self.terrain.instanciate()
        self.terrain.size = Size(5, 5, 5)
        
        self.rocket = self.rocket.instanciate()
        self.rocket.size = Size(0.5, 0.5, 0.5)
        self.rocket.position.y = 8

        self.acceleration = 0

        self.mesh = self.mesh.instanciate()

        glMatrixMode(GL_PROJECTION)
        glFrustum(-1, 1, -1, 1, 1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glShadeModel (GL_SMOOTH)
        
    def on_update(self):
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.camera.look(self.rocket.position)

        glPushMatrix()
        glRotate(self.camera.rotation.x, 1, 0, 0)
        glRotate(self.camera.rotation.y, 0, 1, 0)
        glRotate(self.camera.rotation.z, 0, 0, 1)
        glTranslate(-self.camera.position.x, -self.camera.position.y, -self.camera.position.z)
        self.rocket.draw()
        self.mesh.draw()
        self.skydome.draw()
        self.terrain.draw()

        self.mesh.boundingbox.draw()
        self.rocket.boundingbox.draw()

        glPopMatrix()

        self.rocket.position.y -= self.acceleration

        if self.mesh.boundingbox.collided(self.rocket.boundingbox) or self.terrain.boundingbox.collided(self.rocket.boundingbox):
            while self.mesh.boundingbox.collided(self.rocket.boundingbox) or self.terrain.boundingbox.collided(self.rocket.boundingbox):
                self.rocket.position.y += 0.01
            
            self.rocket.position.y -= 0.01
        else:
            self.acceleration += 0.01
        
        if self.rocket.position.y < -100:
            self.rocket.position.y = 10
            self.acceleration = 0

        glDepthFunc(GL_LESS)
    
    def on_press(self, keys: dict[str, Key]):
        if keys.get(Key.Left):
            self.rocket.position.x -= 0.05
        elif keys.get(Key.Right):
            self.rocket.position.x += 0.05
        
        if keys.get(Key.Up):
            self.rocket.position.z -= 0.05
        elif keys.get(Key.Down):
            self.rocket.position.z += 0.05
        
        if keys.get(Key.Space):
            self.acceleration -= 0.1

RootWindow("hello, world").run()