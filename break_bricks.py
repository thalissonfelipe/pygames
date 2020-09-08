import sys
import pygame
import random
from os import listdir


WIDTH = 780
HEIGHT = 630
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 20


class SceneManager:
    def __init__(self, scene):
        self.go_to(scene)

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


class GameScene:
    def __init__(self):
        super(GameScene, self).__init__()
        self.player = pygame.sprite.Group(Player())
        self.ball = Ball()
        self.ball.scene = self
        self.blocks = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        images_block = self.load_images()
        self.font = pygame.font.SysFont('Arial', 20)

        for y in range(BLOCK_WIDTH//2, BLOCK_HEIGHT*10, BLOCK_HEIGHT):
            for x in range(BLOCK_WIDTH//2, WIDTH-BLOCK_WIDTH, BLOCK_WIDTH):
                block = Block((x, y), random.choice(images_block))
                self.blocks.add(block)

    def handle_events(self, events):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            self.manager.go_to(MenuScene())

    def update(self):
        self.player.update()
        self.ball.update(self.player, self.blocks, self.powerups)
        self.powerups.update()
        self.blocks.update()

    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_score(self.ball.nbrokens, screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.powerups.draw(screen)
        screen.blit(self.ball.image, self.ball.rect.topleft)

    def game_over(self):
        self.manager.go_to(GameOverScene())

    def load_images(self):
        filenames = listdir('assets/ping_pong/blocks')
        blocks = [pygame.image.load('assets/ping_pong/blocks/'+name).convert_alpha() for name in filenames]
        blocks = [pygame.transform.scale(b, (BLOCK_WIDTH, BLOCK_HEIGHT)) for b in blocks]

        return blocks

    def draw_score(self, score, screen):
        score = self.font.render('SCORE: {}'.format(score * 10), False, WHITE)
        screen.blit(score, (100, 0))


class GameOverScene:
    def __init__(self):
        super(GameOverScene, self).__init__()
        bfont = pygame.font.SysFont('Arial', 50)
        sfont = pygame.font.SysFont('Arial', 30)
        self.title = bfont.render('GAME OVER', False, WHITE)
        self.playagain = sfont.render('Play again!', False, WHITE)
        self.playagainrect = self.playagain.get_rect(center=(
            self.playagain.get_width()//2,
            self.playagain.get_height()//2
        ))
        self.playagainrect.left = WIDTH//2-self.playagain.get_width()//2
        self.playagainrect.top = 280

    def handle_events(self, events):
        clicked, _, _ = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            self.manager.go_to(GameScene())

        if self.playagainrect.collidepoint(mouse_pos) and clicked:
            self.manager.go_to(GameScene())

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        screen.blit(self.title, (WIDTH//2-self.title.get_width()//2, 200))
        pygame.draw.rect(screen, BLACK, self.playagainrect)
        screen.blit(
            self.playagain, (WIDTH//2-self.playagain.get_width()//2, 280)
        )


class MenuScene:
    def __init__(self):
        super(MenuScene, self).__init__()
        bfont = pygame.font.SysFont('Arial', 50)
        sfont = pygame.font.SysFont('Arial', 30)
        self.title = bfont.render('Break Bricks', False, WHITE)
        self.play = sfont.render('Play', False, WHITE)
        self.playrect = self.play.get_rect(center=(
            self.play.get_width()//2, self.play.get_height()//2
        ))
        self.playrect.left = WIDTH//2-self.play.get_width()//2
        self.playrect.top = 260
        self.quit = sfont.render('Quit', False, WHITE)
        self.quitrect = self.play.get_rect(center=(
            self.quit.get_width()//2,
            self.quit.get_height()//2
        ))
        self.quitrect.topleft = WIDTH//2-self.quit.get_width()//2, 300

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        clicked, _, _ = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if self.playrect.collidepoint(mouse_pos) and clicked:
            self.manager.go_to(GameScene())

        if self.quitrect.collidepoint(mouse_pos) and clicked:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_SPACE]:
            self.manager.go_to(GameScene())

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((200, 200, 0))
        screen.blit(self.title, (WIDTH//2-self.title.get_width()//2, 200))
        pygame.draw.rect(screen, (200, 200, 0), self.playrect)
        screen.blit(self.play, (WIDTH//2-self.play.get_width()//2, 260))
        pygame.draw.rect(screen, (200, 200, 0), self.quitrect)
        screen.blit(self.quit, (WIDTH//2-self.quit.get_width()//2, 300))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(
            WIDTH//2-self.image.get_width()//2, HEIGHT-2*self.image.get_height()
        ))
        self.speed = 8
        self.vel = pygame.Vector2((0, 0))

    def update(self):
        pressed = pygame.key.get_pressed()
        right, left = [pressed[key] for key in (pygame.K_RIGHT, pygame.K_LEFT)]

        if self.index + 1 > 9:
            self.index = 0

        self.image = self.images[self.index//3]
        self.index += 1

        if right:
            self.vel.x = self.speed

        if left:
            self.vel.x = -self.speed

        if not (right or left):
            self.vel.x = 0

        old_right, old_left = self.rect.right, self.rect.left
        self.rect.left += self.vel.x
        # boundary
        if self.rect.right > WIDTH:
            self.rect.right = old_right
        elif self.rect.left < 0:
            self.rect.left = old_left

    def load_images(self):
        filenames = listdir('assets/ping_pong/spritesheet')
        images = [pygame.image.load('assets/ping_pong/spritesheet/'+name).convert_alpha() for name in filenames]
        self.images = [pygame.transform.scale(i, (100, 20)) for i in images]


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.image = pygame.image.load('assets/ping_pong/ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(topleft=(WIDTH//2-25, HEIGHT-50))
        self.vel = pygame.Vector2((5, 5))
        self.nbrokens = 0

    def update(self, player, blocks, powerups):
        self.rect.left += self.vel.x
        self.rect.top -= self.vel.y

        if pygame.sprite.spritecollide(self, player, False):
            self.vel.y *= -1
        if pygame.sprite.spritecollide(self, blocks, True):
            self.vel.y *= -1
            self.nbrokens += 1
            # if self.nbrokens % 5 == 0:
            #     powerup = PowerUp((100, 100))
            #     powerups.add(powerup)
            #     print(powerups)

        if self.rect.bottom > HEIGHT:
            self.scene.game_over()
        if self.rect.top < 0:
            self.vel.y *= -1

        if self.rect.right > WIDTH:
            self.vel.x *= -1
        elif self.rect.left < 0:
            self.vel.x *= -1


class PowerUp(pygame.sprite.Group):
    def __init__(self, pos):
        super(PowerUp, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 5

    def update(self):
        self.rect.top += self.speed


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super(Block, self).__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Break Bricks')
    clock = pygame.time.Clock()
    manager = SceneManager(MenuScene())
    font = pygame.font.SysFont('Arial', 20)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.draw(screen)
        fps = int(clock.get_fps())
        screen.blit(font.render('FPS: {}'.format(fps), False, WHITE), (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
