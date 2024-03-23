import camera as c
import numpy as np
import ball as b
import time
import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
setFov = 12
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Raytracing")
clock = pygame.time.Clock()

# Function to draw a pixel
def draw_pixel(surface, color, x, y):
    surface.set_at((x, y), color)


# Objects list
objects = []
objects.append(b.ball(np.array([-11, 0, 50], dtype=float), 10, np.array([2000, 2000, 2000], dtype=float)))
objects.append(b.ball(np.array([11, 0, 40], dtype=float), 10, np.array([10000, 0, 0], dtype=float)))
objects.append(b.ball(np.array([-10, 20, 4], dtype=float), 10, np.array([0, 25550, 0], dtype=float)))

cam = c.camera(fov= setFov, pos= np.array([0, 0, -10], dtype=float))



# Main loop
running = True
#while running:
# Handle events
for event in pygame.event.get():
    if event.type == QUIT:
        running = False

# Clear the screen
screen.fill((55,55,80))

# Draw screen
for i in range(width):
    #print(i)
    for j in range(height):
        lightLevel = cam.drawPixel(objects, i - width/2, -(j - height/2))
        #if (any(color > 0 for color in lightLevel)):
            #print(lightLevel)
        # Trækker lysskalaen fra -infty;infty ned til 0;255
        lightLevel = [285/(1 + np.exp(-0.02*(color)+2)) - 30 if color > 0 else 0 for color in lightLevel]
        
        if (any(color > 0 for color in lightLevel)):
            draw_pixel(screen, lightLevel, i, j)

# Update the display
pygame.display.flip()

while running:
    print("banan")

# Quit Pygame
#pygame.quit()
