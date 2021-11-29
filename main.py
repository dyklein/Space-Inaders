import pygame
import random
import math

pygame.init()

SCREEN_X = 800
SCREEN_Y = 600
screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])

# title
pygame.display.set_caption("space invader")
icon = pygame.image.load("space-ship.png")
pygame.display.set_icon(icon)
# background
background = pygame.image.load("space.jpg")

# player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 12
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(100, 650))
    enemyY.append(random.randint(50, 250))
    enemyX_change.append(.5)
    enemyY_change.append(25)


# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 50
bullet_state = "ready"


def player(x, y):
    """Place the player on the screen

    Args:
        x (integer): [x axis]
        y (integer): [y axis]
    """
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    """[summary]

    Args:
        x (integer): [x axis]
        y (integer): [y axis]
        i (integer): [index of the enemay image]
    """
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    """[fires the bullet and tracks where it goes]

    Args:
        x (integer): [x axis]
        y (integer): [y axis]
    """
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 16))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX-bulletX)*(enemyX-bulletX) +
                         (enemyY-bulletY)*(enemyY-bulletY))
    if distance < 27:
        return True
    else:
        return False


#open the high score file
file1 = open("highscore.txt", "r")


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_textX = 10
score_textY = 10

high_score_value = int(file1.read())
high_score_textX = 10
high_score_textY = 50


def show_score(x, y):
    """Show score on board

    Args:
        x (integer): [x axis]
        y (integer): [y axis]
    """
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_high_score(x, y):
    """show the high score on the board

    Args:
        x (integer): [x axis]
        y (integer): [y axis]
    """
    score = font.render(
        "High Score :" + str(high_score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


over_font = pygame.font.Font('freesansbold.ttf', 256)


def game_over():
    """print game over on the screen and the score of the player
    """
    score = font.render("GAME OVER  " + "Score :" +
                        str(score_value), True, (255, 255, 255))
    screen.blit(score, (200, 250))


# game loop
running = True
lost = False
while running:
    # color background
    screen.fill((0, 0, 0))
    # add background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            file1.close()
            if score_value >= high_score_value:
                file2 = open("highscore.txt", "w")
                file2.write(str(score_value))
                file2.close()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 114:
                file1.close()
                if score_value >= high_score_value:
                    file2 = open("highscore.txt", "w")
                    file2.write(str(score_value))
                    file2.close()
                file1 = open("highscore.txt", "r")
                high_score_value = int(file1.read())
                score_value = 0
                enemyImg.clear()
                enemyX.clear()
                enemyY.clear()
                enemyX_change.clear()
                enemyY_change.clear()
                for i in range(num_of_enemy):
                    enemyImg.append(pygame.image.load("alien.png"))
                    enemyX.append(random.randint(100, 650))
                    enemyY.append(random.randint(100, 250))
                    enemyX_change.append(.5)
                    enemyY_change.append(25)

        # if key stroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemy):
        # game over
        if len(enemyImg) > 0:
            if enemyY[i] > 440 and enemyX[i] >= 0 and enemyX[i] <= 736:
                enemyImg.clear()
                enemyX.clear()
                enemyY.clear()
                enemyX_change.clear()
                enemyY_change.clear()
                lost = True
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0.0:
                enemyX_change[i] = .5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736.0:
                enemyX_change[i] = -.5
                enemyY[i] += enemyY_change[i]

            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, SCREEN_X)
                enemyY[i] = random.randint(50, 150)

            # fix enemy values
            if enemyX[i] > 736.0 or enemyY[i] < 0.0:
                enemyX[i] = 700

            enemy(enemyX[i], enemyY[i], i)
    if lost == True:
        game_over()
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(score_textX, score_textY)
    if score_value > high_score_value:
        high_score_value = score_value
    show_high_score(high_score_textX, high_score_textY)
    pygame.display.update()
