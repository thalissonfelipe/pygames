import pygame


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
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
font = pygame.font.SysFont('arial', 24, True, False)

class Scenario:
    def __init__(self, pacman, size):
        self.pacman = pacman
        self.size = size
        self.points = 0
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

    def update(self):
        col = self.pacman.col_intention
        line = self.pacman.line_intention

        if 0 <= col < 28 and 0 <= line < 29:
            if self.matrix[line][col] != WALL:
                self.pacman.accept_moviment()
                if self.matrix[line][col] == FOOD:
                    self.points += 1
                    self.matrix[line][col] = 0

    def draw(self, screen):
        for i, line in enumerate(self.matrix):
            self.__draw(screen, i, line)

        self.draw_points(screen)

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


class Pacman:
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

        # mouth
        mouth_corner = (self.center_x, self.center_y)
        upper_side = (self.center_x + self.radius, self.center_y - self.radius)
        underside = (self.center_x + self.radius, self.center_y)
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


if __name__ == '__main__':
    size = SCREEN_HEIGHT // CELLS
    pacman = Pacman(size)
    scenario = Scenario(pacman, size)

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
        pacman.handle_events(events)

        pacman.update()
        scenario.update()

        screen.fill(BLACK)
        scenario.draw(screen)
        pacman.draw(screen)
        pygame.display.update()
