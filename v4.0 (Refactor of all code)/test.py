import camera as c
import numpy as np
import ball as b
import matplotlib.pyplot as plt
import objReader as objR
import object as ob


# Set up the display
width: int = 800
height: int = 600
setFov: float = 6
screen: np.array = np.ones((height, width, 3), dtype=np.uint8)

screen[:, :] = np.array([40, 40, 80])


# Function to draw a pixel
def draw_pixel(color: np.array, x: int, y: int) -> None:
    screen[y, x] = color


# Objects list
objects: list[ob.object] = []
#objects.append(b.ball(np.array([-11, 12, 50], dtype=float), 10, np.array([2000, 2000, 2000], dtype=float), roughness=0.5))
#objects.append(b.ball(np.array([-11, -12, 50], dtype=float), 10, np.array([2000, 2000, 2000], dtype=float), roughness=0))
#objects.append(b.ball(np.array([22, 0, 40], dtype=float), 10, np.array([5000, 0, 0], dtype=float), roughness=0))
objects.append(b.ball(np.array([-10, 20, 4], dtype=float), 14, np.array([25550, 25550, 25550], dtype=float), roughness=0))
objects.append(objR.createObjFromObjFile(fileName='pyramidR.obj', pos=np.array([0, 0, 10], dtype=float), emission=np.array([0, 0, 0]), material=np.array([255, 0, 0]), roughness=0.7, size=4))

# Init af kamera
cam: c.camera = c.camera(fov= setFov, pos= np.array([0, 0, -10], dtype=float))

# Draw screen
for i in range(width):
    print(i) # Indicator for how long the code has come in its runtime
    for j in range(height):

        # Determines light level of pixel
        lightLevel, objHit = cam.drawPixel(objects=objects, x=i - width/2, y=-(j - height/2))

        # Trækker lysskalaen fra -infty;infty ned til 0;255
        lightLevel: list[int] = [285/(1 + np.exp(-0.02*(color)+2)) - 30 if color > 0 else 0 for color in lightLevel]
        
        if objHit:
            draw_pixel(color=lightLevel, x=i, y=j)

# Vis skærmen
plt.imshow(screen)
plt.axis('off')  # Turn off axis
plt.show()