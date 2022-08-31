from PIL.Image import Image

from .gl.texturebuffer import TextureBuffer

class TextureInstance:
    def __init__(self, owner: "Texture", image: Image):
        self.owner = owner
        self.image = image

        if self.image.width % 2 != 0 or self.image.height % 2 != 0:
            self.image = self.image.resize((256, 256))

        self.update()

    def _create_texture_buffer(self):
        return TextureBuffer(self.image.tobytes(), self.image.width, self.image.height)
    
    def update(self):
        self.texture_buffer = self._create_texture_buffer()
        return self
    
    def bind(self):
        return self.texture_buffer.bind()

class Texture:
    def __init__(self, image: Image):
        self.image = image
    
    def instanciate(self):
        return TextureInstance(self, self.image.convert('RGB'))