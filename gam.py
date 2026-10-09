import pygame
from sys import exit
pygame.init()
#intiates pygame
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
Font = pygame.font.Font(None, 36)
Sky_surface = pygame.image.load("/Users/natalienyysti/Desktop/ENGENERING/python projects 2026/Sky.png").convert_alpha()  
scaled_Sky = pygame.transform.scale(Sky_surface, (800, 600))
Ground_surface = pygame.image.load("/Users/natalienyysti/Desktop/ENGENERING/python projects 2026/Ground.jpeg").convert_alpha()
Scaled_Ground = pygame.transform.scale(Ground_surface, (800, 100))
Text_surface = Font.render("Hello, World!", False, 'Black')  # White text
#screen = pygame.display.set_mode((width, height)) creates a window of size 800x600 pixels where the game will be displayed.
plane_surface = pygame.image.load("/Users/natalienyysti/Desktop/ENGENERING/python projects 2026/Fighter jet .png").convert_alpha()
scaled_plane = pygame.transform.scale(plane_surface, (100, 100))

A10_surface = pygame.image.load("/Users/natalienyysti/Desktop/ENGENERING/python projects 2026/A10.png").convert_alpha() 
scaled_A10 = pygame.transform.scale(A10_surface, (100, 100))
C130_surface = pygame.image.load("/Users/natalienyysti/Desktop/ENGENERING/python projects 2026/C130.png").convert_alpha()
C130_x_pos = 500
C130_surface = pygame.transform.scale(C130_surface, (200, 80))
plane_x_pos = 800
A10_x_pos = 100
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(scaled_Sky, (0, 0))
    screen.blit(Scaled_Ground, (0, 500))
    screen.blit(Text_surface, (350, 250))
    plane_x_pos -= 4  
    screen.blit(scaled_plane, (plane_x_pos, 300))
    if plane_x_pos < -100:  # Reset position when the plane goes off-screen
        plane_x_pos = 800

    A10_x_pos -= 4
    screen.blit(scaled_A10, (A10_x_pos, 300))
    if A10_x_pos < -100:  # Reset position when the A10 goes off-screen
        A10_x_pos = 800
    C130_x_pos -= 4
    screen.blit(C130_surface, (C130_x_pos, 300))     
    if C130_x_pos < -200:  # Reset position when the C130 goes off-screen
        C130_x_pos = 800  
    # draw all elements
    #update the display
    pygame.display.update()
    clock.tick(60)  # Limit the frame rate to 60 frames per second

 