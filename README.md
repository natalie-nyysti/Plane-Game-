# Plane-Game-
This is a game I am creating to learn about Pygame. 
It is basically an airplane version of Flappy Bird.
Here is a video of the game in action 



https://github.com/user-attachments/assets/8bf754d3-37d4-457f-8fe4-12b555dcfc60





<h3>The Game </h3>
<h4> Game Area</h4>
The first thing I did when I was building this game was to create the game area itself. I watched a YouTube video that talked through the basics, and after a bit of trial and error, I figured out how I wanted the area to look. 
     
      
      pygame.init()  # Initialize Pygame's modules before using them.
      SCREEN_WIDTH = 350  # Width of the game window in pixels.
      SCREEN_HEIGHT = 600  # Height of the game window in pixels.
      screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the window.
      clock = pygame.time.Clock()  # Controls the game's frame rate.


      while running:

    # Handle window closing and player flap input.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        pygame.quit()  # Release Pygame resources when the main loop ends.


<h4> background</h4>
Next, I wanted to add the background and have it move. I found the background the game has on Google, then just added it. Most of the rest of the graphics I traced from images online. I have all the files here so that they are easy to access. I added the background by first creating a function to load an image and resize it to specifications. Then I called it so that I could load my background image. Then I used the math feature to calculate how many backgrounds I would need to make it continuous. 
           
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
                "ENTER PATH HERE",
                (SCREEN_WIDTH, SCREEN_HEIGHT), (110, 190, 235),
            )
            tiles = math.ceil(SCREEN_WIDTH / bg.get_width()) + 1
            # Load the ground strip and calculate how many copies span the screen.
           

<h4>ground</h4>
I used the same process as the background to create the continuous ground. I did spend some time adjusting the height of the ground so that it looked right. 

       grass = load_image(
                      "ENTER PATH HERE", (SCREEN_WIDTH, 120),
                      (55, 150, 55), scale_to=(SCREEN_WIDTH, 120), #grass height
                      )
                grass_tiles = math.ceil(SCREEN_WIDTH / grass.get_width()) + 1
                GROUND_COLLISION_HEIGHT = 20  # Collision remains limited to the bottom of the grass.

<h4>Classes</h4>
Next, I created the classes. This game has 4 classes: Player, Enemy, Mountain, and Explosion. I made each of these elements a class so that it would be easier to alter them and handle collisions. 

<h5>Class Player</h5>

The player class is the class that controls our player in the game. The graphic I picked for the player is a C-130 airplane because it is one of my friends' favorites. I loaded the planes atributes using the __init___ fuction. using this i added the rectangle size along some checks for later in the game.  


      def __init__(self):
              self.image = load_image(
                  "ENTER PATH HERE",
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

Then I created the gravity logic for the plane so it would fall similar to the bird in Flappy Bird 
           
             def update(self):
        # Apply gravity, cap falling speed, and move the player vertically.
        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10
        self.rect.y += self.velocity_y
Then I made it so that the plane would stay in the window of the game  # Stop the player from leaving the top of the window.
        
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0

        # Keep the player above the ground at the bottom of the window.
        if self.rect.bottom >= SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.velocity_y = 0
        self.hitbox.center = self.rect.center  # Keep collision area aligned to the sprite.
Then I added the flapping logic 
          
          def flap(self):
        # Replace the current vertical speed with an upward impulse.
        self.velocity_y = self.flap_strength

Also, some of the crashing logic is in the player class as well, but I will go over that once I get into the crash logic. 


<h5>Enemy Class</h5>
Most of the logic of this class is the same as the logic of the player, so I won't rehash it too much. One thing I did have to change between the Player and the enemy logic is having the spawn at random integers with random heights. 

     update(self):
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

<h5>Mountain Class</h5>

This is similar to the other two, except it only spawns at one height and moves at the speed of the ground. 

 
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


<h5> Explosion Class</h5>

This class was created so that when a player hits something, there is an explosion. I made it so that the explosion would show up where the hit happened, then I made it so that it would only last for a certain amount of time. class Explosion:
    
    image = None

    def __init__(self, center):
        if Explosion.image is None:
            Explosion.image = load_image(
                "ENTER PATH HERE",
                (140, 140), (255, 180, 0), scale_to=(140, 140),
               
                )
            
        self.rect = Explosion.image.get_rect(center=center)
        self.start_time = pygame.time.get_ticks()
        self.duration = 700

    def update(self):
        return pygame.time.get_ticks() - self.start_time < self.duration

    def draw(self, surface):
        surface.blit(Explosion.image, self.rect)


along with the explosion class i also created this fuction to trigger the explosion 

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

        
<h4>Varibles</h4>
Over the process of building the game, I added some variables and initial conditions to help here; this is the list. i might have3 missed some but I tried to get as many as I could find so they would be easier to find and know what they do. 

      player = Player()  # Create the controllable character.
      enemies = [Enemy(speed) for speed in (3, 4, 5)]  # Planes travel at different speeds.
      mountains = [Mountain()]  # Create a mountain obstacle.
      explosions = []  # Active collision effects.
      game_over = False  # Becomes true after a collision and pauses game updates.
      game_over_font = pygame.font.Font(None, 48)  # Font for the end-of-game message.
      
      explosion_active = False  # Prevent repeated explosions for the same collision.
      scroll = 0  # Horizontal offsetused to animate the repeating background.
    grass_scroll = 0  # Horizontal offset used to animate the ground.a
    GRASS_SPEED = 2  # Shared horizontal speed for the grass and mountains.

<h4>Crash logic </h4>
I have two different crashes in this game: the first is player vs. enemy, and the second is player vs. mountain or ground. 

<h5> Player vs Enemy </h5>


<h4> The Main fuction</h4>
This is where the game comes to life. 



      
      
      
      
      
      
      
      
      
      
      
