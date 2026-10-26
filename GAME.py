import pygame

pygame.init()
SCREEN_WIDTH =400
SCREEN_HEIGHT =600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True


class Player:
    def __init__(self):
        self.image = pygame.Surface((34, 24))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(100, screen.get_height() // 2))

        self.velocity_y = 0      
        self.gravity = 0.5       
        self.flap_strength = -8 

    def update(self):
        
        self.velocity_y += self.gravity 
       
        if self.velocity_y > 10:
            self.velocity_y = 10
        self.rect.y += self.velocity_y

        if self.rect.bottom >= SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.velocity_y = 0


    def flap(self):
     # Override the current down-speed to make it launch upward
        self.velocity_y = self.flap_strength

    def draw(self, surface):
        surface.blit(self.image, self.rect)


    

player = Player()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for Flap (Spacebar or Mouse Click)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.flap()
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.flap()

    player.update()
    screen.fill("white")
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()



