import pygame
import random

pygame.init()

width = 800
height = 480

player = (140, 42, 6)
red = (255, 0, 0)

walk_right = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
walk_left = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]
background = pygame.image.load('Game/bg.jpg')
standing = pygame.image.load('Game/standing.png')
enemy = pygame.image.load('Game/enemy1.png')
music = pygame.mixer.music.load('game/music.mp3')

Font = pygame.font.SysFont('footlight', 35)

player_size_left = [[18, 48], [24, 46], [19, 46], [23, 46], [24, 47], [24, 46], [24, 47], [26, 47], [22, 47], [28, 48]]
player_size_right = [[20, 47], [20, 46], [20, 46], [24, 46], [20, 47], [20, 46], [22, 47], [22, 47], [20, 47]]

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Falling Stones')

clock = pygame.time.Clock()


def drop_enemies(enemy_list, enemy_size, player_pos):
    a = 0
    delay = random.random()
    if len(enemy_list) < 8 and delay < 0.06:
        x_pos = random.randint(0, width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])
    for x in enemy_list:
        if x[0] == player_pos[0]:
            a = 1
            break
    if a != 1 and delay < 0.03:
        enemy_list.append([player_pos[0], 0])





def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        gameDisplay.blit(enemy, (enemy_pos[0], enemy_pos[1]))
        # pygame.draw.rect(gameDisplay, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_pos(enemy_list, score, speed):
    for index, enemy_pos in enumerate(enemy_list):
        if (enemy_pos[1] >= 0) and (enemy_pos[1] < height):
            enemy_pos[1] += speed
        else:
            score += 1
            enemy_list.pop(index)
    return score


def check_collision(enemy_list, player_pos, right, left, step, enemy_size):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos, right, left, step, enemy_size):
            return True
    return False


def detect_collision(player_pos, enemy_pos, right, left, step, enemy_size):
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    p_x = player_pos[0]
    p_y = player_pos[1]
    if left:
        player_size = player_size_left[step]
    elif right:
        player_size = player_size_right[step]
    else:
        player_size = player_size_left[9]

    if ((e_x >= p_x) and (e_x <= (p_x + player_size[0]))) or ((p_x >= e_x) and (p_x <= (e_x + enemy_size))):
        if ((e_y >= p_y) and e_y <= (p_y + player_size[1])) or ((p_y >= e_y) and p_y <= (e_y + enemy_size)):
            return True
    return False


def draw_sprites(left, right, player_pos, step):
    if left:
        gameDisplay.blit(walk_left[step], (player_pos[0], player_pos[1]))
        step += 1
    elif right:
        gameDisplay.blit(walk_right[step], (player_pos[0], player_pos[1]))
        step += 1
    else:
        gameDisplay.blit(standing, (player_pos[0], player_pos[1]))
    if step > 8:
        step = 0
    return step


def set_level(score, speed):
    if score < 10:
        speed = 6
    elif score < 20:
        speed = 8
    elif score < 40:
        speed = 10
    elif score < 70:
        speed = 12
    elif score < 90:
        speed = 15
    elif score < 115:
        speed = 18
    elif score < 150:
        speed = 20
    elif score < 200:
        speed = 22
    else:
        speed = 25
    return speed

def end_screen(msg, x, y):
    label = Font.render(msg, 1, red)
    gameDisplay.blit(label, (x,y))


def game_loop():

    player_pos = [width / 2, height - 50]

    enemy_size = 19
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    enemy_list = [enemy_pos]

    right = False
    left = False
    step = 0

    game_exit = False
    game_over = False

    increment = 0
    speed = 6
    score = 0

    pygame.mixer.music.play(-1, start=1)

    while not game_exit:

        while game_over:
            pygame.time.wait(1000)
            pygame.mixer.music.play(-1)
            gameDisplay.fill((200, 245, 245))
            score_text = "Score = " + str(score)
            end_screen(score_text , width/2 - 90, height/2 - 80)
            msg = "Game over !!!"
            end_screen(msg, width/2 - 125, height/2 - 35)
            msg = "Press c to play again or q to quit"
            end_screen(msg, width/2 - 250, height/2 + 10)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    increment = -12
                    left = True
                    right = False
                    enemy_size = 23
                elif event.key == pygame.K_RIGHT:
                    increment = 12
                    right = True
                    left = False
                    enemy_size = 25


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    increment = 0
                    right = False
                    left = False
                    step = 0
                    enemy_size = 25

        player_pos[0] += increment
        if player_pos[0] <= 0:
            player_pos[0] = 0
        elif player_pos[0] >= (width - 32):
            player_pos[0] = width - 32

        gameDisplay.blit(background, (0, 0))
        drop_enemies(enemy_list, enemy_size, player_pos)
        score = update_enemy_pos(enemy_list, score, speed)
        speed = set_level(score, speed)
        text = 'Score:' + str(score)
        label = Font.render(text, 1, (255, 255, 255))
        gameDisplay.blit(label, (width - 200, height - 50))

        if check_collision(enemy_list, player_pos, right, left, step, enemy_size):
            game_over = True

        draw_enemies(enemy_list)
        step = draw_sprites(left, right, player_pos, step)
        clock.tick(30)
        pygame.display.update()

game_loop()


