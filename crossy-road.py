#Gain access to the pygame library
import pygame

#Screen size
SCREEN_TITLE = 'Crossy RPG' 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
#Colors according to rgb codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
#Clock used to update game events and frames
clock = pygame.time.Clock()
# Font for in game text
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:
    #Typical rate of 60, equivalent to FPS
    TICK_RATE = 60    
    
    #Initializer for game class to set up width, height and title
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        #create the window of specified size in which to display the game
        self.game_screen = pygame.display.set_mode((width, height))
        #set the game window color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        # Load and set background image
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
        
    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        enemy_0 = EnemyCharacter('enemy.png', 20, 600, 50, 50)
        # Speed increased as we advance in difficulty
        enemy_0.SPEED *= level_speed

        # Create another enemy
        enemy_1 = EnemyCharacter('enemy.png', self.width - 40, 400, 50, 50)
        enemy_1.SPEED *= level_speed

        # Create another enemy
        enemy_2 = EnemyCharacter('enemy.png', 20,200, 50, 50)
        enemy_2.SPEED *= level_speed
        
        treasure = GameObject('treasure.png', 375, 50, 50, 50) 

        #Main game loop, used to update all gameplay. Runs until is_game_over = True
        while not is_game_over:

            #gets all the events occuring at any given time
            for event in pygame.event.get():
            #If there is a quit type event - exit out of loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # Move up if up key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    # Move down if down key is pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                print(event)
                
                # Redraw the background
                self.game_screen.fill(WHITE_COLOR)
                self.game_screen.blit(self.image, (0, 0))

                # Draw the treasure
                treasure.draw(self.game_screen)
                
                # Update the player position
                player_character.move(direction, self.height)
                # Draw the player at the new position
                player_character.draw(self.game_screen)

                # Move and draw enemy position
                enemy_0.move(self.width)
                enemy_0.draw(self.game_screen)

                # Move and draw more enemies when we reach a higher level
                if level_speed > 2:
                    enemy_1.move(self.width)
                    enemy_1.draw(self.game_screen)
                if level_speed > 4:
                    enemy_2.move(self.width)
                    enemy_2.draw(self.game_screen)

                # End game if collision between player and enemy or treasure
                # Close game if we lose and restart game loop if we win
                if player_character.detect_collision(enemy_0):
                    is_game_over = True
                    did_win = False
                    text = font.render('You Lose!', True, BLACK_COLOR)
                    self.game_screen.blit(text, (275, 350))
                    pygame.display.update()
                    clock.tick(1)
                    break
                elif player_character.detect_collision(treasure):
                    is_game_over = True
                    did_win = True
                    text = font.render('You Win!', True, BLACK_COLOR)
                    self.game_screen.blit(text, (275, 350))
                    pygame.display.update()
                    clock.tick(1)
                    break

            #update all game graphics
            pygame.display.update()
            #Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

        # Restart game loop if we win
        # Break out of game loop if we lose
        if did_win:
            self.run_game_loop(level_speed + 0.5)
        else:
            return

# Generic game object class to be subclassed by other objects in the game
class GameObject:

    def __init__(self, image_path, x, y, width, height):
        # Player image import and resize
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))

        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height
        
    # Draw the object by blitting it onto the background(game_screen)
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

# Class to represent the character controlled by the player
class PlayerCharacter(GameObject):

        # How many tiles the character moves per second
        SPEED = 10

        def __init__(self, image_path, x, y, width, height):
            super().__init__(image_path, x, y, width, height)

        # Move function will move character up if direction > 0 and down if < 0
        def move(self, direction, max_height):
            if direction > 0:
                self.y_pos -= self.SPEED
            elif direction < 0:
                self.y_pos += self.SPEED
            # Make sure character never goes past the bottom of the screen
            if self.y_pos >= max_height - 40:
                self.y_pos = max_height - 40

        # Return False (no collision) if y positions and x positions do not overlap
        # Return True when x and y positions overlap
        def detect_collision(self, other_body):
            if self.y_pos > other_body.y_pos + other_body.height:
                return False
            elif self.y_pos + self.height < other_body.y_pos:
                return False

            if self.x_pos > other_body.x_pos + other_body.width:
                return False
            elif self.x_pos + self.width < other_body.x_pos:
                return False
            
            return True

# Class to represent the enemy characters not controlled by the player
class EnemyCharacter(GameObject):

        # How many tiles the character moves per second
        SPEED = 10

        def __init__(self, image_path, x, y, width, height):
            super().__init__(image_path, x, y, width, height)

        # Move function will move enemy right and left automatically
        def move(self, max_width):
            if self.x_pos <= 20:
                self.SPEED = abs(self.SPEED)
            elif self.x_pos >= max_width - 40:
                self.SPEED = -abs(self.SPEED)
            self.x_pos += self.SPEED
                
# Initialize pygame
pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

# Quit pygame and the program
pygame.quit()
quit()

# Draw the player image on top of the screen at (x, y) position
# game_screen.blit(player_image, (375, 375))
