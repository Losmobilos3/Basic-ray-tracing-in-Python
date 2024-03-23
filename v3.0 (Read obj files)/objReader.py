import numpy as np
import re # Used for finding floats in string
import obj3d

def addVertex(vertexes, line):
    cordsList = [float(x) for x in re.findall(r"[-+]?(?:\d*\.*\d+)", line)]
    vertexes.append(np.array([cordsList[0], cordsList[1], cordsList[2]]))

def addFace(faces, line):
    cordsList = [int(x) for x in re.findall(r"[-+]?(?:\d*\.*\d+)", line)]
    faces.append(np.array([cordsList[0], cordsList[1], cordsList[2]]))




file = open('./pyramid.obj', 'r')
objString = file.readlines()

file.close()

object = obj3d.object3d()

# Reads eachline
for line in objString:
    if line[0] == '#':
        continue
    if line[0] == 'v':
        addVertex(object.vertexes, line)
    if line[0] == 'f':
        addFace(object.faces, line)

for i in object.vertexes:
    print(i)

for j in object.faces:
    print(j)

for face in object.faces:
    v0 = object.vertexes[face[1]-1] - object.vertexes[face[0]-1]
    v1 = object.vertexes[face[2]-1] - object.vertexes[face[0]-1]
    u0 = v0/np.linalg.norm(v0)
    w1 = v1 - np.vdot(v1, v0)/np.vdot(v0, v0) * v0
    u1 = w1/np.linalg.norm(w1)
    normVec = -np.cross(u0, u1)
    object.normals.append(normVec)
    

for k in object.normals:
    print(k)
