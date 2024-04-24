import random
import sys

import pygame


class Spike(pygame.sprite.Sprite):
    def __init__(self, pos: set):
        super(Spike, self).__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 10

    def _move(self, dt):
        self.rect.y += self.speed * dt
        if self.rect.y > 650:
            self.kill()

    def update(self, dt):
        self._move(dt)

class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos: set, value: int = 5):
        super(Fruit, self).__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = random.choice([20, 15, 10])
        self.value = value

    def _move(self, dt):
        self.rect.y += self.speed * dt
        if self.rect.y > 650:
            self.kill()

    def update(self, dt):
        self._move(dt)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: set):
        super(Player, self).__init__()
        self.image = pygame.image.load("assets/basket.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 12

    def _move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed * dt * 2

        if keys[pygame.K_RIGHT] and self.rect.x < 750:
            self.rect.x += self.speed * dt * 2

    def update(self, dt):
        self._move(dt)


class Game:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.state = "start"
        self.playersprite = pygame.sprite.GroupSingle(Player(pos=(350, 550)))
        self.fruitsprite = pygame.sprite.Group()
        self.coldown = 0
        self.start()

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("La Finca de Don Juan")
        self.clock = pygame.time.Clock()
        self.running = True
        self.coldown = pygame.time.get_ticks()

    def draw(self, dt):
        self.playersprite.draw(self.screen)
        self.playersprite.update(dt)
        self.fruitsprite.draw(self.screen)
        self.fruitsprite.update(dt)

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def collision(self):
        for fruit in self.fruitsprite:
            if pygame.sprite.spritecollide(fruit, self.playersprite, False):
                
                if isinstance(fruit, Spike):
                    self.lives -= 1
                    if self.lives == 0:
                        self.running = False
                else:
                    self.score += fruit.value
                    fruit.kill()

    def generate_fruit(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.coldown >= 2000:
            x, y = random.choice([70, 150, 300, 600, 750]), 0
            if random.choice([True, False]):
                self.fruitsprite.add(Fruit(pos=(x, y), value=10))
            else:
                self.fruitsprite.add(Spike(pos=(x, y)))
            self.coldown = current_time

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 100
            self.screen.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw(dt)
            self.generate_fruit()
            self.collision()
            self.draw_text(f"Score: {self.score}", 30, "black", 65, 19)
            self.draw_text(f"Lives: {self.lives}", 30, "black", 735, 19)
            pygame.display.update()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
