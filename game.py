import pygame, math, random
from pygame.locals import *

vec = pygame.math.Vector2
height = 500
width = 500
if __name__ == '__main__':
    pygame.init()
    display = pygame.display.set_mode((height, width))
    pygame.display.set_caption("UFO Fighters")

class Bullet(pygame.sprite.Sprite):
    # This constructor is called in the Player class' update function
    # It spawns a bullet at the player's coordinates and moves straight forward
    def __init__(self, speed, x, y, image):
        super(Bullet, self).__init__()
        self.image = image
        self.surface = pygame.image.load(image)
        self.rect = self.surface.get_rect()
        self.speed = vec(speed[0]*1.5, speed[1]*1.5)
        self.rect.x = x + 7
        self.rect.y = y + 7

    # This is called in the "while open" loop
    def update(self):
        # This updates each bullet's position using its speed vector
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        # If a bullet hits a boundary it will be destroyed
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > width:
            self.kill()
        if self.rect.bottom > height:
            self.kill()
        if self.rect.top < 18:
            self.kill()

        # If a bullet hits the enemy player, it will destroy itself and deduct a life from the enemy
        if self.image == "bullet1.png":
            if self.rect.colliderect(player2.rect):
                self.kill()
                player2.lives -= 1
        if self.image == "bullet2.png":
            if self.rect.colliderect(player1.rect):
                self.kill()
                player1.lives -=1


class Player(pygame.sprite.Sprite):
    lives = 5

    # This is the Player constructor, which is called to create 2 players before the game starts
    # This determines the player's controls, spawn coordinates, speed, and all sprites associated with it
    def __init__(self, left, right, image, shoot, x, y, speed, bullet, lives_img):
        super(Player, self).__init__()
        self.image = image
        self.surface = pygame.image.load(self.image)
        self.rect = self.surface.get_rect()
        self.left = left
        self.right = right
        self.shoot = shoot
        self.speed = vec(0, speed)
        self.rect.x = x
        self.rect.y = y
        self.bullet_image = bullet
        self.counter = lives_img

    # This is called in the "while open" loop
    def update(self, function):
        # This updates each player's position with their velocity vectors
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # It will also rotate or shoot upon their input
        if function[self.left]:
            self.speed = self.speed.rotate(-10)
        if function[self.right]:
            self.speed = self.speed.rotate(10)
        if function[self.shoot]:
            if len(self.bullets) < 2:
                bullet = Bullet(self.speed, self.rect.x, self.rect.y, self.bullet_image)
                self.bullets.add(bullet)
        # If a player touches a powerup sprite, they will gain a life
        if pygame.sprite.spritecollide(self, powerups, False):
            if self.lives < 5:
                self.lives += 1
        # This keeps the player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 18:
            self.rect.top = 18
        if self.rect.bottom > height:
            self.rect.bottom = height

    # This will display how many lives each player has at the top of the screen
    # This is called in the "while open" loops
    def livescounter(self):
        if self.image == "ufo1.png":
            for lives in range(0, self.lives):
                display.blit(pygame.image.load(self.counter), ((29*lives), 0))
        if self.image == "ufo2.png":
            for lives in range(0, self.lives + 1):
                display.blit(pygame.image.load(self.counter), (width - (29*lives), 0))


class Powerup(pygame.sprite.Sprite):
    # This determines a powerup's sprite and spawn location
    def __init__(self):
        super(Powerup, self).__init__()
        self.surface = pygame.image.load("heart.png")
        self.rect = self.surface.get_rect()
        self.rect.x = random.randrange(width - 30)
        self.rect.y = random.randrange(18, height - 30)
    # If the powerup is touched by a player, it will despawn
    def update(self):
        if pygame.sprite.spritecollide(self, players, False):
            self.kill()

powerups = pygame.sprite.Group()
if __name__ == '__main__':

    player1 = Player(K_a, K_d, "ufo1.png", K_w, 0, height, -5, "bullet1.png", "ufo1small.png")
    player2 = Player(K_LEFT, K_RIGHT, "ufo2.png", K_UP, width, 0, 5, "bullet2.png", "ufo2small.png")


    players = pygame.sprite.Group(player1, player2)

    player1.bullets = pygame.sprite.Group()
    player2.bullets = pygame.sprite.Group()


    clock = pygame.time.Clock()
    powerspawn = pygame.USEREVENT + 1
    pygame.time.set_timer(powerspawn, 15000)
    gameover = pygame.USEREVENT + 2


    open = True
    # The game will start immediately after opening it
    while open:
        clock.tick(30)
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if pressed[K_ESCAPE]:
                open = False
            elif event.type == QUIT:
                open = False
            elif event.type == gameover:
                open = False

            elif event.type == powerspawn:
                powerup = Powerup()
                powerups.add(powerup)


        display.blit(pygame.image.load("space.png"),(0, 0))


        for sprite in players:
            sprite.update(pressed)
            sprite.livescounter()
            display.blit(sprite.surface, [sprite.rect.x, sprite.rect.y])
            if sprite.lives < 1:
                sprite.kill()
                pygame.time.set_timer(gameover, 3000)


        for sprite in powerups:
            sprite.update()
            display.blit(sprite.surface, [sprite.rect.x, sprite.rect.y])

        for sprite in player1.bullets:
            sprite.update()
            display.blit(sprite.surface, [sprite.rect.x, sprite.rect.y])

        for sprite in player2.bullets:
            sprite.update()
            display.blit(sprite.surface, [sprite.rect.x, sprite.rect.y])


        pygame.display.flip()
