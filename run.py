import pygame
import os
from helper import Player, Enemy, Projectile, bulletHitBox, boxHitBox
pygame.init()

def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render(f"Score: {player_score:02d}", 1, (0,0,0))
    win.blit(text, (700, 10))
    hero.draw(win)
    enemy1.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

# display
screenWidth, screenHeight = 852, 480
win=pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("First Game")
bg = pygame.image.load(os.path.join('images', 'bg.jpg'))

# sounds
bulletSound = pygame.mixer.Sound(os.path.join('audio', 'bullet.mp3'))
hitSound = pygame.mixer.Sound(os.path.join('audio', 'hit.mp3'))
music = pygame.mixer.music.load(os.path.join('audio', 'music.mp3'))
pygame.mixer.music.play(-1)

# util
clock = pygame.time.Clock()
player_score = 0
font = pygame.font.SysFont('cambria', 30, True)
cool_down = 0
hero = Player(300, 410, 64, 64)
enemy1 = Enemy(200, 417, 64, 64, 400)
bullets = []
run = True

#mainloop
while run:
    clock.tick(27)

    if cool_down > 0:
        cool_down -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    for bullet in bullets:
        if bulletHitBox(bullet, enemy1.hitbox) and enemy1.visible:
            hitSound.play()
            enemy1.hit()
            player_score += 1
            bullets.pop(bullets.index(bullet))
        elif bullet.x < screenWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if enemy1.visible and boxHitBox(hero.hitbox, enemy1.hitbox):
        hero.hit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and cool_down == 0:
        bulletSound.play()
        if hero.left:
            facing = -1
        else:
            facing = 1
        
        if len(bullets) < 5: # max projectiles
            bullets.append(Projectile(round(hero.x + hero.width //2), round(hero.y + hero.height //2), 6, (0,0,0), facing))
        
        cool_down = 3

    if keys[pygame.K_LEFT] and hero.x > 0:
        hero.x -= hero.vel
        hero.left, hero.right, hero.standing = True, False, False
    elif keys[pygame.K_RIGHT] and hero.x < screenWidth-(hero.width):
        hero.x += hero.vel
        hero.left, hero.right, hero.standing = False, True, False
    else:
        hero.standing, hero.walkCount = True, 0

    if not(hero.isJump):
        if keys[pygame.K_UP]:
            hero.isJump=True
            hero.standing, hero.walkCount = True, 0
    else:
        if hero.jumpCount > 0:
            hero.y -= (hero.jumpCount ** 2) * 0.5
            hero.jumpCount -= 1
        elif hero.jumpCount >= -10:
            hero.y += (hero.jumpCount ** 2) * 0.5
            hero.jumpCount -= 1
        else:
            hero.isJump=False
            hero.jumpCount = 10
    
    redrawGameWindow()

pygame.quit()
