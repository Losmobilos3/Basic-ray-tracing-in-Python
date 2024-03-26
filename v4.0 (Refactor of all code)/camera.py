import numpy as np
import ball

class camera:
    def __init__(self, fov, pos) -> None:
        self.fov = fov
        self.pos = pos
    


    def drawPixel(self, objects, x, y) -> np.array:
        sightVec : np.array = np.array([x/100, y/100, self.fov],  dtype=float)

        return self.castRay(objects, sightVec, self.pos)



    def castRay(self, objects, reflectionVec, pos, prevLen = 0, depth = 5, prevObj = 0) -> np.array:
        # Hvis rekursionsdybden er nået, så returner et lysniveau på 0
        if depth == 0:
            return np.zeros(3, dtype=float)

        reflectionVec : np.array = reflectionVec/np.linalg.norm(reflectionVec)

        minRayLen : float = -1
        firstIntersectionPos : float = -1
        firstObjHit : float = -1
        firstNormVec : float = -1

        # Find objektet som strålen rammer først
        for obj in objects:
            if prevObj != 0 and prevObj == obj:
                continue
            
            # Finder længden af alle objekter der bliver ramt
            rayLen, intersectionPos, normVec = obj.rayLength(pos, reflectionVec) # rayLen = -1 betyder at objektet ikke blev ramt

            # Bestemmer det første objekt der bliver ramt
            if rayLen != -1 and (minRayLen == -1 or rayLen < minRayLen):
                minRayLen = rayLen
                firstIntersectionPos = intersectionPos
                firstNormVec = normVec
                firstObjHit = obj
            
        if minRayLen == -1: # Hvis ingen objekter blev ramt, returner 0 lys
            return np.zeros(3, dtype=float)

        # Bruger afstands kvadrat loven til at beregne lysstyrken (*10^-4)
        lightFromCurrObj : np.array = firstObjHit.emission/((minRayLen + prevLen)**2*0.004*np.pi)

        # Init af total light
        totalLight : np.array = lightFromCurrObj

        # Bestemmelse af reflektionsvektor
        newReflectionVector : np.array = firstObjHit.newReflection(reflectionVec, firstNormVec)

        # Beregner lyset fra 'n' andre tilfældige rays
        NOReflections : int = 1 # Siger noget om kvaliteten af reflektioner. lavt tal -> fejlpixels
        for i in range(NOReflections):
            randomOffset : np.array = np.random.rand(3)
            randomOffset /= np.linalg.norm(randomOffset)

            # Randomiserer reflektionen lidt. Siger noget om overfladen af objektets rughed
            newRandReflectionVector : np.array = newReflectionVector + randomOffset * firstObjHit.roughness

            lightFromNextObj : np.array = self.castRay(objects, newRandReflectionVector, pos = firstIntersectionPos, prevLen= prevLen + minRayLen, depth= depth - 1, prevObj= firstObjHit)

            #! Dette skal forbedres ift hvad der faktisk sker
            # Bøjer lyset lidt i samme farve som farven af det nuværende object
            bendVector : np.array = firstObjHit.material + np.ones(3)
            bendVector = bendVector/np.linalg.norm(bendVector)
            lightFromNextObjBent: np.array = bendVector * lightFromNextObj

            # Beregner total mængde lys.
            totalLight += lightFromNextObjBent / NOReflections
        return totalLight

