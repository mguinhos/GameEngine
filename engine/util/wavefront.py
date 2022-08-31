from io import StringIO

from ..mesh import Mesh, Texcoord, Vertex, Normal, Face

def parse(stream: StringIO) -> Mesh:
    vertices = []
    normals = []
    texcoords = []
    faces = []

    for line in filter(None, (l.split() for l in stream)):
        if line[0] == 'v':
            vertices.append([float(value) for value in line[1:]])
        elif line[0] == 'vn':
            normals.append([float(value) for value in line[1:]])
        elif line[0] == 'vt':
            texcoords.append([float(value) for value in line[1:]])
        elif line[0] == 'f':
            faces.append([[int(v or 0) for v in value.split('/')] for value in line[1:]])
    
    vertices = [Vertex(x, y, z) for x, y, z in vertices]
    normals = [Normal(x, y, z) for x, y, z in normals]
    texcoords = [Texcoord(x, -y) for x, y in texcoords]
    fcs = []
    
    for face in faces:
        fc = Face([], [], [])
        for v, vt, vn in face:
            fc.vertex_indices.append(v)
            
            if vt:
                fc.texcoord_indices.append(vt)
            
            if vn:
                fc.normal_indices.append(vn)
        
        fcs.append(fc)

    return Mesh(fcs, vertices, normals, texcoords)
