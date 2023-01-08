import pygame
from copy import deepcopy
from random import choice, randrange

width, hue = 10, 20
TI = 45
GAME_R = width * TI, hue * TI
FPS = 60
sqd = []
for x in range(width):
    for y in range(hue):
        sqd.append(pygame.Rect(x * TI, y * TI, TI, TI))

figuresp = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
            [(0, -1), (-1, -1), (-1, 0), (0, 0)],
            [(-1, 0), (-1, 1), (0, 0), (0, -1)],
            [(0, 0), (-1, 0), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, 0)]]
figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in fig] for fig in figuresp]
figurerect = pygame.Rect(0, 0, TI - 2, TI - 2)
field = [[0 for i in range(width)] for j in range(hue)]
animatinon_count, animatinon_speed, animatinon_limit = 0, 60, 2000
figure = deepcopy(choice(figures))


def graniza():
    if figure[j].x < 0 or figure[j].x > width - 1:
        return False
    elif figure[j].y > hue - 1 or field[figure[j].y][figure[j].x]:
        return False
    return True


if __name__ == '__main__':
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(GAME_R)
    clock = pygame.time.Clock()
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        while True:
            dx, rotate = 0, False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_DOWN:
                        animatinon_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True
            # move x
            figureold = deepcopy(figure)
            for j in range(4):
                figure[j].x += dx
                if not graniza():
                    figure = deepcopy(figureold)
                    break
            screen.fill(pygame.Color('black'))
            # move y
            animatinon_count += animatinon_speed
            if animatinon_count > animatinon_limit:
                animatinon_count = 0
                figureold = deepcopy(figure)
                for j in range(4):
                    figure[j].y += 1
                    if not graniza():
                        for j in range(4):
                            field[figureold[j].y][figureold[j].x] = pygame.Color('blue')
                        figure = deepcopy(choice(figures))
                        animatinon_limit = 2000
                        break
            # rotate
            zenter = figure[0]
            figureold = deepcopy(figure)
            if rotate:
                for j in range(4):
                    x = figure[j].y - zenter.y
                    y = figure[j].x - zenter.x
                    figure[j].x = zenter.x - x
                    figure[j].y = zenter.y + y
                    if not graniza():
                        figure = deepcopy(figureold)
                        break
            # check line
            line = hue - 1
            for row in range(hue - 1, -1, -1):
                kolstvo = 0
                for j in range(width):
                    if field[row][j]:
                        kolstvo += 1
                    field[line][j] = field[row][j]
                if kolstvo < width:
                    line -= 1

            # draw sqd
            [pygame.draw.rect(screen, (40, 40, 40), i_r, 1) for i_r in sqd]
            # draw figure
            for j in range(4):
                figurerect.x = figure[j].x * TI
                figurerect.y = figure[j].y * TI
                pygame.draw.rect(screen, pygame.Color('green'), figurerect)
            # draw field
            for y, raw in enumerate(field):
                for x, col in enumerate(raw):
                    if col:
                        figurerect.x, figurerect.y = x * TI, y * TI
                        pygame.draw.rect(screen, col, figurerect)
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()
