import os
import sys
import pygame
import numpy as np


os.environ['SDL_VIDEO_CENTERED'] = '1'

# global variables
WIDTH, HEIGHT = 320, 360
RECT_SIZE = (100, 100)
IMAGE_SIZE = (80, 80)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PADDING = 5
ROWS = COLS = 3
LINE_WIDTH = 5
X_TURN = 1
O_TURN = 2


class Player:
    def __init__(self):
        self.turn = X_TURN
        self.winner = False
        self.tied = 0
        self.x_turn = Font().get_font("X's turn", RED, True)
        self.o_turn = Font().get_font("O's turn", RED, True)
        self.x_wins = Font().get_font('Player "X" wins', RED, True)
        self.o_wins = Font().get_font('Player "O" wins', RED, True)
        self.tied_font = Font().get_font('Nobody won', RED, True)
        self.x = pygame.transform.scale(pygame.image.load('assets/tic_tac_toe/x.png').convert_alpha(), IMAGE_SIZE)
        self.o = pygame.transform.scale(pygame.image.load('assets/tic_tac_toe/o.png').convert_alpha(), IMAGE_SIZE)

    def draw_turn(self, screen):
        if self.tied == 9: # all rects were pressed
            screen.blit(self.tied_font, (WIDTH//2-self.tied_font.get_width()//2, HEIGHT-self.tied_font.get_height()-PADDING))
            self.winner = True
        elif not self.winner:
            font = self.x_turn if self.turn == X_TURN else self.o_turn
            screen.blit(font, (WIDTH//2-font.get_width()//2, HEIGHT-font.get_height()-PADDING))
        else:
            font = self.x_wins if self.turn == X_TURN else self.o_wins
            screen.blit(font, (WIDTH//2-font.get_width()//2, HEIGHT-font.get_height()-PADDING))

    def draw_pressed(self, screen, rects):
        for rect in rects:
            if rect.pressed:
                if rect.pressed == X_TURN:
                    screen.blit(self.x, (rect.rect.x+self.x.get_width()//6, rect.rect.top+self.x.get_height()//6))
                else:
                    screen.blit(self.o, (rect.rect.x+self.o.get_width()//8, rect.rect.top+self.o.get_height()//6))


class Rect(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Rect, self).__init__()
        self.image = pygame.Surface(RECT_SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=pos)
        self.pressed = 0


class Font:
    def __init__(self):
        self.font_family = 'comicsansms'
        self.font = pygame.font.SysFont(self.font_family, 80)
        self.small_font = pygame.font.SysFont(self.font_family, 30)

    def get_font(self, text, color, small=False):
        if small:
            return self.small_font.render(text, False, color)
        return self.font.render(text, False, color)


class TicTac:
    def __init__(self, screen):
        self.screen = screen
        self.create_rects()
        self.create_combinations()
        self.player = Player()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        pressed, _, _ = pygame.mouse.get_pressed()

        for rect in self.rects:
            if pressed and pygame.Rect.collidepoint(rect.rect, mouse_pos):
                if not rect.pressed and not self.player.winner:
                    if self.player.turn == X_TURN:
                        self.player.turn = O_TURN
                        rect.pressed = X_TURN
                    else:
                        self.player.turn = X_TURN
                        rect.pressed = O_TURN
                    self.player.tied += 1

        self.check_win()

    def handle_restart_game(self):
        if self.player.winner or self.player.tied == 9:
            pygame.time.wait(2000)
            self.create_rects()
            self.create_combinations()
            self.position = None
            self.player = Player()

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_lines()
        self.player.draw_pressed(self.screen, self.rects)
        self.player.draw_turn(self.screen)
        if self.player.winner:
            self.draw_winner_line()
        pygame.display.update()

    def draw_lines(self):
        pygame.draw.line(self.screen, BLACK, (107.5, PADDING), (107.5, 315), LINE_WIDTH)
        pygame.draw.line(self.screen, BLACK, (212.5, PADDING), (212.5, 315), LINE_WIDTH)
        pygame.draw.line(self.screen, BLACK, (PADDING, 107.5), (WIDTH-PADDING, 107.5), LINE_WIDTH)
        pygame.draw.line(self.screen, BLACK, (PADDING, 212.5), (WIDTH-PADDING, 212.5), LINE_WIDTH)

    def create_rects(self):
        rects = pygame.sprite.Group()
        x = y = PADDING
        for _ in range(ROWS):
            for _ in range(COLS):
                rects.add(Rect((x, y)))
                x += RECT_SIZE[0] + PADDING
            x = PADDING
            y += RECT_SIZE[1] + PADDING

        self.rects = rects
        self.rects.draw(self.screen)

    def is_pressed(self, rects):
        for rect in rects:
            if not rect.pressed:
                return False

        return all(rect.pressed == rects[0].pressed for rect in rects)

    def draw_winner_line(self):
        if self.position == 0:
            pygame.draw.line(self.screen, RED, (PADDING, 60), (WIDTH-PADDING, 60), LINE_WIDTH)
        elif self.position == 1:
            pygame.draw.line(self.screen, RED, (PADDING, 165), (WIDTH-PADDING, 165), LINE_WIDTH)
        elif self.position == 2:
            pygame.draw.line(self.screen, RED, (PADDING, 270), (WIDTH-PADDING, 270), LINE_WIDTH)
        elif self.position == 3:
            pygame.draw.line(self.screen, RED, (55, PADDING), (55, HEIGHT-9*PADDING), LINE_WIDTH)
        elif self.position == 4:
            pygame.draw.line(self.screen, RED, (160, PADDING), (160, HEIGHT-9*PADDING), LINE_WIDTH)
        elif self.position == 5:
            pygame.draw.line(self.screen, RED, (264, PADDING), (264, HEIGHT-9*PADDING), LINE_WIDTH)
        elif self.position == 6:
            pygame.draw.line(self.screen, RED, (PADDING, PADDING), (WIDTH-PADDING, HEIGHT-9*PADDING), LINE_WIDTH)
        elif self.position == 7:
            pygame.draw.line(self.screen, RED, (WIDTH-PADDING, PADDING), (PADDING, HEIGHT-9*PADDING-PADDING), LINE_WIDTH)

    def check_win(self):
        if not self.player.winner:
            for i, rects in enumerate(self.combinations):
                if self.is_pressed(rects):
                    self.player.winner = True
                    self.player.turn = rects[0].pressed
                    self.position = i
        else:
            self.handle_restart_game()

    def create_combinations(self):
        rects_matrix = np.reshape(self.rects.sprites(), (3, 3))
        combinations = [row for row in rects_matrix]
        for row in np.transpose(rects_matrix):
            combinations.append(row)
        combinations.append(np.diag(rects_matrix))
        combinations.append(np.diag(np.fliplr(rects_matrix)))

        self.combinations = combinations


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tic Tac Toe')
    clock = pygame.time.Clock()
    tictac = TicTac(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tictac.update()
        tictac.draw_lines()
        tictac.draw()
        clock.tick(60)


if __name__ == '__main__':
    main()
