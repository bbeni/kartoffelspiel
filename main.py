__version__ = "0.2"
import pygame
from pygame.locals import *
import math
from copy import deepcopy
import os


games = []
# o is empty
# x is potato
# . is nothing
# r is restart_btn
# s is save_btn
# l is load_btn

'''
gamee  = [[".", "r", "o", "o", "o", "l", "s"],
          [".", ".", "o", "o", "o", ".", "."],
          ["o", "o", "o", "o", "o", "o", "o"],
          ["o", "o", "o", "o", "o", "o", "o"],
          ["o", "o", "o", "o", "o", "o", "o"],
          [".", ".", "o", "o", "o", ".", "."],
          [".", ".", "o", "o", "o", ".", "."]]
'''

games.append([["s", ".", "o", "x", "o", ".", "."],
              ["l", ".", "o", "x", "o", ".", "."],
              ["o", "o", "o", "o", "o", "o", "o"],
              ["o", "o", "o", "o", "o", "o", "o"],
              ["o", "o", "o", "x", "o", "o", "o"],
              ["r", ".", "o", "x", "o", ".", "."],
              [".", ".", "o", "o", "o", ".", "."]])

games.append([["s", ".", "o", "x", "o", ".", "."],
              ["l", ".", "o", "x", "o", ".", "."],
              ["o", "o", "o", "o", "o", "o", "o"],
              ["o", "o", "o", "o", "o", "o", "o"],
              ["o", "o", "o", "x", "x", "o", "o"],
              ["r", ".", "o", "x", "o", ".", "."],
              [".", ".", "o", "o", "o", ".", "."]])

games.append([["s", ".", "o", "x", "o", ".", "."],
              ["l", ".", "o", "x", "o", ".", "."],
              ["o", "o", "o", "o", "o", "o", "o"],
              ["o", "o", "o", "o", "o", "o", "o"],
              ["o", "o", "o", "x", "x", "o", "o"],
              ["r", ".", "x", "x", "o", ".", "."],
              [".", ".", "o", "o", "o", ".", "."]])

games.append([["s", ".", "o", "o", "o", ".", "."],
              ["l", "o", "o", "x", "o", "o", "."],
              ["o", "o", "o", "x", "o", "o", "o"],
              ["o", "x", "x", "x", "x", "x", "o"],
              ["o", "o", "o", "x", "o", "o", "o"],
              ["r", "o", "o", "x", "o", "o", "."],
              [".", ".", "o", "o", "o", ".", "."]])

games.append([["s", ".", "o", "o", "o", ".", "."],
              ["l", "o", "x", "o", "o", "o", "."],
              ["o", "o", "x", "x", "o", "o", "o"],
              ["o", "o", "x", "x", "x", "o", "o"],
              ["o", "o", "x", "x", "o", "o", "o"],
              ["r", "o", "x", "o", "o", "o", "."],
              [".", ".", "o", "o", "o", ".", "."]])

games.append([["s", ".", "o", "o", "x", ".", "."],
              ["l", ".", "o", "x", "x", ".", "."],
              ["o", "o", "o", "x", "o", "x", "o"],
              ["x", "x", "x", "o", "x", "o", "o"],
              ["o", "o", "o", "x", "o", "o", "o"],
              ["r", ".", "o", "o", "o", ".", "."],
              [".", ".", "o", "o", "o", ".", "."]])

games.append([["s", ".", "x", "x", "x", ".", "."],
              ["l", ".", "x", "x", "x", ".", "."],
              ["x", "x", "x", "x", "x", "x", "x"],
              ["x", "x", "x", "o", "x", "x", "x"],
              ["x", "x", "x", "x", "x", "x", "x"],
              ["r", ".", "x", "x", "x", ".", "."],
              [".", ".", "x", "x", "x", ".", "."]])

games.append([["s", ".", "x", "x", "x", ".", "."],
              ["l", "x", "x", "x", "x", "x", "."],
              ["x", "x", "x", "o", "x", "x", "x"],
              ["x", "x", "x", "x", "x", "x", "x"],
              ["x", "x", "x", "x", "x", "x", "x"],
              ["r", "x", "x", "x", "x", "x", "."],
              [".", ".", "x", "x", "x", ".", "."]])


game_nr = 0
board = deepcopy(games[game_nr])

pygame.init()
info = pygame.display.Info()
WIDTH = min(info.current_w, info.current_h)

W = len(board)
H = len(board[0])

POTATO_SIZE = WIDTH//W # 125 # in pixels
SCREEN_WIDTH = POTATO_SIZE*W
SCREEN_HEIGHT = POTATO_SIZE*H

# offset everything
TOP_OFFSET = 0
# we are probably on mobile portrait
if info.current_w < info.current_h:
    TOP_OFFSET = info.current_h - info.current_w 
    TOP_OFFSET = TOP_OFFSET//2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+TOP_OFFSET))
pygame.display.set_caption('Kartoffelspiel')


art_folder = os.path.abspath('.') + '/artwork/'

kartoffel_image = pygame.image.load(art_folder + 'kartoffel.png').convert_alpha()
kartoffel_image = pygame.transform.scale(kartoffel_image, (POTATO_SIZE, POTATO_SIZE))
kartoffel_stoned_image = pygame.image.load(art_folder + 'kartoffel_stoned.png').convert_alpha()
kartoffel_stoned_image = pygame.transform.scale(kartoffel_stoned_image, (POTATO_SIZE, POTATO_SIZE))

hole_image = pygame.image.load(art_folder + 'hole.jpg').convert()
hole_image = pygame.transform.scale(hole_image, (POTATO_SIZE, POTATO_SIZE))
active_hole_image = pygame.image.load(art_folder + 'active_hole.jpg').convert()
active_hole_image = pygame.transform.scale(active_hole_image, (POTATO_SIZE, POTATO_SIZE))


pygame.mixer.init()
hmpf = pygame.mixer.Sound(art_folder + "hmpf.wav")
win = pygame.mixer.Sound(art_folder + "win.wav")
lose = pygame.mixer.Sound(art_folder + "lose.wav")


win_color = (0,255,0)
lose_color = (255,0,0)

font_size = POTATO_SIZE*2
font = pygame.font.Font(None, font_size)
lost_text = font.render('LOST!', True, lose_color)
won_text = font.render('WON!', True, win_color)

font_size = POTATO_SIZE//2
font = pygame.font.Font(None, font_size)
restart_text_win = font.render('<tap anywhere to go next>', True, win_color)
restart_text_lose = font.render('<tap anywhere to restart>', True, lose_color)

tut_color = (24,2,253)
font_size = int(POTATO_SIZE/4*3)
font = pygame.font.Font(None, font_size)
tutorial_text1 = font.render('select a POTATO by tapping!', True, tut_color)
tutorial_text2 = font.render('eat the ONE in between!', True, tut_color)
tutorial_text3 = font.render('there can be only ONE POTATO!', True, tut_color)
tutorial_texts = [tutorial_text1, tutorial_text2, tutorial_text3]


# buttons
btn_load_image = pygame.image.load(art_folder + 'load_saved_btn.png').convert()
btn_save_image = pygame.image.load(art_folder + 'save_btn.png').convert()
btn_restart_image = pygame.image.load(art_folder + 'restart_btn.png').convert()
btn_load_image = pygame.transform.scale(btn_load_image, (POTATO_SIZE, POTATO_SIZE))
btn_save_image = pygame.transform.scale(btn_save_image, (POTATO_SIZE, POTATO_SIZE))
btn_restart_image = pygame.transform.scale(btn_restart_image, (POTATO_SIZE, POTATO_SIZE))


def between(pos1, pos2):
    a = int((pos1[0] + pos2[0]) / 2)
    b = int((pos1[1] + pos2[1]) / 2)
    return a, b

def character(pos):
    a, b = pos
    return board[a][b]

def has_neigbour_h(board, pos, char):
    x, y = pos
    for nx in [x+1, x-1]:
        if nx < 0 or nx >= len(board):
            continue
        if board[nx][y] == char:
            return True
    return False

def has_neigbour_v(board, pos, char):
    x, y = pos
    for ny in [y+1, y-1]:
        if ny < 0 or ny >= len(board[0]):
            continue
        if board[x][ny] == char:
            return True
    return False

def is_finished(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 'x':
                continue
            if has_neigbour_h(board, (i,j), 'o') and has_neigbour_h(board, (i,j), 'x'):
                return False
            if has_neigbour_v(board, (i,j), 'o') and has_neigbour_v(board, (i,j), 'x'):
                return False
    return True

def check_win(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x':
                count += 1
    if count == 1:
        return True
    return False


selected = None
can_jump_to = []

tutorial_state_prev = -1
tutorial_state = 0

def click(pos):
    global can_jump_to, board, selected, tutorial_state
    x, y = pos
    i, j = int(math.floor(x / POTATO_SIZE)), int(math.floor(y / POTATO_SIZE))

    def is_char(i, j, c):
        if 0 <= i < len(board) and 0 <= j < len(board[0]):
            return board[i][j] == c
        return False

    if selected and (i, j) in can_jump_to:
        i_selected, j_selected = selected
        board[i][j] = "x"
        a = int((i + i_selected) / 2)
        b = int((j + j_selected) / 2)
        board[a][b] = "o"
        board[i_selected][j_selected] = "o"
        selected = None
        can_jump_to = []

        if is_finished(board):
            return True
        hmpf.play()

        if tutorial_state < 2:
            tutorial_state = 2


    elif is_char(i, j, 'x'):
        selected = (i, j)
        can_jump_to = [(i - 2, j), (i + 2, j), (i, j - 2), (i, j + 2)]
        can_jump_to = [(i, j) for i, j in can_jump_to
                       if W > i >= 0 and j < H and j >= 0
                       and board[i][j] == "o"]
        can_jump_to = [(a, b) for a, b in can_jump_to
                       if character(between((a, b), selected)) == "x"]
        if tutorial_state == 0 and len(can_jump_to) > 0:
            tutorial_state = 1

    elif is_char(i, j, 'r'):
        reset_board(game_nr)
        selected = False
        can_jump_to = []
    
    elif is_char(i, j, 's'):
        save()

    elif is_char(i, j, 'l'):
        load()
        selected = False
        can_jump_to = []

    else:
        selected = None
        can_jump_to = []

    return False


def reset_board(game_nr):
    global board
    board = deepcopy(games[game_nr])

def save(fname='.board_state'):
    with open(fname, 'w') as f:
        f.write(f'{game_nr}\n')
        for b in board:
            f.write(','.join(b)+'\n')
  
def load(fname='.board_state'):
    global board, game_nr
    new_board = []
    try:
        with open(fname, 'r') as f:
            lines = f.readlines()
            game_nr = int(lines[0].strip())
            for line in lines[1:]:
                new_board.append(line.strip().split(','))
        board = new_board
    except:
        pass
    
def main():
    global tutorial_state, tutorial_state_prev, game_nr
    won = False
    finished = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_AC_BACK:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                event.pos = event.pos[0], event.pos[1]-TOP_OFFSET
                if finished:
                    reset_board(game_nr)
                    finished = False
                is_over = click(event.pos)
                if is_over:
                    if check_win(board):
                        win.play()
                        won = True
                        game_nr += 1
                    else:
                        lose.play()
                        won = False
                    finished = True


        for i, row in enumerate(board):
            for j, c in enumerate(row):
                x, y = POTATO_SIZE * i, POTATO_SIZE * j
                y += TOP_OFFSET
                if c in "xo":
                    if (i, j) in can_jump_to:
                        screen.blit(active_hole_image, (x, y))
                    else:
                        screen.blit(hole_image, (x, y))

                if c == "x":
                    if finished and not won:
                        screen.blit(kartoffel_stoned_image, (x, y))
                    else:
                        screen.blit(kartoffel_image, (x, y))
                elif c == 'r':
                    screen.blit(btn_restart_image, (x, y))   
                elif c == 'l':
                    screen.blit(btn_load_image, (x, y))   
                elif c == 's':
                    screen.blit(btn_save_image, (x, y))   

        if tutorial_state < 3:
            tut = tutorial_texts[tutorial_state]
            mid_x, mid_y = SCREEN_WIDTH//2, TOP_OFFSET//2
            mid_text_x, mid_text_y = tut.get_width()//2, tut.get_height()//2 
            screen.blit(tut, (mid_x - mid_text_x, mid_y - POTATO_SIZE//2 - mid_text_y))


            t = pygame.time.get_ticks()
            
            if tutorial_state_prev != tutorial_state:
                tut_timer_start = t

            if tutorial_state == 2:
                if t - tut_timer_start > 3500:
                    tutorial_state = 3
                    
            tutorial_state_prev = tutorial_state



        if finished:
            mid_x, mid_y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + TOP_OFFSET//2
            mid_restart_x, mid_restart_y = restart_text_win.get_width()//2, won_text.get_height()//2 
                
            if won:
                mid_win_x, mid_win_y = won_text.get_width()//2, won_text.get_height()//2
                screen.blit(won_text, (mid_x - mid_win_x, mid_y - mid_win_y))
                screen.blit(restart_text_win, (mid_x - mid_restart_x, mid_y + mid_win_y) )

            else:
                mid_lose_x, mid_lose_y = won_text.get_width()//2, won_text.get_height()//2
                screen.blit(lost_text, (mid_x - mid_lose_x, mid_y - mid_lose_y))
                screen.blit(restart_text_lose, (mid_x - mid_restart_x, mid_y + mid_lose_y))

        pygame.display.flip()
        pygame.display.get_surface().fill((0, 0, 0))
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
