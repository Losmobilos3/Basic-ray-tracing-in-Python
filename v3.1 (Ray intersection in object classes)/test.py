import camera as c
import numpy as np
import ball as b
import matplotlib.pyplot as plt
import objReader as objR


# Set up the display
width, height = 800, 600
setFov = 6
screen = np.ones((height, width, 3), dtype=np.uint8)

screen[:, :] = [40, 40, 80]


# Function to draw a pixel
def draw_pixel(color, x, y):
    screen[y, x] = color


# Objects list
objects = []
#objects.append(b.ball(np.array([-11, 12, 50], dtype=float), 10, np.array([2000, 2000, 2000], dtype=float), roughness=0.5))
#objects.append(b.ball(np.array([-11, -12, 50], dtype=float), 10, np.array([2000, 2000, 2000], dtype=float), roughness=0))
#objects.append(b.ball(np.array([22, 0, 40], dtype=float), 10, np.array([5000, 0, 0], dtype=float), roughness=0))
objects.append(b.ball(np.array([-10, 20, 4], dtype=float), 10, np.array([0, 25550, 0], dtype=float), roughness=0))
objects.append(objR.createObjFromObjFile(fileName='pyramid.obj', pos=np.array([0, 0, 10], dtype=float), emission=np.array([300, 300, 300]), roughness=0.7, size=4))

# Init af kamera
cam = c.camera(fov= setFov, pos= np.array([0, 0, -10], dtype=float))

# Draw screen
for i in range(width):
    print(i)
    for j in range(height):

        # Determines light level of pixel
        lightLevel = cam.drawPixel(objects, i - width/2, -(j - height/2))

        # Trækker lysskalaen fra -infty;infty ned til 0;255
        lightLevel = [285/(1 + np.exp(-0.02*(color)+2)) - 30 if color > 0 else 0 for color in lightLevel]
        
        if (any(color > 0 for color in lightLevel)):
            draw_pixel(lightLevel, i, j)

# Vis skærmen
plt.imshow(screen)
plt.axis('off')  # Turn off axis
plt.show()