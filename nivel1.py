# === Importar bibliotecas ===
import pygame
import os
from pathlib import Path

# === Importar teclas ===
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_e,
    K_LSHIFT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)   

# === Inicializar mixer ===
pygame.mixer.init()

# === Inicializar pygame ===
successes, failures = pygame.init() 
print("{0} successes and {1} failures".format(successes, failures))

# === Colores ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# === Configurar la ventana y reloj ===
FPS = 60 
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EcoRush!")
clock = pygame.time.Clock() # Controlar FPS

# === Definir al Player ===
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((WHITE))
        self.rect = self.surf.get_rect()

    # === Mover el sprite ===
    def update(self, pressed_keys):
        self.rect.clamp_ip(screen.get_rect()) # Para no salirse de la pantalla

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        if pressed_keys[K_LSHIFT]:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -8)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 8)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-8, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(8, 0)

            if pressed_keys[K_w]:
                self.rect.move_ip(0, -8)
            if pressed_keys[K_s]:
                self.rect.move_ip(0, 8)
            if pressed_keys[K_a]:
                self.rect.move_ip(-8, 0)
            if pressed_keys[K_d]:
                self.rect.move_ip(8, 0)

# === Rutas relativas con pathlib ===
# BASE_DIR: carpeta donde esta el archivo main.py
BASE_DIR = Path(__file__).resolve().parent
# IMG_DIR: carpeta donde se guardan las imagenes del proyecto
IMG_DIR = BASE_DIR / "assets" / "img"

# === Cargar imaganes ===

# === 
player = Player()
player.rect.center = (WIDTH//2, HEIGHT//2)   # una sola vez: empieza centrado

running = True

# === Bucle principal ===
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # === Logica del juego ===

    pressed_keys = pygame.key.get_pressed() # Detectar las teclas pulsadas
    
    player.update(pressed_keys) # Actualizar el sprite mediante las teclas


    # === Zona de Dibujo ===
    screen.fill(BLACK)   
    screen.blit(player.surf, player.rect)

    pygame.display.flip()