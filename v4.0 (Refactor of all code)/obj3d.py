import numpy as np
import object as ob

class object3d(ob.object):
    def __init__(self, vertexes, faces, normals, pos, emission = np.array([0, 0, 0]), roughness = 0, size = 1, material = np.array([255, 255, 255])) -> None:
        super().__init__(pos=pos, emission=emission, roughness=roughness, material=material)
        self.vertexes = [vertex * size + pos for vertex in vertexes]
        self.faces = faces
        self.normals = normals

    def rayLength(self, rayStart, reflectionVec) -> list[float, np.array, np.array]:
        movedVertexes = [vertex - rayStart for vertex in self.vertexes]

        firstHitFace : int = -1
        firstIntersection : np.array = -1
        firstRayLength : float = -1

        for face in range(len(self.faces)):
            # Hvis facet peger væk fra kameraet, så kan vi godt skippe det.
            if reflectionVec @ self.normals[face] > 0:
                continue
            
            # Gets the corners of the triangle
            a : np.array = movedVertexes[self.faces[face][0]-1]
            b : np.array = movedVertexes[self.faces[face][1]-1]
            c : np.array = movedVertexes[self.faces[face][2]-1]

            # Beregning af intersection med plan som trekant ligger på.
            ab : np.array = (b - a) [:, np.newaxis]
            ac : np.array = (c - a) [:, np.newaxis]

            # beregner intersection med planen
            A : np.array = np.hstack([ab, ac, reflectionVec[:, np.newaxis]])
            # Init of interception
            I : np.array = -1
            # Løser ligningssystem for strålen
            if np.allclose(np.vdot(reflectionVec, self.normals[face]), 0): # Hvis ray'en er parallel med planen, så er der ingen interception
                continue

            t : float = np.linalg.solve(A, a) [2]

            # Hvis objektet bliver ramt bag kameraet, gå videre til næste flade
            if t < 0:
                continue

            I = reflectionVec * t + rayStart

            # Nu er intersection med planen (I) bestemt. Vi skal nu bestemme om vi rammer trekanten på planen

            corners : list[np.array] = [a, b, c]
            # Computation of barycentric coordinates
            baryCords : np.array = np.array([0, 0, 0], dtype=float)
            for corner in range(3):
                # Beregner ratio af barycentrisk koordinat
                ab : np.array = corners[(corner+1) % 3] - corners[corner]
                cb : np.array = corners[(corner+1) % 3] - corners[(corner+2) % 3]

                aI : np.array = (I - rayStart) - corners[corner]

                heightOfTriangle : float = np.linalg.norm(ab - np.vdot(ab, cb)/np.vdot(cb, cb) * cb)
                heightOfIntersecTriangle : float = np.linalg.norm(aI - np.vdot(aI, cb)/np.vdot(cb, cb) * cb)
                ratioBetweenHeights : float = heightOfIntersecTriangle / heightOfTriangle

                baryCords[corner] = 1.0 - ratioBetweenHeights # Bestemmer den barycentriske koordinat
            
            rayLength : float = np.linalg.norm(I - rayStart)

            if all(cord > 0 for cord in baryCords) and (rayLength < firstRayLength or firstRayLength == -1):
                #print("Jeg rammer trekanten")
                firstHitFace = face
                firstRayLength = rayLength
                firstIntersection = I

        if firstHitFace == -1:
            return -1, -1, -1 # No intersection found
        return firstRayLength, firstIntersection, self.normals[firstHitFace] # Ellers returner længden af reflektionen og intersection punktet
        

