import numpy as np
import ball

class camera:
    def __init__(self, fov, pos):
        self.fov = fov
        self.pos = pos
    


    def drawPixel(self, objects, x, y):
        sightVec = np.array([x/100, y/100, self.fov],  dtype=float)

        return self.castRay(objects, sightVec, self.pos)



    def castRay(self, objects, reflectionVec, pos, prevLen = 0, depth = 10, prevObj = 0):
        # Hvis rekursionsdybden er nået, så returner et lysniveau på 0
        if depth == 0:
            return np.zeros(3, dtype=float)

        for obj in objects:
            if prevObj != 0 and prevObj == obj:
                continue

            # Find relativ bold position ift kameraet
            relativeBallPos = obj.pos - pos

            # Find projektionen af den relative position på synslinjen
            projRelBPosOnSightVec = np.vdot(relativeBallPos, reflectionVec)/np.vdot(reflectionVec, reflectionVec) * reflectionVec

            # Bestemmelse af hvor meget synslinjen "misser"
            leastLenFromBallCenter = np.linalg.norm(relativeBallPos - projRelBPosOnSightVec)


            # Hvis missLen er større end radius af bolden, så kan vi ikke se bolden på denne pixel
            # Hvis forholdet mellem projektionen og synslinjen er positiv, så ligger de i samme retning
            if (leastLenFromBallCenter <= obj.radius and (projRelBPosOnSightVec[0]/reflectionVec[0]) > 0):
                # Bestemmelse af punkt hvor intersection sker
                unitProj = projRelBPosOnSightVec/np.linalg.norm(projRelBPosOnSightVec) # enhedsvektor til at træde tilbage til intersection
                backStepLen = np.sqrt(obj.radius**2 - leastLenFromBallCenter**2) # Finder ud af hvor meget vi skal træde tilbage
                actualRay = projRelBPosOnSightVec - backStepLen * unitProj # Træder den ønskede mængde tilbage
                lenOfReflection = np.linalg.norm(actualRay) # Beregner længden fra intersection til intersection
                intersectionPos = pos + actualRay

                # Laver en householder vector, som får reflektioner til at få indgangsvinkel = udgangsvinkel vha spejling
                HHvector = (intersectionPos - obj.pos) [:, np.newaxis]
                s = 2/np.vdot(HHvector, HHvector)
                HHmatrix = np.eye(3) - s * HHvector @ HHvector.T

                # Spejler strålen i normalvektoren for cirklen i skæringen.
                newReflectionVector = HHmatrix @ reflectionVec

                # Bruger afstands kvadrat loven til at beregne lysstyrken (*10^-4)
                lightFromCurrObj = obj.emission/((lenOfReflection + prevLen)**2*0.004*np.pi)
                lightFromNextObj = self.castRay(objects, newReflectionVector, pos = intersectionPos, prevLen= prevLen + lenOfReflection, depth= depth - 1, prevObj= obj)
                
                # Bøjer lyset lidt i samme farve som farven af det nuværende object
                bendVector = obj.emission + np.ones(3)
                bendVector = bendVector/np.linalg.norm(bendVector)
                lightFromNextObjBent = bendVector * lightFromNextObj

                # Calculates total light
                totalLight = lightFromCurrObj + lightFromNextObjBent
                return totalLight
        
        return np.zeros(3, dtype=float)

