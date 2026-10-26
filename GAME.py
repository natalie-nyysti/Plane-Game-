import pygame  
import math  
import random  

pygame.init()  # Initialize Pygame's modules before using them.
SCREEN_WIDTH = 350  # Width of the game window in pixels.
SCREEN_HEIGHT = 600  # Height of the game window in pixels.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the window.
clock = pygame.time.Clock()  # Controls the game's frame rate.
running = True  # Keep the main loop running until the player closes the window.
scroll = 0  # Horizontal offsetused to animate the repeating background.
grass_scroll = 0  # Horizontal offset used to animate the ground.a
GRASS_SPEED = 2  # Shared horizontal speed for the grass and mountains.

def load_image(path, fallback_size, fallback_color, scale_to=None, alternatives=()):
    # Try the requested image path and any alternate paths, in order.
    for filename in (path, *alternatives):
        try:
            image = pygame.image.load(filename).convert_alpha()
            # Resize the image when requested, otherwise keep its original size.
            return pygame.transform.scale(image, scale_to) if scale_to else image
        except (pygame.error, OSError):
            # Continue to the next path if the file cannot be opened or decoded.
            pass
    # Draw a solid-color placeholder so the game can still run without its art files.
    image = pygame.Surface(fallback_size, pygame.SRCALPHA)
    image.fill(fallback_color)
    return image
 
# Load the sky and calculate enough copies to cover the window while scrolling.
bg = load_image(
    "/Users/natalienyysti/Desktop/ENGENERING/python projects 2026/sky1.png",
    (SCREEN_WIDTH, SCREEN_HEIGHT), (110, 190, 235),
)
tiles = math.ceil(SCREEN_WIDTH / bg.get_width()) + 1
# Load the ground strip and calculate how many copies span the screen.
grass = load_image(
    "/Users/natalienyysti/Downloads/grass.png", (SCREEN_WIDTH, 120),
    (55, 150, 55), scale_to=(SCREEN_WIDTH, 120), #grass height
)
grass_tiles = math.ceil(SCREEN_WIDTH / grass.get_width()) + 1
GROUND_COLLISION_HEIGHT = 20  # Collision remains limited to the bottom of the grass.

class Player:
    # The player can flap upward and is kept within the top and bottom screen bounds.
    def __init__(self):
        self.image = load_image(
            "/Users/natalienyysti/Desktop/ENGENERING/python projects 2026/C130.png",
            (86, 60), (60, 60, 60), scale_to=(86, 60),
        )
        self.image = pygame.transform.flip(self.image, True, False)  # Face the other way.
        # The visible sprite and collision hitbox are separate rectangles.
        self.rect = pygame.Rect(0, 0, 86, 44)
        self.rect.center = (100, screen.get_height() // 2)
        self.hitbox = pygame.Rect(0, 0, 70, 34)
        self.hitbox.center = self.rect.center

        self.velocity_y = 0  # Current vertical speed; negative values move upward.
        self.gravity = 0.5  # Pulls the player downward each frame.
        self.flap_strength = -8  # Upward speed applied when the player flaps.
        self.crashed = False
        self.crash_velocity_y = 0
        self.crash_angle = 0

    def update(self):
        # Apply gravity, cap falling speed, and move the player vertically.
        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10
        self.rect.y += self.velocity_y

        # Stop the player from leaving the top of the window.
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0

        # Keep the player above the ground at the bottom of the window.
        if self.rect.bottom >= SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.velocity_y = 0
        self.hitbox.center = self.rect.center  # Keep collision area aligned to the sprite.

    def start_crash(self):
        if not self.crashed:
            self.crashed = True
            self.crash_velocity_y = 1

    def update_crash(self):
        # Continue the motion while the crash is drawn, so the plane visibly tumbles and lands.
        self.crash_velocity_y = min(self.crash_velocity_y + 0.45, 9)
        self.rect.x -= 1
        self.rect.y += self.crash_velocity_y
        self.crash_angle -= .5
        if self.rect.bottom >= SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.crash_velocity_y = 0
            self.crash_angle -= 4
        self.hitbox.center = self.rect.center

    def flap(self):
        # Replace the current vertical speed with an upward impulse.
        self.velocity_y = self.flap_strength

    def draw(self, surface):
        if self.crashed:
            self.update_crash()
        image = pygame.transform.rotate(self.image, self.crash_angle) if self.crashed else self.image
        surface.blit(image, image.get_rect(center=self.rect.center))


class Enemy:
    # Enemies enter from the right, travel left, and respawn after leaving the screen.
    def __init__(self, speed):
        self.image = load_image(
            "/Users/natalienyysti/Desktop/ENGENERING/python projects 2026/fighter jet .png",
            (78, 44), (190, 55, 55), scale_to=(78, 44),
        )
        self.rect = pygame.Rect(0, 0, 78, 30)  # Visible bounds for positioning.
        self.rect.midleft = (SCREEN_WIDTH, 0)
        self.hitbox = pygame.Rect(0, 0, 62, 22)  # Smaller collision area than the sprite.
        self.hitbox.center = self.rect.center
        self.speed = speed  # Each plane travels at its own speed.
        self.active = False  # Inactive enemies wait until their next spawn time.
        self.next_spawn = pygame.time.get_ticks() + random.randint(800, 2500)
        self.crashed = False
        self.crash_velocity_y = 0
        self.crash_angle = 0

    def update(self):
        now = pygame.time.get_ticks()
        if not self.active:
            # When its timer expires, place the enemy off-screen at a random height.
            if now >= self.next_spawn:
                self.rect.left = SCREEN_WIDTH
                self.rect.centery = random.randint(30, SCREEN_HEIGHT - 30)
                self.hitbox.center = self.rect.center
                self.active = True
            return

        # Move active enemies left and update their collision area.
        self.rect.x -= self.speed
        self.hitbox.center = self.rect.center
        if self.rect.right < 0:
            # Schedule another appearance after this enemy has crossed the screen.
            self.active = False
            self.next_spawn = now + random.randint(800, 2500)

    def start_crash(self):
        if not self.crashed:
            self.crashed = True
            self.crash_velocity_y = 1

    def update_crash(self):
        self.crash_velocity_y = min(self.crash_velocity_y + 0.45, 9)
        self.rect.x -= 1
        self.rect.y += self.crash_velocity_y
        self.crash_angle -= .5
        if self.rect.bottom >= SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.crash_velocity_y = 0
            self.crash_angle -= 4
        self.hitbox.center = self.rect.center

    def draw(self, surface):
        # Only draw enemies that are currently on their active pass.
        if self.active:
            if self.crashed:
                self.update_crash()
            image = pygame.transform.rotate(self.image, self.crash_angle) if self.crashed else self.image
            surface.blit(image, image.get_rect(center=self.rect.center))

class Mountain:
    # Mountains scroll in from the right along the ground as stationary obstacles.
    def __init__(self):
        self.image = load_image(
            "/Users/natalienyysti/Download/moutain1.png",
            (220, 400), (90, 400, 100), scale_to=(220, 400),
            alternatives=("/Users/natalienyysti/Downloads/moutain1.png",),
        )
        self.rect = pygame.Rect(0, 0, 220, 190)  # Visible bounds for positioning.
        self.hitbox = pygame.Rect(0, 0, 180, 150)  # Collision area, slightly inset.
        self.speed = GRASS_SPEED  # Match the grass scroll speed.
        self.active = False  # Wait off-screen until the spawn timer expires.
        self.next_spawn = pygame.time.get_ticks() + random.randint(600, 1600)

    def update(self):
        now = pygame.time.get_ticks()
        if not self.active:
            # Spawn the mountain at the right edge with its base on the ground.
            if now >= self.next_spawn:
                self.rect.left = SCREEN_WIDTH
                self.rect.bottom = 600
                self.hitbox.center = self.rect.center
                self.active = True
            return

        # Move the active obstacle left and keep its hitbox aligned.
        self.rect.x -= self.speed
        self.hitbox.center = self.rect.center
        if self.rect.right < 0:
            # Schedule the next mountain after this one leaves the screen.
            self.active = False
            self.next_spawn = now + random.randint(600, 1600)

    def draw(self, surface):
        # Draw the mountain only while it is active.
        if self.active:
            surface.blit(self.image, self.image.get_rect(center=self.rect.center))


class Explosion:
    
    image = None

    def __init__(self, center):
        if Explosion.image is None:
            Explosion.image = load_image(
                "/Users/natalienyysti/Downloads/ENDEXPL1.png",
                (140, 140), (255, 180, 0), scale_to=(140, 140),
               
                )
            
        self.rect = Explosion.image.get_rect(center=center)
        self.start_time = pygame.time.get_ticks()
        self.duration = 700

    def update(self):
        return pygame.time.get_ticks() - self.start_time < self.duration

    def draw(self, surface):
        surface.blit(Explosion.image, self.rect)

player = Player()  # Create the controllable character.
enemies = [Enemy(speed) for speed in (3, 4, 5)]  # Planes travel at different speeds.
mountains = [Mountain()]  # Create a mountain obstacle.
explosions = []  # Active collision effects.
game_over = False  # Becomes true after a collision and pauses game updates.
game_over_font = pygame.font.Font(None, 48)  # Font for the end-of-game message.

explosion_active = False  # Prevent repeated explosions for the same collision.

def trigger_explosion(center):
    global explosion_active
    if not explosion_active:
        explosions.append(Explosion(center))
        player.start_crash()
        # Also crash the enemy involved in the collision.
        for enemy in enemies:
            if enemy.active and enemy.hitbox.colliderect(player.hitbox):
                enemy.start_crash()
        explosion_active = True

# Main loop: process input, update objects, draw the frame, and cap the frame rate.
while running:

    # Handle window closing and player flap input.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.flap()
        elif not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            player.flap()

    # Update the player only while the game is still in progress.
    if not game_over:
        player.update()
        # The top edge of the grass acts as a solid collision boundary.
        if player.hitbox.bottom >= SCREEN_HEIGHT - GROUND_COLLISION_HEIGHT:
            player.start_crash()
            game_over = True
    # Draw adjacent copies of the sky to create a continuous scrolling background.
    for i in range(tiles):
        screen.blit(bg, (bg.get_width() * i + scroll, 0))
    scroll -= 2  # Move the background left each frame.
    if scroll <= -bg.get_width():
        scroll += bg.get_width()  # Wrap the offset when one background tile passes.
    grass_scroll -= GRASS_SPEED  # Move the ground at the same speed as the mountains.
    if grass_scroll <= -grass.get_width():
        grass_scroll += grass.get_width()

    # Update enemies and end the game if one hits the player.
    for enemy in enemies:
        if not game_over:
            enemy.update()

            if enemy.active and player.hitbox.colliderect(enemy.hitbox):
                trigger_explosion(player.rect.center)
                game_over = True
    # Update mountains; they do not trigger explosions or end the game.
    for mountain in mountains:
        if not game_over:
            mountain.update()

    # Keep explosions animating and remove them after their duration.
    explosions[:] = [explosion for explosion in explosions if explosion.update()]

    # Draw the ground as repeating tiles along the bottom edge.
    for i in range(grass_tiles):
        screen.blit(grass, (grass.get_width() * i + grass_scroll, SCREEN_HEIGHT - grass.get_height()))

    # Draw the player and all obstacles over the background and ground.
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for mountain in mountains:
        mountain.draw(screen)
    for explosion in explosions:
        explosion.draw(screen)
    if game_over:
        # Display the end-state message after a collision.
        message = game_over_font.render("Game Over", True, (255, 255, 255))
        screen.blit(message, message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    pygame.display.flip()  # Present the completed frame in the window.
    clock.tick(60)  # Limit updates to 60 frames per second.


pygame.quit()  # Release Pygame resources when the main loop ends.



