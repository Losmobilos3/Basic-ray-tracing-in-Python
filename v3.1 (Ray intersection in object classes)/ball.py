import numpy as np

class ball:
    def __init__(self, pos, radius, emission, roughness):
        self.pos = pos
        self.radius = radius
        self.emission = emission
        self.roughness = roughness
    


    def rayLength(self, rayStart, reflectionVec): # Returns raylength of -1, if no hit is detected
        # Find relativ bold position ift kameraet
        relativeBallPos = self.pos - rayStart

        # Find projektionen af den relative position på synslinjen

        projRelBPosOnSightVec = np.vdot(relativeBallPos, reflectionVec) * reflectionVec

        # Bestemmelse af hvor meget synslinjen "misser"
        leastLenFromBallCenter = np.linalg.norm(relativeBallPos - projRelBPosOnSightVec)

        # Hvis missLen er større end radius af bolden, så kan vi ikke se bolden på denne pixel
        # Hvis forholdet mellem projektionen og synslinjen er positiv, så ligger de i samme retning
        if (leastLenFromBallCenter <= self.radius and (projRelBPosOnSightVec[0]/reflectionVec[0]) > 0):
            unitProj = projRelBPosOnSightVec/np.linalg.norm(projRelBPosOnSightVec) # enhedsvektor til at træde tilbage til intersection
            backStepLen = np.sqrt(self.radius**2 - leastLenFromBallCenter**2) # Finder ud af hvor meget vi skal træde tilbage
            #print(backStepLen)
            actualRay = projRelBPosOnSightVec - backStepLen * unitProj # Træder den ønskede mængde tilbage
            lenOfReflection = np.linalg.norm(actualRay) # Beregner længden fra intersection til intersection
            intersectionPos = rayStart + actualRay
            return lenOfReflection, intersectionPos, intersectionPos - self.pos
        return -1, -1, -1
    


    def newReflection(self, reflectionVec, normVec):
        # Laver en householder vector, som får reflektioner til at få indgangsvinkel = udgangsvinkel vha spejling
        HHvector = (normVec) [:, np.newaxis]
        s = 2/np.vdot(HHvector, HHvector)
        HHmatrix = np.eye(3) - s * HHvector @ HHvector.T

        # Spejler strålen i normalvektoren for cirklen i skæringen.
        newReflectionVector = HHmatrix @ reflectionVec
        return newReflectionVector