__version__ = "0.0.1"
import pygame
from pygame.locals import *
import math
from copy import deepcopy

POTATO_SIZE = 115 # in pixels

game1  = [[".", ".", "x", "x", "x", ".", "."],
          [".", "x", "x", "x", "x", "x", "."],
          ["x", "x", "x", "x", "x", "x", "x"],
          ["x", "x", "x", "o", "x", "x", "x"],
          ["x", "x", "x", "x", "x", "x", "x"],
          [".", "x", "x", "x", "x", "x", "."],
          [".", ".", "x", "x", "x", ".", "."]]

game2  = [[".", ".", "x", "x", "x", ".", "."],
          [".", ".", "x", "x", "x", ".", "."],
          ["x", "x", "x", "x", "x", "x", "x"],
          ["x", "x", "x", "o", "x", "x", "x"],
          ["x", "x", "x", "x", "x", "x", "x"],
          [".", ".", "x", "x", "x", ".", "."],
          [".", ".", "x", "x", "x", ".", "."]]

game3 = [["x", "x", "o", "o"],
         ["x", "x", "o", "o"],
         ["x", "x", "o", "o"]]

game_debug  = [[".", ".", "o", "o", "o", ".", "."],
               [".", ".", "o", "o", "o", ".", "."],
               ["o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "x", "o"],
               ["o", "o", "o", "o", "x", "o", "o"],
               [".", ".", "o", "o", "x", ".", "."],
               [".", ".", "o", "o", "o", ".", "."]]


board_original = game2
board = deepcopy(board_original)

W = len(board)
H = len(board[0])

SCREEN_WIDTH = POTATO_SIZE*W
SCREEN_HEIGHT = POTATO_SIZE*H


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCALED|FULLSCREEN)
pygame.display.set_caption('Kartoffelspiel')


kartoffel_image = pygame.image.load('kartoffel.png').convert_alpha()
kartoffel_image = pygame.transform.scale(kartoffel_image, (POTATO_SIZE, POTATO_SIZE))
kartoffel_stoned_image = pygame.image.load('kartoffel_stoned.png').convert_alpha()
kartoffel_stoned_image = pygame.transform.scale(kartoffel_stoned_image, (POTATO_SIZE, POTATO_SIZE))

hole_image = pygame.image.load('hole.jpg').convert()
hole_image = pygame.transform.scale(hole_image, (POTATO_SIZE, POTATO_SIZE))
active_hole_image = pygame.image.load('active_hole.jpg').convert()
active_hole_image = pygame.transform.scale(active_hole_image, (POTATO_SIZE, POTATO_SIZE))


pygame.mixer.init()
hmpf = pygame.mixer.Sound("hmpf.wav")
win = pygame.mixer.Sound("win.wav")
lose = pygame.mixer.Sound("lose.wav")


win_color = (0,255,0)
lose_color = (255,0,0)

font_size = POTATO_SIZE*2
font = pygame.font.Font(None, font_size)
lost_text = font.render('LOST!', True, lose_color)
won_text = font.render('WON!', True, win_color)

font_size = POTATO_SIZE//2
font = pygame.font.Font(None, font_size)
restart_text_win = font.render('<tap anywhere to restart>', True, win_color)
restart_text_lose = font.render('<tap anywhere to restart>', True, lose_color)

tut_color = (24,2,253)
font_size = int(POTATO_SIZE/2)
font = pygame.font.Font(None, font_size)
tutorial_text1 = font.render('select a POTATO by tapping!', True, tut_color)
tutorial_text2 = font.render('eat the ONE in between!', True, tut_color)
tutorial_text3 = font.render('there can be only ONE POTATO!', True, tut_color)
tutorial_texts = [tutorial_text1, tutorial_text2, tutorial_text3]


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


    elif board[i][j] == "x":
        selected = (i, j)
        can_jump_to = [(i - 2, j), (i + 2, j), (i, j - 2), (i, j + 2)]
        can_jump_to = [(i, j) for i, j in can_jump_to
                       if W > i >= 0 and j < H and j >= 0
                       and board[i][j] == "o"]
        can_jump_to = [(a, b) for a, b in can_jump_to
                       if character(between((a, b), selected)) == "x"]
        if tutorial_state == 0 and len(can_jump_to) > 0:
            tutorial_state = 1

    else:
        selected = None
        can_jump_to = []

    return False


def reset_board():
    global board
    board = deepcopy(board_original)

### android stuff
def save(fname='.board_state'):
    try:
        with open(fname, 'w') as f:
            for b in board:
                f.write(','.join(b)+'\n')
    except:
        pass

def load(fname='.board_state'):
    global board
    new_board = []
    try:
        with open(fname, 'r') as f:
            for line in f.readlines():
                new_board.append(line.strip().split(','))
        board = new_board
    except:
        pass
### end android stuff
    
def main():
    global tutorial_state, tutorial_state_prev
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
                if finished:
                    reset_board()
                    finished = False
                is_over = click(event.pos)
                if is_over:
                    if check_win(board):
                        win.play()
                        won = True
                    else:
                        lose.play()
                        won = False
                    finished = True

            elif event.type == APP_WILLENTERBACKGROUND:
                save()

            elif event.type == APP_DIDENTERFOREGROUND:
                load()



        for i, row in enumerate(board):
            for j, c in enumerate(row):
                x, y = POTATO_SIZE * i, POTATO_SIZE * j
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

        if tutorial_state < 3:
            tut = tutorial_texts[tutorial_state]
            mid_x, mid_y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
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
            mid_x, mid_y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
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
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
