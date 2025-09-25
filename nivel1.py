import pygame
from pathlib import Path

from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_w, K_a, K_s, K_d,
    K_LSHIFT, K_e, QUIT
)

pygame.init()

# === Configuración ===
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EcoRush!")
clock = pygame.time.Clock()
FPS = 60

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # carpeta donde está nivel1.py
IMG_DIR = BASE_DIR / "assets" / "img"

MAPA = pygame.image.load(str(IMG_DIR / "mapaprototipo.png"))
MAPA = pygame.transform.scale(MAPA, (WIDTH, HEIGHT))


# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
YELLOW= (255, 255, 0)
GREEN = (0, 255, 0)

# Fuente
font = pygame.font.SysFont("Arial", 36)

# === Jugador ===
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=(WIDTH//2, HEIGHT//2))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]: self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]: self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]: self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]: self.rect.move_ip(5, 0)
        if pressed_keys[K_w]: self.rect.move_ip(0, -5)
        if pressed_keys[K_s]: self.rect.move_ip(0, 5)
        if pressed_keys[K_a]: self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]: self.rect.move_ip(5, 0)

        if pressed_keys[K_LSHIFT]:  # correr más rápido
            if pressed_keys[K_UP]: self.rect.move_ip(0, -8)
            if pressed_keys[K_DOWN]: self.rect.move_ip(0, 8)
            if pressed_keys[K_LEFT]: self.rect.move_ip(-8, 0)
            if pressed_keys[K_RIGHT]: self.rect.move_ip(8, 0)
            if pressed_keys[K_w]: self.rect.move_ip(0, -8)
            if pressed_keys[K_s]: self.rect.move_ip(0, 8)
            if pressed_keys[K_a]: self.rect.move_ip(-8, 0)
            if pressed_keys[K_d]: self.rect.move_ip(8, 0)

        self.rect.clamp_ip(screen.get_rect())  # no salir de pantalla

# === Objeto interactivo ===
class Objeto:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.encendido = True   # empieza encendido (brilla)

    def draw(self, surface):
        if self.encendido:
            pygame.draw.rect(surface, YELLOW, self.rect)  # encendido (brillando)
        else:
            pygame.draw.rect(surface, RED, self.rect)     # apagado

# Crear jugador
player = Player()

# Crear varios objetos
objetos = [
    Objeto(300, 200, 80, 80),
    Objeto(600, 400, 80, 80),
    Objeto(900, 250, 80, 80)
]

# Control de super botón
super_boton_visible = False
objeto_actual = None  # guarda el objeto con el que chocamos

# === Temporizador ===
START_TIME = 3 * 60  # 3 minutos en segundos
start_ticks = pygame.time.get_ticks()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # === Calcular tiempo ===
    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, START_TIME - seconds_passed)

    minutes = time_left // 60
    seconds = time_left % 60
    color = WHITE if time_left > 30 else RED
    timer_text = font.render(f"{minutes:02}:{seconds:02}", True, color)

    # === Detectar colisión con algún objeto ===
    super_boton_visible = False
    for obj in objetos:
        if player.rect.colliderect(obj.rect) and obj.encendido:
            super_boton_visible = True
            objeto_actual = obj
            break  # solo un objeto a la vez

    # Si presiono espacio y hay un objeto actual → se apaga
    if super_boton_visible and pressed_keys[K_e]:
        objeto_actual.encendido = False
        super_boton_visible = False
        objeto_actual = None
        print("⚡ Objeto apagado ⚡")

    # === Dibujar ===
    screen.blit(MAPA, (0, 0))  # dibuja el mapa de fondo
    screen.blit(player.surf, player.rect)

    for obj in objetos:
        obj.draw(screen)

    # Dibujar el temporizador arriba al centro
    screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 20))

    if super_boton_visible:
        boton_text = font.render("SUPER BOTON (E)", True, GREEN)
        screen.blit(boton_text, (player.rect.centerx - boton_text.get_width()//2,
                                 player.rect.top - 40))

    pygame.display.flip()

    # === Condiciones de fin de juego ===
    if time_left <= 0 or all(not obj.encendido for obj in objetos):
        end_text = font.render("¡Fin del nivel!", True, RED)
        screen.fill(BLACK)
        screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
