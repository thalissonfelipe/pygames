import os
import sys
import pygame
from random import randrange, randint
from pygame.locals import (
    K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, USEREVENT, QUIT, Rect
)


WIDTH, HEIGHT = 512, 544
SCREENRECT = Rect(0, 0, WIDTH, HEIGHT)
BACKGROUNDRECT = Rect(0, 0, WIDTH, HEIGHT)
root_dir = os.path.dirname(os.path.realpath(__file__))
SHIP_DIR = os.path.join(root_dir, 'assets', 'space_invaders', 'ship')
BG_DIR = os.path.join(root_dir, 'assets', 'space_invaders', 'background')
SHOT_DIR = os.path.join(root_dir, 'assets', 'space_invaders', 'shot')
ALIEN_DIR = os.path.join(root_dir, 'assets', 'space_invaders', 'aliens')
EXPLOSION_DIR = os.path.join(root_dir, 'assets', 'space_invaders', 'explosion')
SOUNDS_DIR = os.path.join(root_dir, 'sounds', 'space_invaders')
MAX_SHOTS = 10
SCORE = 0
WHITE = (255, 255, 255)


class dummysound:
    def play(self): pass


class Player(pygame.sprite.Sprite):
    images = []

    def __init__(self):
        super(Player, self).__init__(self.containers)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.speed = 5
        self.animatecycle = 3
        self.reloading = 0
        self.shot_sound = load_sound(SOUNDS_DIR, 'shoot.wav')
        self.explosion_sound = load_sound(SOUNDS_DIR, 'explosion.wav')
        self.shot_sound.set_volume(0.05)
        self.explosion_sound.set_volume(0.09)

    def update(self):
        keys = pygame.key.get_pressed()
        keys_pressed = [keys[key] for key in (K_LEFT, K_RIGHT, K_UP, K_DOWN)]
        left, right, up, down = keys_pressed

        if self.index + 1 > len(self.images)*self.animatecycle:
            self.index = 0

        self.image = self.images[self.index//self.animatecycle]
        self.index += 1

        if left:
            self.rect.move_ip(-self.speed, 0)

        if right:
            self.rect.move_ip(self.speed, 0)

        if up:
            self.rect.move_ip(0, -self.speed)

        if down:
            self.rect.move_ip(0, self.speed)

        self.rect.clamp_ip(SCREENRECT)

    def shot(self, firing, shots):
        if not self.reloading and firing and len(shots) < MAX_SHOTS:
            self.shot_sound.play()
            Shot((self.rect.centerx, self.rect.top))
        self.reloading = firing

    def collide(self, aliens):
        global SCORE
        sprite_list = pygame.sprite.spritecollide(self, aliens, False)
        if sprite_list:
            for sprite in sprite_list:
                sprite.kill()
                self.explosion_sound.play()
                SCORE -= 1


class Shot(pygame.sprite.Sprite):
    images = []

    def __init__(self, pos):
        super(Shot, self).__init__(self.containers)
        self.image = self.images[2]
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = -11

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()

        for sprite in self.containers:
            if isinstance(sprite, pygame.sprite.Group):
                for spr in sprite:
                    if pygame.sprite.collide_rect(self, spr):
                        if isinstance(spr, Alien):
                            self.kill()
                            spr.life -= 1


class Alien(pygame.sprite.Sprite):
    images = []

    def __init__(self, index):
        super(Alien, self).__init__(self.containers)
        self.animation_count = 0
        self.aliens_img = self.images[index]
        self.image = self.aliens_img[self.animation_count]
        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIDTH-self.rect.width)
        self.rect.y = randrange(-40, 0)
        self.speed = pygame.Vector2(randrange(-3, 3), randrange(3, 5))
        self.animatecycle = 3
        self.life = index + 1 * 2 - 1
        self.padding = 3

    def update(self):
        global SCORE
        if self.animation_count + 1 > len(self.aliens_img)*self.animatecycle:
            self.animation_count = 0

        self.image = self.aliens_img[self.animation_count//self.animatecycle]
        self.animation_count += 1

        if self.life == 0:
            self.kill()
            Explosion(self.rect.topleft)
            SCORE += 1

        self.rect.left += self.speed.x
        self.rect.top += self.speed.y

        if self.rect.left < self.padding:
            self.speed.x *= -1

        if self.rect.right > WIDTH-self.padding:
            self.speed.x *= -1

        if self.rect.top > HEIGHT-self.padding:
            self.kill()
            SCORE -= 1


class Explosion(pygame.sprite.Sprite):
    images = []

    def __init__(self, pos):
        super(Explosion, self).__init__(self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.index = 0
        self.explosion_sound = load_sound(SOUNDS_DIR, 'explosion.wav')
        self.explosion_sound.set_volume(0.09)

    def update(self):
        self.index += 1
        self.image = self.images[self.index]
        if self.index == len(self.images)-1:
            self.explosion_sound.play()
            self.kill()


class Text(pygame.sprite.Sprite):
    def __init__(self, pos, width, type):
        super(Text, self).__init__(self.containers)
        self.font = pygame.font.SysFont('arial', 20)
        self.color = WHITE
        self.width = width
        self.height = 20
        self.text = 'FPS: ' if type == 'fps' else 'SCORE: '
        self.value = 0
        self.pos = pos

    def update(self):
        self.surf = self.font.render(self.text + str(self.value), 1, self.color)
        self.image = pygame.Surface((self.width, self.height))
        self.image.blit(
            self.surf, (0, self.height/2 - self.surf.get_height()/2)
        )
        self.rect = self.image.get_rect(topleft=self.pos)


def load_sound(dirname, file):
    if not pygame.mixer:
        return dummysound()
    file = os.path.join(dirname, file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error as e:
        print('Warning, unable to load, %s' % file)
        raise e
    return dummysound()


def load_image(dirname, file):
    path = os.path.join(dirname, file)
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print('Error: ', e)
        raise e
    return image


def load_images(dirname):
    images = []
    for filename in os.listdir(dirname):
        images.append(load_image(dirname, filename))
    return images


def configure_screen():
    screen = pygame.display.set_mode(SCREENRECT.size)
    pygame.display.set_caption('Space')
    background = pygame.Surface((BACKGROUNDRECT.size))
    img = load_image(BG_DIR, 'desert-background.png')
    img = pygame.transform.scale(img, BACKGROUNDRECT.size)
    cloudimg = load_image(BG_DIR, 'clouds-transparent.png')
    cloudimg = pygame.transform.scale(cloudimg, (WIDTH, cloudimg.get_height()))
    background.blit(img, (0, 0))
    background.blit(cloudimg, (0, 0))
    background.blit(cloudimg, (0, 112 * 3))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    return screen, background


def main():
    pygame.init()
    screen, background = configure_screen()
    clock = pygame.time.Clock()

    # Loading images
    pi = load_images(SHIP_DIR)
    Player.images = [pygame.transform.scale(i, (24, 32)) for i in pi]

    ai = load_images(ALIEN_DIR)[::-1]
    for j, i in enumerate(ai):
        ai[j] = pygame.transform.scale(i, (i.get_width()+8, i.get_height()+8))
    Alien.images = {0: ai[0:2], 1: ai[2:4], 2: ai[4:6]}

    Shot.images = load_images(SHOT_DIR)
    Explosion.images = load_images(EXPLOSION_DIR)

    all = pygame.sprite.RenderUpdates()
    shots = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    Player.containers = all
    Shot.containers = shots, all
    Alien.containers = aliens, all
    Explosion.containers = all
    Text.containers = all

    player = Player()
    text_fps = Text((0, 0), 75, 'fps')
    text_score = Text((WIDTH-130, 0), 130, 'score')
    pygame.time.set_timer(USEREVENT+1, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == USEREVENT+1:
                Alien(randint(0, 2))

        # update fps and score values
        text_fps.value = int(clock.get_fps())
        text_score.value = SCORE

        all.clear(screen, background)
        all.update()
        keys = pygame.key.get_pressed()
        firing = keys[K_SPACE]
        player.shot(firing, shots)
        player.collide(aliens)

        dirty = all.draw(screen)
        pygame.display.update(dirty)
        clock.tick(60)


if __name__ == '__main__':
    main()
