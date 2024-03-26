import numpy as np
import object as ob

class ball(ob.object):
    def __init__(self, pos, radius, emission = np.array([0, 0, 0]), material = np.array([255, 255, 255]), roughness = 0):
        super().__init__(pos=pos, emission=emission, roughness=roughness, material=material)
        self.radius = radius
    


    def rayLength(self, rayStart, reflectionVec) -> list[float, np.array, np.array]: # Returns raylength of -1, if no hit is detected
        # Find relativ bold position ift kameraet
        relativeBallPos : np.array = self.pos - rayStart

        # Find projektionen af den relative position på synslinjen

        projRelBPosOnSightVec : np.array = np.vdot(relativeBallPos, reflectionVec) * reflectionVec

        # Bestemmelse af hvor meget synslinjen "misser"
        leastLenFromBallCenter : np.array = np.linalg.norm(relativeBallPos - projRelBPosOnSightVec)

        # Hvis missLen er større end radius af bolden, så kan vi ikke se bolden på denne pixel
        # Hvis forholdet mellem projektionen og synslinjen er positiv, så ligger de i samme retning
        if (leastLenFromBallCenter <= self.radius and (projRelBPosOnSightVec[0]/reflectionVec[0]) > 0):
            unitProj : np.array = projRelBPosOnSightVec/np.linalg.norm(projRelBPosOnSightVec) # enhedsvektor til at træde tilbage til intersection
            backStepLen : float = np.sqrt(self.radius**2 - leastLenFromBallCenter**2) # Finder ud af hvor meget vi skal træde tilbage
            actualRay : np.array = projRelBPosOnSightVec - backStepLen * unitProj # Træder den ønskede mængde tilbage
            lenOfReflection : float = np.linalg.norm(actualRay) # Beregner længden fra intersection til intersection
            intersectionPos : np.array = rayStart + actualRay
            return lenOfReflection, intersectionPos, intersectionPos - self.pos
        return -1, -1, -1
    
