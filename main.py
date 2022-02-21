import sqlite3
import pygame
import sys
import random
import datetime
import os

import register_part
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
ex = register_part.MyWidget(app)
ex.show()
app.exec_()
ex.hide()
CONST_K = 1
CONST_TIME = 10
level = ex.return_level()
if level == 1:
    CONST_K = 1
    CONST_TIME *= 1
elif level == 2:
    CONST_K = 2
    CONST_TIME *= 1.5
elif level == 3:
    CONST_K = 3
    CONST_TIME *= 2
CONST_TIME = 10
# CONST_CELL_SIZE = 30
CONST_B = 0
if CONST_K % 2 == 0:
    CONST_B = 1
CONST_CELL_SIZE = 60 // CONST_K
CONST_PLAYER_SHIFT_X = 0 / CONST_K
CONST_PLAYER_SHIFT_Y = 0 / CONST_K
# CONST_PLAYER_SHIFT_X = 0
# CONST_PLAYER_SHIFT_Y = 0
CONST_LABYRINTH_X = 37 * CONST_K + CONST_B
CONST_LABYRINTH_Y = 21 * CONST_K + CONST_B
CONST_LABYRINTH_INDEX_X = CONST_LABYRINTH_X - 1
CONST_LABYRINTH_INDEX_Y = CONST_LABYRINTH_Y - 1
CONST_SECOND_IN_MINUTE = 60
pygame.init()
# size = width, height = 1850, 1050
size = width, height = CONST_CELL_SIZE * CONST_LABYRINTH_X, CONST_CELL_SIZE * CONST_LABYRINTH_Y
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if 'mario.png' in name:
        image = pygame.transform.scale(image, (
            CONST_CELL_SIZE - CONST_PLAYER_SHIFT_X * 2, CONST_CELL_SIZE - CONST_PLAYER_SHIFT_Y * 2))
    else:
        image = pygame.transform.scale(image, (CONST_CELL_SIZE, CONST_CELL_SIZE))
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def generate_map(q, r):
    def start_point_generate():
        return q, r

    def finish_point_generate(n, m):
        return n * 2 - 2, m * 2 - 2

    def transition_choice(x, y, rm):
        """Функция выбора дальнейшего пути в генерации лабиринта"""
        choice_list = []
        if x > 0:
            if not rm[x - 1][y]:
                choice_list.append((x - 1, y))
        if x < len(rm) - 1:
            if not rm[x + 1][y]:
                choice_list.append((x + 1, y))
        if y > 0:
            if not rm[x][y - 1]:
                choice_list.append((x, y - 1))
        if y < len(rm[0]) - 1:
            if not rm[x][y + 1]:
                choice_list.append((x, y + 1))
        if choice_list:
            nx, ny = random.choice(choice_list)
            if x == nx:
                if ny > y:
                    tx, ty = x * 2, ny * 2 - 1
                else:
                    tx, ty = x * 2, ny * 2 + 1
            else:
                if nx > x:
                    tx, ty = nx * 2 - 1, y * 2
                else:
                    tx, ty = nx * 2 + 1, y * 2
            return nx, ny, tx, ty
        else:
            return -1, -1, -1, -1

    def create_labyrinth(n=((CONST_LABYRINTH_Y + 1) // 2), m=((CONST_LABYRINTH_X + 1) // 2)):
        """Генерация лабиринта"""
        reach_matrix = []
        for i in range(n):
            reach_matrix.append([])
            for j in range(m):
                reach_matrix[i].append(False)
        transition_matrix = []
        for i in range(n * 2 - 1):
            transition_matrix.append([])
            for j in range(m * 2 - 1):
                if i % 2 == 0 and j % 2 == 0:
                    transition_matrix[i].append(True)
                else:
                    transition_matrix[i].append(False)
        start = start_point_generate()
        finish = finish_point_generate(n, m)
        list_transition = [start]
        x, y = start
        reach_matrix[x][y] = True
        x, y, tx, ty = transition_choice(x, y, reach_matrix)
        for i in range(1, m * n):
            while not (x >= 0 and y >= 0):
                x, y = list_transition[-1]
                list_transition.pop()
                x, y, tx, ty = transition_choice(x, y, reach_matrix)
            reach_matrix[x][y] = True
            list_transition.append((x, y))
            transition_matrix[tx][ty] = True
            x, y, tx, ty = transition_choice(x, y, reach_matrix)
            '''transition_matrix[q][r] = '@' '''
        return transition_matrix, start, finish

    return create_labyrinth()


def generate_level(level):
    global map
    map = level[0]
    '''finish = level[2]
    start = level[1]'''
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == True:
                Tile('empty', x, y)
            elif map[y][x] == False:
                Tile('wall', x, y)
    Tile('empty', player_coords[0], player_coords[1])
    new_player = Player(player_coords[0], player_coords[1])
    Tile('x', CONST_LABYRINTH_INDEX_X, CONST_LABYRINTH_INDEX_Y)
    return new_player, player_coords[0], player_coords[1]


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png'), 'x': load_image('X.png')}
player_image = load_image('mario.png', -1)
tile_width = tile_height = CONST_CELL_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + CONST_PLAYER_SHIFT_X,
                                               tile_height * pos_y + CONST_PLAYER_SHIFT_Y)

    def update(self, x, y):
        if 0 <= self.rect.y + y < height and 0 <= self.rect.x + x < width and \
                map[(self.rect.y + y) // tile_height][(self.rect.x + x) // tile_width] in (True, '@'):
            self.rect = self.rect.move(x, y)


'''all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
win_flag = False
level_map = None
player, level_x, level_y = generate_level(generate_map())
run = True'''
win_flag = False
player_coords = 0, 0


def main():
    global player_coords
    global win_flag, tiles_group, all_sprites, player_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    '''if level == 1:
        CONST_CELL_SIZE = 30
        CONST_PLAYER_SHIFT_X = 0
        CONST_PLAYER_SHIFT_Y = 0
    elif level == 2:
        CONST_CELL_SIZE = 50
        CONST_PLAYER_SHIFT_X = 15
        CONST_PLAYER_SHIFT_Y = 5
        size = width, height = CONST_CELL_SIZE * CONST_LABYRINTH_X, CONST_CELL_SIZE * CONST_LABYRINTH_Y
        screen = pygame.display.set_mode(size)'''
    player, level_x, level_y = generate_level(generate_map(0, 0))
    run = True
    date1 = datetime.datetime.today()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                win_flag = True
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                player.update(0, tile_height)
            if key[pygame.K_UP]:
                player.update(0, -tile_height)
            if key[pygame.K_LEFT]:
                player.update(-tile_width, 0)
            if key[pygame.K_RIGHT]:
                player.update(tile_width, 0)
        if player.rect.x // CONST_CELL_SIZE == (CONST_LABYRINTH_X - 1) and player.rect.y // CONST_CELL_SIZE == (
                CONST_LABYRINTH_Y - 1):
            '''if level == 1:
                level = 2
                player.rect.x = 0
                player.rect.y = 0
            elif level == 2:
                run = False
                win_flag = True'''
            run = False
            win_flag = True
        player_coords = player.rect.x // CONST_CELL_SIZE, player.rect.y // CONST_CELL_SIZE
        if datetime.datetime.today().second >= (date1 + datetime.timedelta(seconds=CONST_TIME)).second:
            run = False
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()


date_before_start = datetime.datetime.today()
while win_flag is False:
    main()
date_after_end = datetime.datetime.today()
score = int((date_after_end.minute - date_before_start.minute) * CONST_SECOND_IN_MINUTE + (
        date_after_end.second - date_before_start.second))
print(score)

con = sqlite3.connect("score.db")
cur = con.cursor()
score_from_db = cur.execute(
    f"""SELECT score{ex.return_level()} FROM account_scores WHERE name = '{ex.return_name()}'""").fetchall()
if score <= score_from_db[0][0]:
    cur.execute(f"""UPDATE account_scores
                SET score{ex.return_level()} = {score}
                WHERE name = '{ex.return_name()}'""").fetchall()

score_from_db = cur.execute(
    f"""SELECT score{ex.return_level()} FROM account_scores WHERE name = '{ex.return_name()}'""").fetchall()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_TAB]:
            run = False
    font = pygame.font.SysFont(None, 70)
    img = font.render(f'CONGRATULATIONS! YOUR SCORE: {score}. BEST SCORE: {score_from_db[0][0]}', True, (255, 0, 0))
    img2 = font.render(f'Press TAB to quit.', True, (255, 0, 0))
    screen.fill((0, 255, 0))
    screen.blit(img, (475, 325))
    screen.blit(img2, (900, 425))
    pygame.display.flip()
con.commit()
