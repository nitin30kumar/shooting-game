import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
#screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#class defined for player in the game i.e. you
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.surf = pygame.Surface((75, 25))
        # self.surf.fill((255, 255, 255))
        #image for the player 
        self.surf = pygame.image.load("btnNext.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()

    #update function to update the screen with player current position
    def update(self, pressed_keys):
        #which key is pressed 
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #check whether image goes out of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#class defined for enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # self.surf = pygame.Surface((20,10))
        # self.surf.fill((255,255,255))
        #image for the enemy
        self.surf = pygame.image.load("loader1.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20 , SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        #random speed generated for enemy from 4 to 7
        self.speed = random.randint(4, 7)

    def update(self):
        #- sign for direction of enemy
        self.rect.move_ip(-self.speed, 0)
        #if enemy goes leftmost position it should die
        if self.rect.right < 0:
            self.kill()

#just animation for clouds 
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        #image defined for clouds
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0),RLEACCEL)
        self.rect = self.surf.get_rect(
            center= (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        #update function for updating the cloud current position
    def update(self):
        #- sign for position, 2 for speed
        self.rect.move_ip(-2,0)
        if self.rect.right < 0:
            self.kill()

#setup for sounds
pygame.mixer.init()

#initialize game
pygame.init()

#display position for the game to be displayed
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#add enemy user event
ADDENEMY = pygame.USEREVENT = 1
pygame.time.set_timer(ADDENEMY, 250)

#add cloud user event
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

#Player having a object player
player = Player()

#grouping lots of enemies and clouds in a single frame
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#by default it should be true to continue running
running = True

#setup for the clock
clock = pygame.time.Clock()

#load sound and background music effects in game
pygame.mixer.music.load("music-1.mp3")
pygame.mixer.music.play(loops=-1)

#load all sound files
move_up_sound = pygame.mixer.Sound("music-2.ogg")
move_down_sound = pygame.mixer.Sound("music-3.ogg")
collision_sound = pygame.mixer.Sound("music-4.ogg")

#main loop or program under this game
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        #add enemy
        elif event.type== ADDENEMY:
            #Create new enemy
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        #Add cloud
        elif event.type == ADDCLOUD:
            #create a cloud newly
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()

        #stop any moving sounds
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        #stop the loop
        running = False


# screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    #screen.blit(player.surf, player.rect)
    pygame.display.flip()

    #maintains a frame rate of 30 frames per second
    clock.tick(50)
