import numpy as np

class object:
    def __init__(self, pos, emission = np.array([0, 0, 0]), roughness = 0, material = np.array([255, 255, 255])) -> None:
        self.pos = pos
        self.emission = emission
        self.material = material
        self.roughness = roughness   

    def rayLength(self, rayStart, reflectionVec) -> list[float, np.array, np.array]:
        ...

    def newReflection(self, reflectionVec, normVec) -> np.array:
        # Laver en householder vector, som får reflektioner til at få indgangsvinkel = udgangsvinkel vha spejling
        HHvector = (normVec) [:, np.newaxis]
        s = 2/np.vdot(HHvector, HHvector)
        HHmatrix = np.eye(3) - s * HHvector @ HHvector.T

        # Spejler strålen i normalvektoren for cirklen i skæringen.
        newReflectionVector = HHmatrix @ reflectionVec
        return newReflectionVector
            
