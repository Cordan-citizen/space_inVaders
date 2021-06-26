import pygame
import random
import math
from pygame import mixer

# Инициализация модулей Pygame
pygame.init()

# Создание окна. Обязательно добавить скобки внутри скобок
screen = pygame.display.set_mode((800, 600))

# Добавдение фонового изображения
background = pygame.image.load('image/background/bkg.png')

# background-музыка
mixer.music.load('sounds/background/background.mp3')
mixer.music.play(-1)

# Иконка и заголовок
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('icon/ufo.png')
pygame.display.set_icon(icon)

# Добавление игрока на экран
playerImg = pygame.image.load('image/player/player.png') 
playerX = 370
playerY = 480
playerX_change = 0

# Добавление врага на экран
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('image/enemy/enemy.png')) 
	enemyX.append(random.randint(0, 728))
	enemyY.append(random.randint(0, 150))
	enemyX_change.append(3)
	enemyY_change.append(40)

# Добавление пули на экран
# ready - вы не видите пулю на экране
# fire - пуля движется
bulletImg = pygame.image.load('image/bullet/bullet.png') 
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 50
bullet_state = "ready"

# Счёт очков
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Текст Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


# Функции, добавляющие объекты на экран в определённых координатах
def show_score(x, y):
	score = font.render('Счёт: ' +  str(score_value), True, (255, 255, 255))
	screen.blit(score, (x, y))

def game_over_text():
        over_text = over_font.render('Game over :(', True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

def player(x, y):
	screen.blit(playerImg, (x, y))

def enemy(x, y, i):
	screen.blit(enemyImg[i], (x, y))

def bullet(x, y):
	screen.blit(bulletImg, (x, y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x + 20, y + 10))
def isCollision(enemyY, enemyX, bulletY, bulletX):
	distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
	if distance < 27:
		return True
	else:
		return False

# Цикл while, который позволяет закрыть окно по нажатию на крестик
running = True
while running:
	# Изменение цвета экрана RGB
	screen.fill((19, 7, 30))

	# Фон
	screen.blit(background, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# Проверка нажатия клавиш влево/вправо, пробел
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -25
			if event.key == pygame.K_RIGHT:
				playerX_change = 25
			if event.key == pygame.K_SPACE:
				if bullet_state is 'ready':
					bulletX = playerX
					bullet_Sound = mixer.Sound('sounds/laser/laser.mp3')
					bullet_Sound.play()
					fire_bullet(bulletX, bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0

	playerX += playerX_change

	# Границы движения корабля справа и слева
	if playerX <= 0:
		playerX = 0
	elif playerX >= 727.5:
		playerX = 727.5

	# Границы движения противника
	for i in range(num_of_enemies):
		# Game over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break
		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] = 10
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 727.5:
			enemyX_change[i] = -10
			enemyY[i] += enemyY_change[i]
		# Столкновение
		collision = isCollision(enemyY[i], enemyX[i], bulletY, bulletX)
		if collision:
			explosion_Sound = mixer.Sound('sounds/explosion/explosion.mp3')
			explosion_Sound.play()
			bulletY = 480
			bullet_state = 'ready'
			score_value += 1
			enemyX[i] = random.randint(0, 728)
			enemyY[i] = random.randint(0, 150)
		enemy(enemyX[i], enemyY[i], i)

	# Обновление и движение пули
	if bulletY <= -20:
		bulletY = 480
		bullet_state = 'ready'

	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	player(playerX, playerY)
	show_score(textX, textY)
	# Обновление экрана
	pygame.display.update()
