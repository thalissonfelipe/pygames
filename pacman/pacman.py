import pygame
import random
from abc import ABCMeta, abstractmethod


pygame.init()

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELLS = 30
SPEED = 1
WALL = 2
FOOD = 1

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 140, 0)
PINK = (255, 15, 192)

# directions
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

# states
PLAYING = 0
PAUSED = 1
GAMEOVER = 2
WINNER = 3

pygame.display.set_caption('Pacman')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
font = pygame.font.SysFont('arial', 24, True, False)


class Game(metaclass=ABCMeta):
    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass


class Movable(metaclass=ABCMeta):
    @abstractmethod
    def accept_moviment(self):
        pass

    def decline_moviment(self, directions):
        pass

    def corner(self, directions):
        pass


class Scenario(Game):
    MAX_POINTS = 306

    def __init__(self, pacman, size):
        self.pacman = pacman
        self.movables = [pacman]
        self.size = size
        self.points = 0
        self.state = 0
        self.lives = 1
        self.matrix = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    exit()
                if e.key == pygame.K_r:
                    self.restart()
                if e.key == pygame.K_p:
                    if self.state == PLAYING:
                        self.state = PAUSED
                    elif self.state == PAUSED:
                        self.state = PLAYING

    def update(self):
        if self.state == PLAYING:
            self.update_playing()
        elif self.state == PAUSED:
            self.update_paused()
        elif self.state == GAMEOVER:
            self.update_gameover()

    def update_playing(self):
        for movable in self.movables:
            line = movable.line
            col = movable.column
            line_intention = movable.line_intention
            col_intention = movable.col_intention

            directions = self.get_directions(line, col)
            if len(directions) >= 3:
                movable.corner(directions)

            if (
                isinstance(movable, Ghost) and
                movable.line == self.pacman.line and
                movable.column == self.pacman.column
            ):
                self.lives -= 1
                if self.lives <= 0:
                    self.state = GAMEOVER
                else:
                    self.pacman.line = 1
                    self.pacman.column = 1
            else:
                if (
                    0 <= col_intention < 28 and 0 <= line_intention < 29 and
                    self.matrix[line_intention][col_intention] != WALL
                ):
                    movable.accept_moviment()
                    if isinstance(movable, Pacman) and self.matrix[line][col] == FOOD:
                        self.points += 1
                        self.matrix[line][col] = 0
                        if self.points >= self.MAX_POINTS:
                            self.state = WINNER
                else:
                    movable.decline_moviment(directions)

    def update_paused(self):
        pass

    def update_gameover(self):
        pass

    def draw(self, screen):
        self.draw_info(screen)
        if self.state == PLAYING:
            self.draw_playing(screen)
        elif self.state == PAUSED:
            self.draw_playing(screen)
            self.draw_paused(screen)
        elif self.state == GAMEOVER:
            self.draw_playing(screen)
            self.draw_gameover(screen)
        elif self.state == WINNER:
            self.draw_playing(screen)
            self.draw_winner(screen)

    def draw_playing(self, screen):
        for i, line in enumerate(self.matrix):
            self.__draw(screen, i, line)
        self.draw_points(screen)

    def draw_paused(self, screen):
        self.draw_text_center(screen, 'P A U S E D')

    def draw_gameover(self, screen):
        self.draw_text_center(screen, 'G A M E O V E R!')

    def draw_winner(self, screen):
        self.draw_text_center(screen, 'C O N G R A T U L A T I O N S! Y O U W O N!')

    def draw_info(self, screen):
        text = font.render('P : Pause/Unpause', True, YELLOW)
        text_x = 580
        text_y = 200
        screen.blit(text, (text_x, text_y))
        text = font.render('Q : Quit', True, YELLOW)
        text_x = 580
        text_y = 275
        screen.blit(text, (text_x, text_y))
        text = font.render('R : Restart', True, YELLOW)
        text_x = 580
        text_y = 300
        screen.blit(text, (text_x, text_y))
        text = font.render('↕: Up/Down', True, YELLOW)
        text_x = 573
        text_y = 225
        screen.blit(text, (text_x, text_y))
        text = font.render('↔ : Left/Right', True, YELLOW)
        text_x = 580
        text_y = 250
        screen.blit(text, (text_x, text_y))

    def restart(self):
        self.lives = 5

    @staticmethod
    def draw_text_center(screen, text):
        text = font.render(text, True, YELLOW)
        text_x = (screen.get_width() - text.get_width()) // 2
        text_y = (screen.get_height() - text.get_height()) // 2
        screen.blit(text, (text_x, text_y))

    def __draw(self, screen, i, line):
        for j, col in enumerate(line):
            x = j * self.size
            y = i * self.size
            half = self.size // 2

            color = BLACK
            if col == WALL:
                color = BLUE

            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)

            if col == FOOD:
                pygame.draw.circle(screen, YELLOW, (x + half, y + half), self.size // 10, 0)

    def draw_points(self, screen):
        x, y = CELLS * self.size, 50
        text = font.render(f'Score: {self.points}', True, YELLOW)
        screen.blit(text, (x, y))
        text = font.render(f'Lives: {self.lives}', True, YELLOW)
        screen.blit(text, (x, y + 50))

    def get_directions(self, line, column):
        directions = []

        if self.matrix[line-1][column] != WALL:
            directions.append(UP)
        if self.matrix[line+1][column] != WALL:
            directions.append(DOWN)
        if self.matrix[line][column-1] != WALL:
            directions.append(LEFT)
        if self.matrix[line][column+1] != WALL:
            directions.append(RIGHT)

        return directions

    def add_movable(self, obj):
        self.movables.append(obj)


class Pacman(Game, Movable):
    def __init__(self, size):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.size = size
        self.radius = self.size // 2
        self.speed_x = 0
        self.speed_y = 0
        self.line = 1
        self.column = 1
        self.col_intention = self.column
        self.line_intention = self.line
        self.opened = 0
        self.speed_o = 1

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.speed_x = SPEED
                if e.key == pygame.K_LEFT:
                    self.speed_x = -SPEED
                if e.key == pygame.K_UP:
                    self.speed_y = -SPEED
                if e.key == pygame.K_DOWN:
                    self.speed_y = SPEED

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.speed_x = 0
                if e.key == pygame.K_LEFT:
                    self.speed_x = 0
                if e.key == pygame.K_UP:
                    self.speed_y = 0
                if e.key == pygame.K_DOWN:
                    self.speed_y = 0

    def update(self):
        self.col_intention = self.column + self.speed_x
        self.line_intention = self.line + self.speed_y
        self.center_x = self.column * self.size + self.radius
        self.center_y = self.line * self.size + self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        self.opened += self.speed_o
        if self.opened > self.radius:
            self.speed_o = -1
        if self.opened <= 0:
            self.speed_o = 1

        # mouth
        mouth_corner = (self.center_x, self.center_y)
        upper_side = (self.center_x + self.radius, self.center_y - self.opened)
        underside = (self.center_x + self.radius, self.center_y + self.opened)
        points = [mouth_corner, upper_side, underside]

        pygame.draw.polygon(screen, BLACK, points, 0)
        pygame.time.delay(100)

        # eye
        eye_x = self.center_x + self.radius // 3
        eye_y = self.center_y - self.radius * 0.7
        eye_radius = self.radius  // 10

        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), eye_radius, 0)

    def accept_moviment(self):
        self.line = self.line_intention
        self.column = self.col_intention

    def decline_moviment(self, directions):
        self.line_intention = self.line
        self.col_intention = self.column

    def corner(self, directions):
        pass


class Ghost(Game):
    def __init__(self, color, size):
        self.column = 13
        self.line = 15
        self.color = color
        self.size = size
        self.speed = 1
        self.direction = DOWN
        self.col_intention = self.column
        self.line_intention = self.line

    def handle_events(self, events):
        pass

    def update(self):
        if self.direction == UP:
            self.line_intention -= self.speed
        elif self.direction == DOWN:
            self.line_intention += self.speed
        elif self.direction == LEFT:
            self.col_intention -= self.speed
        elif self.direction == RIGHT:
            self.col_intention += self.speed

    def draw(self, screen):
        slc = self.size // 8
        px = self.column * self.size
        py = self.line * self.size
        contours = [
            (px, py + self.size),
            (px + slc, py + 2 * slc),
            (px + 2 * slc, py + slc // 2),
            (px + 3 * slc, py),
            (px + 5 * slc, py),
            (px + 6 * slc, py + slc // 2),
            (px + 7 * slc, py + 2 * slc),
            (px + self.size, py + self.size)
        ]

        eye_radius_ext = slc
        eye_radius_int = slc // 2
        eye_l_x = px + 2.5 * slc
        eye_l_y = py + 2.5 * slc
        eye_r_x = px + 5.5 * slc
        eye_r_y = py + 2.5 * slc

        pygame.draw.polygon(screen, self.color, contours, 0)
        pygame.draw.circle(screen, WHITE, (eye_l_x, eye_l_y), eye_radius_ext, 0)
        pygame.draw.circle(screen, BLACK, (eye_l_x, eye_l_y), eye_radius_int, 0)
        pygame.draw.circle(screen, WHITE, (eye_r_x, eye_r_y), eye_radius_ext, 0)
        pygame.draw.circle(screen, BLACK, (eye_r_x, eye_r_y), eye_radius_int, 0)

    def corner(self, directions):
        self.change_direction(directions)

    def accept_moviment(self):
        self.line = self.line_intention
        self.column = self.col_intention

    def decline_moviment(self, directions):
        self.line_intention = self.line
        self.col_intention = self.column
        self.change_direction(directions)

    def change_direction(self, directions):
        self.direction = random.choice(directions)


if __name__ == '__main__':
    size = SCREEN_HEIGHT // CELLS

    pacman = Pacman(size)
    blinky = Ghost(RED, size)
    inky = Ghost(CYAN, size)
    clyde = Ghost(ORANGE, size)
    pinky = Ghost(PINK, size)
    scenario = Scenario(pacman, size)

    scenario.add_movable(blinky)
    scenario.add_movable(inky)
    scenario.add_movable(clyde)
    scenario.add_movable(pinky)

    clk = pygame.time.Clock()

    while True:
        events = pygame.event.get()
        pacman.handle_events(events)
        scenario.handle_events(events)

        pacman.update()
        blinky.update()
        inky.update()
        clyde.update()
        pinky.update()
        scenario.update()

        screen.fill(BLACK)
        scenario.draw(screen)
        pacman.draw(screen)
        blinky.draw(screen)
        inky.draw(screen)
        clyde.draw(screen)
        pinky.draw(screen)

        pygame.display.update()

        clk.tick(60)
