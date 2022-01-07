import pygame
import os

class Player(object):
    walkRight = [pygame.image.load(os.path.join('images', 'sprite1', f'R{x}.png')) for x in range(1,10)]
    walkLeft = [pygame.image.load(os.path.join('images', 'sprite1', f'L{x}.png')) for x in range(1,10)]
    
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.vel = 5
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 100
        self.maxHealth = self.health
        self.visible = True
    
    def draw(self, win):
        if self.walkCount >= 27:
            self.walkCount= 0
        if not(self.standing):
            if self.left:
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x,self.y))
            else:
                win.blit(self.walkLeft[0], (self.x,self.y))
        pygame.draw.rect(win, (0,0,0), (self.hitbox[0], self.hitbox[1] - 10, self.hitbox[2], 5))
        pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 10, round(self.hitbox[2] * self.health/self.maxHealth), 5))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
    
    def hit(self):
        print('player hit')
        self.health -= 1

class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    walkRight = [pygame.image.load(os.path.join('images', 'enemy1', f'R{x}E.png')) for x in range(1,12)]
    walkLeft = [pygame.image.load(os.path.join('images', 'enemy1', f'L{x}E.png')) for x in range(1,12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = x
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 100
        self.maxHealth = self.health
        self.visible = True
    
    def draw(self, win):
        self.move()
        if self.visible == True:
            if self.walkCount >= 33:
                self.walkCount= 0
            if self.vel < 0:
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (0,0,0), (self.hitbox[0], self.hitbox[1] - 10, self.hitbox[2], 5))
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 10, round(self.hitbox[2] * self.health/self.maxHealth), 5))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.end:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.start:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    
    def hit(self):
        # hitSound.play()
        if self.health > 5:
            self.health -= 5
        else:
            self.visible = False
        print('enemy hit')

def bulletHitBox(bullet, box):
    if (bullet.y - bullet.radius < box[1] + box[3] and bullet.y + bullet.radius > box[1]) and (bullet.x - bullet.radius < box[0] + box[2] and bullet.x + bullet.radius > box[0]):
        return True
    else:
        return False

def boxHitBox(box1, box2):
    if (box1[1] < box2[1] + box2[3] and box1[1] + box1[3] > box2[1]) and (box1[0] < box2[0] + box2[2] and box1[0] + box1[2] > box2[0]):
        return True
    else:
        return False