from threading import Event

import pygame
from pygame.examples.moveit import HEIGHT
from pygame.version import PygameVersion
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
BG = pygame.image.load(os.path.join('download (1).png'))
BG  =pygame.transform.scale(BG, (WIDTH, HEIGHT))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Galactic Warfare!')
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
YELLOW_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS =  10

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Grenade.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('BULLET_FIRE_SOUND.wav'))
GAME_OVER = pygame.mixer.Sound(os.path.join('gameOver.mp3'))

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (70, 50)
YELLOW_SPACESHIP = pygame.image.load(os.path.join('yello_spaceship.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
GREEN_SPACESHIP = pygame.image.load(os.path.join('green_spaceship.jpeg'))
GREEN_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

def draw_window(yellow, green, yellow_bullets, green_bullets, yellow_health, green_health):
    WIN.blit(BG, (0,0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    yellow_health_text = HEALTH_FONT.render("Health: "+ str(yellow_health), 1, WHITE)
    green_health_text = HEALTH_FONT.render("Health: "+ str(green_health), 1, WHITE)
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))
    WIN.blit(green_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(GREEN_SPACESHIP_IMAGE, (green.x, green.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x -VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x +VEL +yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y -VEL > 0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y +VEL + yellow.height < HEIGHT - 15:  # down
        yellow.y += VEL

def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_LEFT]  and green.x -VEL > BORDER.x + BORDER.width:  # LEFT
        green.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and green.x +VEL +green.width < WIDTH:  # RIGHT
        green.x += VEL
    if keys_pressed[pygame.K_UP] and green.y -VEL > 0:  # Down
        green.y -= VEL
    if keys_pressed[pygame.K_DOWN] and green.y +VEL + green.height < HEIGHT :  # UP
        green.y += VEL


def handle_bullets(yellow_bullets, green_bullets, yellow, green):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            green_bullets.remove(bullet)
        elif bullet.x < 0:
            green_bullets.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow = pygame.Rect(10, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(840, 290, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    clock = pygame.time.Clock()

    yellow_health = 10
    green_health = 10
    green_bullets = []
    yellow_bullets = []

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y + green.height // 2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()
            if event.type == GREEN_HIT:
                green_health -=1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Green Won!"
            pygame.time.delay(1000)
            GAME_OVER.play()

        if green_health <=0:
            winner_text = "Yellow Won!"
            pygame.time.delay(1000)
            GAME_OVER.play()

        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        green_handle_movement(keys_pressed, green)

        handle_bullets(yellow_bullets, green_bullets, yellow, green)

        draw_window(yellow, green, yellow_bullets, green_bullets, green_health, yellow_health)

    main()

if __name__ == "__main__":
    main()