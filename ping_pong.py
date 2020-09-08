import sys
import pygame
import random


SCREEN_SIZE = (800, 600)
PLAYER_SIZE = (10, 80)
BALL_SIZE = (15, 15)
RED = (255, 0, 0)
GREEN = (0, 0, 255)
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.vel = 7
        self.color = color
        self.score = 0
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.velx = 10
        self.vely = 10
        self.image = pygame.Surface(BALL_SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, window, sprites, player_a, player_b):
        self.rect.x += self.velx
        self.rect.y += self.vely

        if self.collide(sprites):
            self.velx *= -1

        if self.rect.x > window.get_width():
            player_a.score += 1
            self.rect.x = 775
            self.rect.y = random.randrange(0, SCREEN_SIZE[1])
            self.velx *= -1

        if self.rect.x < 1:
            player_b.score += 1
            self.rect.x = 25
            self.rect.y = random.randrange(0, SCREEN_SIZE[1])
            self.velx *= -1

        if self.rect.y < 1:
            self.vely *= -1

        if self.rect.y > window.get_height() - self.rect.height:
            self.vely *= -1

    def collide(self, sprites):
        if pygame.sprite.spritecollide(self, sprites, False):
            return True


class Game():
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.score_a = 0
        self.score_b = 0

    def draw_scores(self, player_a, player_b):
        font = pygame.font.SysFont('comicsans', 50)
        text_a = font.render(str(player_a.score), False, RED)
        text_b = font.render(str(player_b.score), False, RED)

        self.window.blit(text_a, (200, 50))
        self.window.blit(text_b, (600, 50))

    def main(self):
        player_a = Player(10, 265, RED)
        player_b = Player(780, 265, GREEN)
        ball = Ball(392.5, 292.5)

        self.players_sprite = pygame.sprite.Group()
        self.players_sprite.add(player_a)
        self.players_sprite.add(player_b)

        self.ball_sprite = pygame.sprite.Group()
        self.ball_sprite.add(ball)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] and player_a.y > 0:
                player_a.y -= player_a.vel

            if(
                keys[pygame.K_DOWN]
                and player_a.y < SCREEN_SIZE[1] - player_a.rect.height
            ):
                player_a.y += player_a.vel

            if keys[pygame.K_w] and player_b.y > 0:
                player_b.y -= player_b.vel

            if (keys[pygame.K_s]
                    and player_b.y < SCREEN_SIZE[1] - player_b.rect.height):
                player_b.y += player_b.vel

            self.window.fill((153, 204, 50))

            player_a.update()
            player_b.update()
            ball.update(self.window, self.players_sprite, player_a, player_b)

            self.players_sprite.draw(self.window)
            self.ball_sprite.draw(self.window)

            pygame.draw.line(
                self.window,
                WHITE,
                (400, 0),
                (400, SCREEN_SIZE[0]),
                2
            )

            self.draw_scores(player_a, player_b)
            pygame.display.update()
            self.clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Ping Pong')
    game = Game(window)
    game.main()
