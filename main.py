__version__ = "0.5"
import pygame
from pygame.locals import *
import math
from copy import deepcopy
import os

# load all levels
from games import games
print(f'INFO: got {len(games)} games')

art_folder = os.path.abspath('.') + '/artwork/'

DRAW_EVERY_NTH_FRAME = 5 # Affects time eye closed
EYE_OPEN_RATIO = 99/100  # ratio of (time eyes open) / time

tut_color        = (4  , 204, 253)
win_color        = (0  , 255, 0  )
lose_color       = (255, 0  , 0  )
background_color = (45 ,  30, 15 )
board_nr_color   = (15 ,  0 , 15 )
board_nr_color_greyed = (150,  135 , 150)

# random number generator settings
RNG_A = 75
RNG_C = 74
RNG_M = (1 << 16) + 1

def rng(seed):
    return (RNG_A * seed + RNG_C) % RNG_M


def setup_screen():
    pygame.init()
    info = pygame.display.Info()
    screen_size = info.current_w, info.current_h

    if 'ANDROID_ARGUMENT' in os.environ:
        print('INFO: running on android')
        SCREEN_WIDTH, SCREEN_HEIGHT = screen_size
    else:
        print('INFO: running on desktop')
        SCREEN_HEIGHT = screen_size[1]*5//7
        SCREEN_WIDTH = SCREEN_HEIGHT//3*2

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Kartoffelspiel')
    return screen, SCREEN_WIDTH, SCREEN_HEIGHT

def generate_scalable_drawable(size):
    images = {}
    kartoffel_image = pygame.image.load(art_folder + 'kartoffel.png').convert_alpha()
    images['potato'] = pygame.transform.scale(kartoffel_image, (size, size))
    kartoffel_stoned_image = pygame.image.load(art_folder + 'kartoffel_stoned.png').convert_alpha()
    images['stoned_potato'] = pygame.transform.scale(kartoffel_stoned_image, (size, size))
    kartoffel_winky_image = pygame.image.load(art_folder + 'kartoffel_winky.png').convert_alpha()
    images['winky_potato'] = pygame.transform.scale(kartoffel_winky_image, (size, size))

    hole_image = pygame.image.load(art_folder + 'hole.jpg').convert()
    images['hole'] = pygame.transform.scale(hole_image, (size, size))
    active_hole_image = pygame.image.load(art_folder + 'active_hole.jpg').convert()
    images['active_hole'] = pygame.transform.scale(active_hole_image, (size, size))

    # board number display
    font = pygame.font.Font(None, size)
    glow_image = pygame.image.load(art_folder + 'glow.png').convert()
    glow_image = pygame.transform.scale(glow_image, (size, size))

    board_nr_renders = []
    for i in range(len(games)):
        nr_render = font.render(f'{i+1}', True, board_nr_color)
        rect = nr_render.get_rect(center=(size//2, size//2))
        base = glow_image.copy()
        base.blit(nr_render, rect)
        board_nr_renders.append(base)

    images['btn_nr'] = board_nr_renders
    btn_restart_image = pygame.image.load(art_folder + 'restart_btn.png').convert()
    images['btn_restart'] = pygame.transform.scale(btn_restart_image, (size, size))
    btn_back_image = pygame.image.load(art_folder + 'back_btn.png').convert()
    images['btn_back'] = pygame.transform.scale(btn_back_image, (size, size))
    return images

def generate_fixed_size_drawable(size):
    texts = {}
    font_size = size*2
    font = pygame.font.Font(None, font_size)
    texts['won'] = font.render('WON!', True, win_color)
    texts['lost'] = font.render('LOST!', True, lose_color)

    font_size = size
    font = pygame.font.Font(None, font_size)
    texts['go_next'] = font.render('<tap to go next>', True, win_color)
    texts['restart_lose'] = font.render('<tap to restart>', True, lose_color)

    font_size = int(size/5*4)
    font = pygame.font.Font(None, font_size)
    tutorial_text1 = font.render('tap on a POTATO!', True, tut_color)
    tutorial_text2 = font.render('eat the ONE in between!', True, tut_color)
    tutorial_text3 = font.render('eat ALL but ONE!', True, tut_color)
    texts['tut'] = [tutorial_text1, tutorial_text2, tutorial_text3]

    images = {}

    # board number display
    font = pygame.font.Font(None, size)
    glow_image = pygame.image.load(art_folder + 'glow.png').convert()
    glow_image = pygame.transform.scale(glow_image, (size, size))

    board_nr_renders = []
    for i in range(len(games)):
        nr_render = font.render(f'{i+1}', True, board_nr_color)
        rect = nr_render.get_rect(center=(size//2, size//2))
        base = glow_image.copy()
        base.blit(nr_render, rect)
        board_nr_renders.append(base)

    images['btn_nr'] = board_nr_renders

    board_nr_renders_greyed = []
    for i in range(len(games)):
        nr_render = font.render(f'{i+1}', True, board_nr_color_greyed)
        rect = nr_render.get_rect(center=(size//2, size//2))
        base = glow_image.copy()
        base.blit(nr_render, rect)
        board_nr_renders_greyed.append(base)

    images['btn_nr_grey'] = board_nr_renders_greyed
    return images, texts


def calculate_potato_size(board):
    nw, nh = len(board[0]), len(board)
    potato_size = min(SCREEN_WIDTH//nw, SCREEN_HEIGHT//nh)
    y_offset = max(0, SCREEN_HEIGHT - potato_size*nh)//2
    return potato_size, y_offset, nw, nh 


def reset_board(game_nr):
    global board
    board = deepcopy(games[game_nr])

def save_game_state(fname='.game_state'):
    with open(fname, 'w') as f:
        f.write(f'game_version:{__version__}\n')
        f.write(f'{game_nr}\n')
        f.write(f'{game_nr_reached}\n')            
        f.write(f'{tutorial_state}\n')
        for b in board:
            f.write(','.join(b)+'\n')

def load_game_state(fname='.game_state'):
    global board, game_nr, game_nr_reached, tutorial_state
    new_board = []

    try:
        with open(fname, 'r') as f:
            lines = f.readlines()
            __version_line = lines[0].strip()
            assert __version_line == "game_version:0.5", 'TODO: implement migration'
            game_nr = int(lines[1].strip())
            game_nr_reached = int(lines[2].strip())
            tutorial_state = int(lines[3].strip())
            for line in lines[4:]:
                new_board.append(line.strip().split(','))

        board = new_board
    except FileNotFoundError as e:
        pass



# sound 
pygame.mixer.init()
hmpf = pygame.mixer.Sound(art_folder + "hmpf.wav")
win = pygame.mixer.Sound(art_folder + "win.wav")
lose = pygame.mixer.Sound(art_folder + "lose.wav")

screen, SCREEN_WIDTH, SCREEN_HEIGHT = setup_screen() 

game_nr = 0
game_nr_reached = 0
board = deepcopy(games[game_nr])

# per level
widths = []
heights = []
y_offsets = []
potato_sizes = []
for game in games:
    size, y_offset, w, h = calculate_potato_size(game)
    potato_sizes.append(size)
    widths.append(w)
    heights.append(h)
    y_offsets.append(y_offset)


scalable = {}
for size in set(potato_sizes):
    scalable[size] = generate_scalable_drawable(size)

smallest_potato = min(potato_sizes)
fixed_images, texts = generate_fixed_size_drawable(smallest_potato)

idx_smallest = potato_sizes.index(smallest_potato)
NW_MENU = widths[idx_smallest]
NH_MENU = heights[idx_smallest]

load_game_state()
potato_size, y_offset, W, H = calculate_potato_size(board)

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

level_selection = False


prev_state = deepcopy(board), game_nr
def click_while_playing(pos):
    global can_jump_to, board, selected, tutorial_state, level_selection, prev_state
    x, y = pos
    i, j = int(math.floor(y / potato_size)), int(math.floor(x / potato_size))

    def is_char(i, j, c):
        if 0 <= i < len(board) and 0 <= j < len(board[0]):
            return board[i][j] == c
        return False

    if selected and (i, j) in can_jump_to:
        prev_state = deepcopy(board), game_nr

        i_selected, j_selected = selected
        board[i][j] = "x"
        a = int((i + i_selected) / 2)
        b = int((j + j_selected) / 2)
        board[a][b] = "o"
        board[i_selected][j_selected] = "o"
        selected = None
        can_jump_to = []

        if tutorial_state < 2:
            tutorial_state = 2

        if is_finished(board):
            return True   
        hmpf.play()

    elif is_char(i, j, 'x'):
        selected = (i, j)
        can_jump_to = [(i - 2, j), (i + 2, j), (i, j - 2), (i, j + 2)]

        can_jump_to = [(i, j) for i, j in can_jump_to
                       if H > i >= 0 and W > j >= 0
                       and board[i][j] == "o"]

        can_jump_to = [(a, b) for a, b in can_jump_to
                       if character(between((a, b), selected)) == "x"]
                       
        if tutorial_state == 0 and len(can_jump_to) > 0:
            tutorial_state = 1

    elif is_char(i, j, 'r'):
        reset_board(game_nr)
        selected = False
        can_jump_to = []
    
    elif is_char(i, j, 'l'):
        level_selection = True

    elif is_char(i, j, 'b'):
        prev_board, prev_game_nr = prev_state
        if board != prev_board and prev_game_nr == game_nr:
            board, _ = prev_state

    else:
        selected = None
        can_jump_to = []

    return False

def click_level_selection(pos):
    global game_nr, level_selection, selected, can_jump_to
    selected = False
    can_jump_to = []
    i, j = int(math.floor(pos[0] / smallest_potato)), int(math.floor(pos[1] / smallest_potato))

    supposed_game_nr = i + j*NH_MENU
    if 0 <= supposed_game_nr <= game_nr_reached:
        last_game_nr = game_nr
        game_nr = supposed_game_nr
        level_selection = False

        if last_game_nr != game_nr:
            reset_board(game_nr)

    
def main():
    global tutorial_state, tutorial_state_prev, game_nr, game_nr_reached,\
     level_selection, board, potato_size, H, W, y_offset
    won = False
    finished = False
    running = True

    random_nr = rng(0)
    ticks = 0



    while running:
        need_reedraw = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:

                event.pos = event.pos[0], event.pos[1]-y_offset
                need_reedraw = True

                if not level_selection:
                    if finished:
                        reset_board(game_nr) 
                        potato_size, y_offset, W, H = calculate_potato_size(board)
                        finished = False
                    is_over = click_while_playing(event.pos)
                    if is_over:
                        if check_win(board):
                            win.play()
                            won = True
                            game_nr += 1
                            if game_nr > game_nr_reached:
                                game_nr_reached = game_nr
                            # ugly way to save the next level state when we finish
                            saved_board = deepcopy(board)
                            reset_board(game_nr)
                            save_game_state()
                            board = saved_board

                        else:
                            lose.play()
                            won = False
                        finished = True
                else:
                    click_level_selection(event.pos)
                    potato_size, y_offset, W, H = calculate_potato_size(board)

        # drawing stuff 
        if (need_reedraw or (ticks % DRAW_EVERY_NTH_FRAME == 0)):

            pygame.display.get_surface().fill(background_color)

            if not level_selection:
                random_nr = draw_board_and_potatoes(random_nr, finished, won)

                if tutorial_state < 3:
                    tut = texts['tut'][tutorial_state]
                    mid_x, mid_y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
                    mid_text_x, mid_text_y = tut.get_width()//2, tut.get_height()//2 
                    screen.blit(tut, (mid_x - mid_text_x, mid_y - potato_size - mid_text_y))

                    t = pygame.time.get_ticks()
                    if tutorial_state_prev != tutorial_state:
                        tut_timer_start = t

                    if tutorial_state == 2:
                        if t - tut_timer_start > 4000:
                            tutorial_state = 3 # finished
                    tutorial_state_prev = tutorial_state

                if finished:
                    draw_end_text(won)
            else:
                draw_level_selection()

            pygame.display.flip()

        ticks += 1
        pygame.time.wait(30)

    if finished:
        reset_board(game_nr)
    save_game_state()


def draw_level_selection():
    for i in range(len(games)):
        x, y = i % NW_MENU * smallest_potato , i // NW_MENU * smallest_potato + y_offset
        if i <= game_nr_reached:
            screen.blit(fixed_images['btn_nr'][i], (x, y))
        else:
            screen.blit(fixed_images['btn_nr_grey'][i], (x, y))


def draw_board_and_potatoes(random_nr, finished, won):
    images = scalable[potato_size]
    for j, row in enumerate(board):
        for i, c in enumerate(row):
            random_nr = rng(random_nr)
            x, y = potato_size * i, potato_size * j
            y += y_offset
            if c in "xo":
                if (j, i) in can_jump_to:
                    screen.blit(images['active_hole'], (x, y))
                else:
                    screen.blit(images['hole'], (x, y))

            if c == "x":
                if random_nr >= EYE_OPEN_RATIO * RNG_M:
                    screen.blit(images['winky_potato'], (x, y))
                elif finished and not won:
                    screen.blit(images['stoned_potato'], (x, y))
                else:
                    screen.blit(images['potato'], (x, y))

            elif c == 'r':
                screen.blit(images['btn_restart'], (x, y))
            
            elif c == 'b':
                screen.blit(images['btn_back'], (x, y))

            elif c == 'l':
                if won and finished:
                    screen.blit(images['btn_nr'][game_nr-1], (x, y))
                else:
                    screen.blit(images['btn_nr'][game_nr], (x, y))

    return random_nr


def draw_end_text(won):
    mid_x = SCREEN_WIDTH//2
    mid_y = SCREEN_HEIGHT//2

    if won:
        screen.blit(texts['won'], (mid_x-texts['won'].get_width()//2, 0))
        screen.blit(texts['go_next'], (mid_x-texts['go_next'].get_width()//2, texts['won'].get_height()))
    else:
        screen.blit(texts['lost'], (mid_x-texts['lost'].get_width()//2, 0))
        screen.blit(texts['restart_lose'], 
            (mid_x-texts['restart_lose'].get_width()//2, texts['lost'].get_height()))


if __name__ == "__main__":
    main()
