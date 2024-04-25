import random
import sys

import pygame

# Espina
class Spike(pygame.sprite.Sprite):
    def __init__(self, pos: set):
        super(Spike, self).__init__()
        self.image = pygame.image.load("assets/espina.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 10

    def _move(self, dt):
        self.rect.y += self.speed * dt
        if self.rect.y > 650:
            self.kill()

    def update(self, dt):
        pass

# Fruta
class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos: set, value: int = 5, image: str = ""):
        super(Fruit, self).__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = random.choice([20, 15, 10])
        self.value = value

    def _move(self, dt):
        self.rect.y += self.speed * dt
        if self.rect.y > 650:
            self.kill()

    def update(self, dt):
        # agregar movimiento
        pass

# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, pos: set):
        super(Player, self).__init__()
        self.image = pygame.image.load("assets/canasta.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 12

    def _move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed * dt * 2

        if keys[pygame.K_RIGHT] and self.rect.x < 700:
            self.rect.x += self.speed * dt * 2

    def update(self, dt):
        # agregar movimiento
        pass


class Game:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.state = "start"
        self.frutas = [
            {"image": "assets/manzana.png", "value": 10},
            {"image": "assets/banana.png", "value": 5},
            {"image": "assets/pera.png", "value": 15},
            {"image": "assets/uva.png", "value": 20},
            {"image": "assets/sandia.png", "value": 25},
        ]
        self.playersprite = pygame.sprite.GroupSingle(Player(pos=(350, 550)))
        self.fruitsprite = pygame.sprite.Group()
        self.coldown = 0
        self.start()

    # Iniciar
    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("La Finca de Don Juan")
        self.clock = pygame.time.Clock()
        self.running = True
        self.coldown = pygame.time.get_ticks()

    # Dibujar
    def draw(self, dt):
        self.playersprite.draw(self.screen)
        self.playersprite.update(dt)
        self.fruitsprite.draw(self.screen)
        self.fruitsprite.update(dt)

    # Dibujar texto
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Colisiones
    def collision(self):
        for fruit in self.fruitsprite:
            if pygame.sprite.spritecollide(fruit, self.playersprite, False):
                if isinstance(fruit, Spike):
                    fruit.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.running = False

                else:
                    self.score += fruit.value
                    fruit.kill()
    
    # generar frutas y espinas
    def generate_fruit(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.coldown >= 2000:
            x, y, fruit = (
                random.choice([70, 150, 300, 600, 750]),
                0,
                random.choice(self.frutas),
            )
            if random.choice([True, True, True, True, False]):
                self.fruitsprite.add(
                    Fruit(pos=(x, y), value=fruit["value"], image=fruit["image"])
                )
            else:
                self.fruitsprite.add(Spike(pos=(x, y)))
            self.coldown = current_time
    
        

    def run(self):
        while self.running:
            # Tiempo de juego.
            dt = self.clock.tick(60) / 100
            self.screen.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
           
            # Escenario de juego.
            self.estado(dt)
            
            # Actualizar pagina.
            pygame.display.update()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def mostrar_graficos(self):
        self.draw_text(f"Score: {self.score}", 30, "black", 65, 19)
        self.draw_text(f"Lives: {self.lives}", 30, "black", 735, 19)
        
    def estado(self, dt):
        pass

if __name__ == "__main__":
    pass
