import pygame
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Space invaders')

mixer.music.load('Surak - Lullaby.mp3')
mixer.music.play(-1)

playerImg = pygame.image.load('ufo.png')
bulletImg = pygame.image.load('bullet.png')
bg = pygame.image.load('Wallpaper.jpg')
pygame.display.set_icon(playerImg)

playerX = 370
playerY = 512
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemies = 6
flag = 0

for i in range(numEnemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.choice([64, 128, 192]))
    enemyX_change.append(0.2)
    enemyY_change.append(64)

bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

scoreValue = 0
pressEnter = pygame.font.Font('freesansbold.ttf', 16)
font = pygame.font.Font('freesansbold.ttf', 32)
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)
textX = 10
textY = 10


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 16))


def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = (((EnemyX - BulletX) ** 2) + ((EnemyY - BulletY) ** 2)) ** 1/2
    if distance < 64:
        mixer.Sound('invaderkilled.wav').play()
        return True
    return False


def showScore(x, y):
    if enemyY[0] < 1000:
        score = font.render(f'Score : {scoreValue}', True, (0, 0, 255))
        screen.blit(score, (x, y))


def gameOver():
    global flag
    txt = gameOverFont.render('GAME OVER', True, (255, 255, 255))
    screen.blit(txt, (200, 250))
    score = font.render(f'Score : {scoreValue}', True, (0, 0, 255))
    screen.blit(score, (300, 324))
    enter = pressEnter.render('Press Enter to continue...', True, (255, 255, 255))
    screen.blit(enter, (300, 366))

    flag = 1


running = True
while running:
    screen.blit(bg, (-600, -200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_SPACE and flag == 0:
                if bullet_state == 'ready':
                    bulletX = playerX
                    mixer.Sound('shoot.wav').play()
                fire(playerX, bulletY)

            if event.key == pygame.K_RETURN and flag == 1:
                for i in range(numEnemies):
                    enemyX[i] = random.randint(0, 735)
                    enemyY.append(random.choice([64, 128]))
                scoreValue = 0
            flag = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    if playerX > 736:
        playerX = 736

    for i in range(numEnemies):
        enemyX[i] += enemyX_change[i]

        if enemyY[i] > 448:
            for j in range(numEnemies):
                enemyY[j] = 1000
            gameOver()
            break

        if scoreValue < 1000:
            if enemyX[i] < 0:
                enemyX_change[i] = 0.2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] > 736:
                enemyX_change[i] = -0.2
                enemyY[i] += enemyY_change[i]
        else:
            if enemyX[i] < 0:
                enemyX_change[i] = 0.2 + scoreValue/10000
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] > 736:
                enemyX_change[i] = -0.2 - scoreValue/10000
                enemyY[i] += enemyY_change[i]

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bullet_state = 'ready'
            bulletY = 480
            scoreValue += 100
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY < 0:
        bullet_state = 'ready'
        bulletY = 480

    if bullet_state == 'fire':
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    showScore(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
