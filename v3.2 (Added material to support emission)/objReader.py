import numpy as np
import re # Used for finding floats in string
import obj3d

def addVertex(vertexes, line):
    cordsList = [float(x) for x in re.findall(r"[-+]?(?:\d*\.*\d+)", line)]
    vertexes.append(np.array([cordsList[0], cordsList[1], cordsList[2]]))

def addFace(faces, line):
    cordsList = [int(x) for x in re.findall(r"[-+]?(?:\d*\.*\d+)", line)]
    faces.append(np.array([cordsList[0], cordsList[1], cordsList[2]]))

def createObjFromObjFile(fileName, pos, emission, roughness, size):
    file = open(fileName, 'r')
    objString = file.readlines()

    vertexes = []
    faces = []
    normals = []

    file.close()

    # Reads eachline
    for line in objString:
        if line[0] == '#':
            continue
        if line[0] == 'v':
            addVertex(vertexes, line)
        if line[0] == 'f':
            addFace(faces, line)

    #for i in object.vertexes:
        #print(i)

    #for j in faces:
    #    print(j)

    for face in faces:
        v0 = vertexes[face[1]-1] - vertexes[face[0]-1]
        v1 = vertexes[face[2]-1] - vertexes[face[0]-1]
        u0 = v0/np.linalg.norm(v0)
        w1 = v1 - np.vdot(v1, v0)/np.vdot(v0, v0) * v0
        u1 = w1/np.linalg.norm(w1)
        normVec = -np.cross(u0, u1)
        normals.append(normVec)

    for k in normals:
        print(k)

    object = obj3d.object3d(vertexes=vertexes, faces=faces, normals=normals, pos=pos, emission=emission, roughness=roughness, size=size)

    return object