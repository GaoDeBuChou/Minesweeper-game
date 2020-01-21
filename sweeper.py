import random
import sys
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


def bomber(length, width, bomb, m, n):
    """
    Place bombs randomly (position of first click and its surroundings cannot be bombs)
    :param length: length of the board
    :param width: width of the board
    :param bomb: number of bombs
    :param m: horizontal position of first click
    :param n: vertical position of first click
    :return: list of bomb positions
    """
    forbidden = ((m - 1, n - 1), (m - 1, n), (m - 1, n + 1), (m, n - 1), (m, n), (m, n + 1), (m + 1, n - 1), (m + 1, n),
                 (m + 1, n + 1))
    candidates = [(x, y) for x in range(length) for y in range(width) if (x, y) not in forbidden]
    return random.sample(candidates, bomb)


def get_cal(length, width, bombs):
    """
    Get numbers of non-bomb positions
    :param length: length of the board
    :param width: width of the board
    :param bombs: list of bomb positions
    :return: matrix of numbers
    """
    cals = [[0 for _ in range(width)] for _ in range(length)]
    for i in range(length):
        for j in range(width):
            if (i, j) not in bombs:
                tests = [(m, n) for m in (i - 1, i, i + 1) for n in (j - 1, j, j + 1)]
                cals[i][j] = sum([t in bombs for t in tests])
    return cals


def position(mouse_x, mouse_y, length, width):
    """
    Get the position on the board representing the mouse click
    :param mouse_x: horizontal position of mouse click
    :param mouse_y: vertical position of mouse click
    :param length: length of the board
    :param width: width of the board
    :return: position on the board
    """
    x, y = (mouse_x - 20) // 15, (mouse_y - 40) // 15
    if 0 <= x < length and 0 <= y < width:
        return x, y
    return -1, -1


def expand(x, y, cals, shown, length, width):
    """
    Expand empty position with no bombs surrounded
    :param x: horizontal position
    :param y: vertical position
    :param cals: matrix of numbers
    :param shown: list of positions shown
    :param length: length of the board
    :param width: width of the board
    :return: modified list of positions shown
    """
    for m in (x - 1, x, x + 1):
        for n in (y - 1, y, y + 1):
            if 0 <= m < length and 0 <= n < width:
                if (m != x or n != y) and (m, n) not in shown:
                    shown.append((m, n))
                    if cals[m][n] == 0:
                        expand(m, n, cals, shown, length, width)
    return shown


def doubleclick(x, y, bombs, cal, flags):
    """
    Shortcut for double click
    :param x: horizontal position of the click
    :param y: vertical position of the click
    :param bombs: list of bomb positions
    :param cal: number of the position
    :param flags: list of flags
    :return: status after the double click (0 for wrong judgment, 1 for right judgment, -1 for invalid double click),
             list of positions to expand (empty list for status 0 or -1)
    """
    tests = [(m, n) for m in (x - 1, x, x + 1) for n in (y - 1, y, y + 1) if (m, n) not in flags]
    if cal == 9 - len(tests):
        for t in tests:
            if t in bombs:
                return 0, []
        return 1, tests
    return -1, []


def main():
    length, width, bomb = 9, 9, 10  # length of the board, width of the board, number of bombs
    pygame.init()
    fps, fps_clock = 30, pygame.time.Clock()
    displaysurf = pygame.display.set_mode((length * 15 + 40, width * 15 + 60 + 20), 0, 32)
    pygame.display.set_caption("Minesweeper")

    one_img = pygame.image.load("img/1.bmp")
    two_img = pygame.image.load("img/2.bmp")
    three_img = pygame.image.load("img/3.bmp")
    four_img = pygame.image.load("img/4.bmp")
    five_img = pygame.image.load("img/5.bmp")
    six_img = pygame.image.load("img/6.bmp")
    seven_img = pygame.image.load("img/7.bmp")
    eight_img = pygame.image.load("img/8.bmp")
    flag_img = pygame.image.load("img/flag.bmp")
    notsure_img = pygame.image.load("img/notsure.bmp")
    imgs = (one_img, two_img, three_img, four_img, five_img, six_img, seven_img, eight_img)

    font1 = pygame.font.SysFont("simsunnsimsun", 15)
    time1 = font1.render("Time: 0", True, BLACK, GREY)
    rect1 = time1.get_rect()
    rect1.center = (50, 20)
    bomb1 = font1.render("Bombs: 0", True, BLACK, GREY)
    rect2 = bomb1.get_rect()
    rect2.center = (length * 15 - 10, 20)
    easy1 = font1.render("Easy", True, GREEN, GREY)
    rect3 = easy1.get_rect()
    rect3.center = (30, width * 15 + 50)
    normal1 = font1.render("Norm", True, YELLOW, GREY)
    rect4 = normal1.get_rect()
    rect4.center = (80, width * 15 + 50)
    hard1 = font1.render("Hard", True, RED, GREY)
    rect5 = hard1.get_rect()
    rect5.center = (130, width * 15 + 50)

    difficulty, game, bombed = 1, 2, False  # 1 easy, 2 normal, 3 hard; 0 game ends, 1 game continues, 2 game starts
    bombs, shown = [], []  # list of bomb positions, list of positions shown
    time, second = 0, 0
    cals = [[0 for _ in range(width)] for _ in range(length)]  # initialize matrix of numbers
    flags, notsure = [], []  # list of flags, list of question marks
    red = (-1, -1)  # bombing point

    while True:
        displaysurf.fill(GREY)
        for i in range(length + 1):
            pygame.draw.line(displaysurf, BLACK, (20 + i * 15, 40), (20 + i * 15, 40 + width * 15), 1)
        for i in range(width + 1):
            pygame.draw.line(displaysurf, BLACK, (20, 40 + i * 15), (20 + length * 15, 40 + i * 15), 1)
        for i, j in shown:
            cal = cals[i][j]
            if cal == 0:
                pygame.draw.rect(displaysurf, WHITE, (21 + i * 15, 41 + j * 15, 14, 14), 0)
            else:
                displaysurf.blit(imgs[cal - 1], (22 + i * 15, 42 + j * 15))
        for i, j in flags:
            displaysurf.blit(flag_img, (22 + i * 15, 42 + j * 15))
        for i, j in notsure:
            displaysurf.blit(notsure_img, (22 + i * 15, 42 + j * 15))

        if bombed:
            for i, j in bombs:
                pygame.draw.circle(displaysurf, BLACK, (28 + i * 15, 48 + j * 15), 6)
            pygame.draw.circle(displaysurf, RED, (28 + red[0] * 15, 48 + red[1] * 15), 6)

        if game == 0 and not bombed:  # win
            bomb = 0
            for i, j in bombs:
                pygame.draw.rect(displaysurf, GREEN, (21 + i * 15, 41 + j * 15, 14, 14))
                pygame.draw.circle(displaysurf, BLACK, (28 + i * 15, 48 + j * 15), 6)

        time1 = font1.render("Time: " + str(second), True, BLACK, GREY)
        displaysurf.blit(time1, rect1)
        bomb1 = font1.render("Bombs: " + str(bomb), True, BLACK, GREY)
        displaysurf.blit(bomb1, rect2)
        displaysurf.blit(easy1, rect3)
        displaysurf.blit(normal1, rect4)
        displaysurf.blit(hard1, rect5)

        if game != 0:
            time += 1
            if time % 30 == 0:
                second += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x, y = position(mouse_x, mouse_y, length, width)
                pressed = pygame.mouse.get_pressed()  # indices 0 for left click, 1 for middle click, 2 for right click
                if 0 <= x < length and 0 <= y < width:
                    if pressed[0] and pressed[2]:  # shortcut for double click
                        if game == 1 and cals[x][y] > 0 and (x, y) in shown:
                            temp, to_expands = doubleclick(x, y, bombs, cals[x][y], flags)
                            if temp == 0:  # wrong judgment, game over
                                pygame.mixer.music.load("aud/001.wav")
                                pygame.mixer.music.play()
                                bombed, game = True, 0
                                red = (-10, -10)  # do not show red
                            if temp == 1:  # right judgment, expand surroundings
                                for m, n in to_expands:
                                    if 0 <= m < length and 0 <= n < width:
                                        if (m, n) not in bombs and (m, n) not in shown:
                                            shown.append((m, n))
                                            if cals[m][n] == 0:
                                                shown = expand(m, n, cals, shown, length, width)
                                if length * width - len(shown) == len(bombs):  # win if all non-bomb positions are shown
                                    pygame.mixer.music.load("aud/002.mid")
                                    pygame.mixer.music.play()
                                    game = 0
                    if pressed[0] and not pressed[2]:  # left click
                        if game == 1:
                            if (x, y) not in shown and (x, y) not in flags and (x, y) not in notsure:
                                if (x, y) in bombs:  # click the bomb
                                    pygame.mixer.music.load("aud/001.wav")
                                    pygame.mixer.music.play()
                                    bombed, game = True, 0
                                    red = (x, y)
                                else:
                                    shown.append((x, y))
                                    if cals[x][y] == 0:  # no bombs surrounded
                                        shown = expand(x, y, cals, shown, length, width)
                            if length * width - len(shown) == len(bombs):  # win if all non-bomb positions are shown
                                pygame.mixer.music.load("aud/002.mid")
                                pygame.mixer.music.play()
                                game = 0
                        elif game == 2:  # new game
                            game = 1
                            bombs = bomber(length, width, bomb, x, y)
                            cals = get_cal(length, width, bombs)  # store numbers of non-bomb positions
                            shown.append((x, y))
                            shown = expand(x, y, cals, shown, length, width)  # expand surroundings
                        else:  # restart
                            game, bombed = 2, False
                            if difficulty == 1:
                                length, width, bomb = 9, 9, 10
                            elif difficulty == 2:
                                length, width, bomb = 16, 16, 40
                            else:
                                length, width, bomb = 16, 30, 99
                            bombs, shown = [], []
                            time, second = 0, 0
                            flags, notsure = [], []
                    if pressed[2] and not pressed[0]:  # right click
                        if game == 1 and (x, y) not in shown:
                            if (x, y) not in flags:  # no flag at this position
                                if (x, y) not in notsure:  # empty position
                                    flags.append((x, y))
                                    bomb -= 1
                                else:
                                    notsure.remove((x, y))
                            else:  # with flag at this position
                                bomb += 1
                                flags.remove((x, y))
                                notsure.append((x, y))
                if width * 15 + 42 < mouse_y < width * 15 + 58:
                    change = False
                    if 15 < mouse_x < 45 and difficulty != 1:  # click "Easy"
                        difficulty, length, width, bomb, change = 1, 9, 9, 10, True
                    elif 65 < mouse_x < 95 and difficulty != 2:  # click "Norm"
                        difficulty, length, width, bomb, change = 2, 16, 16, 40, True
                    elif 115 < mouse_x < 145 and difficulty != 3:  # click "Hard"
                        difficulty, length, width, bomb, change = 3, 16, 30, 99, True
                    if change:  # change difficulty level
                        game, bombed, time, second = 2, False, 0, 0
                        bombs, shown, flags, notsure = [], [], [], []
                        displaysurf = pygame.display.set_mode((length * 15 + 40, width * 15 + 60 + 20), 0, 32)
                        rect3.center = (30, width * 15 + 50)
                        rect4.center = (80, width * 15 + 50)
                        rect5.center = (130, width * 15 + 50)

        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
