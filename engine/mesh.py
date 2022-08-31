from dataclasses import dataclass
from ctypes import *
from OpenGL.GL import *

from .gl.vertexbuffer import VertexBuffer
from .position import Vector, Position, Rotation, Size
from .texture import Texture

class Vertex(Vector):
    pass

class Normal(Vector):
    pass

class Texcoord(Vector):
    pass

@dataclass
class Face:
    vertex_indices: tuple[int]
    normal_indices: tuple[int]
    texcoord_indices: tuple[int] 

class BoundingBox:
    def __init__(self, position: Position, size: Size):
        self.position = position
        self.size = size
    
    def inside(self, position: Position):
        if position.x >= self.position.x and position.x <= self.position1.x:
            if position.y >= self.position.y and position.y <= self.position1.y:
                if position.z >= self.position.z and position.z <= self.position1.z:
                    return True
        
        return False
    
    def draw(self):
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex3f(self.position.x, self.position.y, self.position.z)
        glVertex3f(self.position1.x, self.position.y, self.position.z)

        glVertex3f(self.position1.x, self.position.y, self.position1.z)
        glVertex3f(self.position.x, self.position.y, self.position1.z)

        glVertex3f(self.position.x, self.position.y, self.position.z)
        glVertex3f(self.position.x, self.position.y, self.position1.z)

        glVertex3f(self.position1.x, self.position.y, self.position.z)
        glVertex3f(self.position1.x, self.position.y, self.position1.z)


        glVertex3f(self.position.x, self.position1.y, self.position.z)
        glVertex3f(self.position1.x, self.position1.y, self.position.z)

        glVertex3f(self.position1.x, self.position1.y, self.position1.z)
        glVertex3f(self.position.x, self.position1.y, self.position1.z)

        glVertex3f(self.position.x, self.position1.y, self.position.z)
        glVertex3f(self.position.x, self.position1.y, self.position1.z)

        glVertex3f(self.position1.x, self.position1.y, self.position.z)
        glVertex3f(self.position1.x, self.position1.y, self.position1.z)

        glEnd()
    
    def collided(self, boundingbox: "BoundingBox"):
        return (
            self.position.x <= boundingbox.position1.x and
            self.position1.x >= boundingbox.position.x and
            self.position.y <= boundingbox.position1.y and
            self.position1.y >= boundingbox.position.y and
            self.position.z <= boundingbox.position1.z and
            self.position1.z >= boundingbox.position.z
        )
    
    @property
    def position1(self):
        return self.position + self.size

def OFFSET(offset: int) -> c_void_p:
    return c_void_p(sizeof(c_float) * offset)

class MeshInstance:
    position: Position
    rotation: Rotation
    size: Size

    def __init__(self, owner: "Mesh", faces: list[Face], vertices: list[Vertex], normals: list[Normal], texcoords: list[Texcoord], *, position=Position(0, 0, 0), rotation=Rotation(0, 0, 0), size=Size(1, 1, 1), texture: Texture=None):
        self.owner = owner
        self.faces = faces
        self.vertices = vertices
        self.normals = normals
        self.texcoords = texcoords
        self.position = position.copy()
        self.rotation = rotation.copy()
        self.size = size.copy()
        self.texture = texture
        self.update()
    
    def _create_vertex_buffer(self):
        self.flat_vertices = []
        self.flat_normals = []
        self.flat_texcoords = []

        for face in self.faces:
            for vertex_indice in face.vertex_indices:
                if vertex_indice:
                    self.flat_vertices.append(self.vertices[vertex_indice -1].flat)
            
            for normal_indice in face.normal_indices:
                if normal_indice:
                    self.flat_normals.append(self.normals[normal_indice -1].flat)
            
            for texcoord_indice in face.texcoord_indices:
                if texcoord_indice:
                    self.flat_texcoords.append(self.texcoords[texcoord_indice -1].flat)
        
        flat = []

        if self.flat_normals:
            if self.flat_texcoords:
                for v, n, t in zip(self.flat_vertices, self.flat_normals, self.flat_texcoords):
                    flat.extend(v)
                    flat.extend(n)
                    flat.extend(t)
            else:
                for v, n in zip(self.flat_vertices, self.flat_normals):
                    flat.extend(v)
                    flat.extend(n)
        else:
            for v in self.flat_vertices:
                flat.extend(v)
        
        self.min_vertex = Vertex(
            min((v.x for v in self.vertices)),
            min((v.y for v in self.vertices)),
            min((v.z for v in self.vertices))
        )

        self.max_vertex = Vertex(
            max((v.x for v in self.vertices)),
            max((v.y for v in self.vertices)),
            max((v.z for v in self.vertices))
        )

        return VertexBuffer(flat)
    
    def update(self):
        self.vertexbuffer = self._create_vertex_buffer()
        
        if self.texture:
            self.texture = self.texture.instanciate()

        self.stride = 3

        if self.normals:
            self.stride += 3
        
        if self.texcoords:
            self.stride += 3
        
        self.stride *= sizeof(c_float)

        return self
    
    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        self.vertexbuffer.bind()
        
        if self.texture:
            glEnable(GL_TEXTURE_2D)
            self.texture.bind()

        glVertexPointer(3, GL_FLOAT, self.stride, None)
        
        if self.normals:
            glNormalPointer(GL_FLOAT, self.stride, OFFSET(3))

            if self.texcoords:
                glTexCoordPointer(2, GL_FLOAT, self.stride, OFFSET(6))

        elif self.texcoords:
            glTexCoordPointer(2, GL_FLOAT, self.stride, OFFSET(3))

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslate(self.position.x, self.position.y, self.position.z)
        glScale(self.size.x, self.size.y, self.size.z)
        glRotate(self.rotation.x, 1, 0, 0)
        glRotate(self.rotation.y, 0, 1, 0)
        glRotate(self.rotation.z, 0, 0, 1)
        glDrawArrays(GL_TRIANGLES, 0, len(self.flat_vertices))
        glPopMatrix()

        if self.texture:
            glDisable(GL_TEXTURE_2D)

        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
    
    @property
    def boundingbox(self):
        position = Position(self.min_vertex.x, self.min_vertex.y, self.min_vertex.z)
        size = Size(self.max_vertex.x, self.max_vertex.y, self.max_vertex.z) - position
        
        return BoundingBox(self.position + (position * self.size), size * self.size)

class Mesh:
    def __init__(self, faces: list[Face], vertices: list[Vertex], normals: list[Normal], texcoords: list[Texcoord], texture: Texture=None):
        self.faces = faces
        self.vertices = vertices
        self.normals = normals
        self.texcoords = texcoords
        self.texture = texture
    
    def instanciate(self):
        return MeshInstance(self, self.faces, self.vertices, self.normals, self.texcoords, texture=self.texture)