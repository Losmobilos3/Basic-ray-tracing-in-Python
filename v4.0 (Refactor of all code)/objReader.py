import numpy as np
import re # Used for finding floats in string
import obj3d



def addVertex(vertexes: list[np.array], line: str) -> None:
    cordsList: list[float] = [float(x) for x in re.findall(r"[-+]?(?:\d*\.*\d+)", line)]
    vertexes.append(np.array([cordsList[0], cordsList[1], cordsList[2]]))



def addFace(faces: list[np.array], line: str) -> None:
    vertexList: list[int] = [int(x) for x in re.findall(r"[-+]?(?:\d*\.*\d+)", line)]
    faces.append(np.array([vertexList[0], vertexList[1], vertexList[2]]))



def createObjFromObjFile(fileName: str, pos: np.array, emission: np.array, roughness: np.array, size: float, material: np.array) -> obj3d.object3d:
    file = open(fileName, 'r')
    objString : list[str] = file.readlines()

    vertexes : list[np.array] = []
    faces : list[np.array] = []
    normals : list[np.array] = []

    file.close()

    # Reads eachline
    for line in objString:
        if line[0] == '#':
            continue
        if line[0] == 'v':
            addVertex(vertexes, line)
        if line[0] == 'f':
            addFace(faces, line)

    for face in faces:
        v0 : np.array = vertexes[face[1]-1] - vertexes[face[0]-1]
        v1 : np.array = vertexes[face[2]-1] - vertexes[face[0]-1]
        u0 : np.array = v0/np.linalg.norm(v0)
        w1 : np.array = v1 - np.vdot(v1, v0)/np.vdot(v0, v0) * v0
        u1 : np.array = w1/np.linalg.norm(w1)
        normVec : np.array = -np.cross(u0, u1)
        normals.append(normVec)

    object = obj3d.object3d(vertexes=vertexes, faces=faces, normals=normals, pos=pos, emission=emission, roughness=roughness, size=size, material=material)

    return object