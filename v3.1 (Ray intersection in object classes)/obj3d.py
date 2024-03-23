import numpy as np

class object3d:
    def __init__(self, vertexes, faces, normals, pos, emission, roughness, size):
        self.pos = pos
        self.emission = emission
        self.roughness = roughness
        self.vertexes = [vertex * size + pos for vertex in vertexes]
        self.faces = faces
        self.normals = normals

    def rayLength(self, rayStart, reflectionVec):
        movedVertexes = [vertex - rayStart for vertex in self.vertexes]

        firstHitFace = -1
        firstIntersection = -1
        firstRayLength = -1

        for face in range(len(self.faces)):
            # Gets the corners of the triangle
            a = movedVertexes[self.faces[face][0]-1]
            b = movedVertexes[self.faces[face][1]-1]
            c = movedVertexes[self.faces[face][2]-1]

            # Beregning af intersection med plan som trekant ligger på.
            ab = (b - a) [:, np.newaxis]
            ac = (c - a) [:, np.newaxis]

            # beregner intersection med planen
            A = np.hstack([ab, ac, reflectionVec[:, np.newaxis]])
            # Init of interception
            I = -1
            # Løser ligningssystem for strålen
            if np.vdot(reflectionVec, self.normals[face]) != 0: # Hvis ray'en er parallel med planen, så er der ingen interception
                t = np.linalg.solve(A, a) [2]
                if t > 0:
                    I = reflectionVec * t + rayStart
                    #print(I)
                else: 
                    continue
            else:
                continue

            # Nu er intersection med planen (I) bestemt. Vi skal nu bestemme om vi rammer trekanten på planen

            corners = [a, b, c]
            #! Computation of barycentric coordinates
            baryCords = np.array([0, 0, 0], dtype=float)
            for corner in range(3):
                #! Beregner ratio af barycentrisk koordinat
                ab = corners[(corner+1) % 3] - corners[corner]
                cb = corners[(corner+1) % 3] - corners[(corner+2) % 3]

                aI = (I - rayStart) - corners[corner]

                heightOfTriangle = np.linalg.norm(ab - np.vdot(ab, cb)/np.vdot(cb, cb) * cb)
                heightOfIntersecTriangle = np.linalg.norm(aI - np.vdot(aI, cb)/np.vdot(cb, cb) * cb)
                ratioBetweenHeights = heightOfIntersecTriangle / heightOfTriangle

                #print("                                     ratios: ", heightOfTriangle, heightOfIntersecTriangle, ratioBetweenHeights)

                baryCords[corner] = 1.0 - ratioBetweenHeights # Bestemmer den barycentriske koordinat
            
            rayLength = np.linalg.norm(I - rayStart)

            #print("                             BaryCords: ", baryCords)
            if all(cord > 0 for cord in baryCords) and (rayLength < firstRayLength or firstRayLength == -1):
                #print("Jeg rammer trekanten")
                firstHitFace = face
                firstRayLength = rayLength
                firstIntersection = I

        if firstHitFace == -1:
            return -1, -1, -1 # No intersection found
        return firstRayLength, firstIntersection, self.normals[firstHitFace] # Ellers returner længden af reflektionen og intersection punktet
        


    def newReflection(self, reflectionVec, normVec):
        # Laver en householder vector, som får reflektioner til at få indgangsvinkel = udgangsvinkel vha spejling
        HHvector = (normVec) [:, np.newaxis]
        s = 2/np.vdot(HHvector, HHvector)
        HHmatrix = np.eye(3) - s * HHvector @ HHvector.T

        # Spejler strålen i normalvektoren for cirklen i skæringen.
        newReflectionVector = HHmatrix @ reflectionVec
        return newReflectionVector
            
