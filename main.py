# Importar bibliotecas
import pygame
import os
from pathlib import Path

# Inicializar pygame
successes, failures = pygame.init() 
print("{0} successes and {1} failures".format(successes, failures))   

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configurar la ventana y reloj
FPS = 60 
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EcoRush!")
clock = pygame.time.Clock() 


# Rutas relativas con pathlib
# BASE_DIR: carpeta donde esta el archivo main.py
BASE_DIR = Path(__file__).resolve().parent
# IMG_DIR: carpeta donde se guardan las imagenes del proyecto
IMG_DIR = BASE_DIR / "assets" / "img"

"""
Helper para cargar imagen
- name: nombre del archivo
- alpha: True usa conver_alpha() para png con transparencia
         False usa convert() para png sin transparencia
"""
def load_img(name, alpha=True):
    path = IMG_DIR / name # une la carpeta con el nombre del archivo
    surf = pygame.image.load(str(path)) # pygame necesita string, por eso se usa el str
    return surf.convert_alpha() if alpha else surf.convert()

# BLUR (downscale/upscale)
def make_blur(surf, factor=0.25, passes=2):
    """Devuelve una copia borrosa de 'surf' aplicando smoothscale down/up."""
    out = surf
    for _ in range(passes):
        w = max(1, int(out.get_width()  * factor))
        h = max(1, int(out.get_height() * factor))
        out = pygame.transform.smoothscale(out, (w, h))
        out = pygame.transform.smoothscale(out, surf.get_size())
    return out

# Cargar imagenes
background   = load_img("fondo1.png", alpha=False) # Se pone ya que no necesita transparencia
titulo       = load_img("titulo.png")
botoninicio  = load_img("botoninicio.png")
botonconfig  = load_img("botonconfig.png")
botontuto    = load_img("botontuto.png")
botonsalir   = load_img("botonsalir.png")
config       = load_img("config.png")
# botones_config = load_img("botones_config.png")
config_x     = load_img("config_x.png")
tuto         = load_img("tuto.png")
botones_tuto = load_img("botones_tutorial.png")
bg_niv       = load_img("niv_fondo1.png", alpha=False)

# Escalar las imagenes
background  = pygame.transform.scale(background, (WIDTH, HEIGHT))
titulo      = pygame.transform.scale(titulo, (1118, 178))
botoninicio = pygame.transform.scale(botoninicio, (225.33, 226))
botonconfig = pygame.transform.scale(botonconfig, (334.66, 85.33))
botontuto   = pygame.transform.scale(botontuto, (334.66, 85.33))
botonsalir  = pygame.transform.scale(botonsalir, (120, 118))
config      = pygame.transform.scale(config, (860, 488.66))
# botonones_config = pygame.transform.scale(botonconfig, ())
config_x    = pygame.transform.scale(config_x, (34, 33.33))
tuto        = pygame.transform.scale(tuto, (863.33, 485.33))
botones_tuto = pygame.transform.scale(botones_tuto, (318, 251.33))
bg_niv      = pygame.transform.scale(bg_niv, (WIDTH, HEIGHT))

# Definir rects de botones (hitboxes)
rect_inicio   = botoninicio.get_rect(topleft=(527, 310))
rect_config   = botonconfig.get_rect(topleft=(158, 380))
rect_tuto     = botontuto.get_rect(topleft=(793, 380))
rect_salir    = botonsalir.get_rect(topleft=(30, 572))
rect_regresar = config_x.get_rect(topleft=(244, 148.33))
config_rect   = config.get_rect(center=(WIDTH//2, HEIGHT//2))
config_x_rect = config_x.get_rect(topright=(config_rect.right-10, config_rect.top+10))
tuto_rect     = tuto.get_rect(center=(WIDTH//2, HEIGHT//2))

# Offset inicial (movimiento del fondo)
bg_width = background.get_width()
bg_height = background.get_height()
bg_x = 0  # desplazamiento inicial
scroll_speed = 2  # velocidad (px por frame)

# Estado del juego ---
game_state = "menu"

# --- Superficie para renderizar el menú (la usaremos para hacer el blur) ---
menu_surface = pygame.Surface((WIDTH, HEIGHT)).convert()

# Bucle principal
running = True
while running:     
    clock.tick(FPS)  
        
    for event in pygame.event.get():         
        if event.type == pygame.QUIT:             
            running = False  

        # --- Botones ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "menu":
                if rect_inicio.collidepoint(event.pos):
                    game_state = "niveles"
                    print("Ir a MENU NIVELES")
                elif rect_config.collidepoint(event.pos):
                    game_state = "config"
                    print("Ir a CONFIGURACIÓN")
                elif rect_tuto.collidepoint(event.pos):
                    game_state = "tutorial"
                    print("Ir a TUTORIAL") 
                elif rect_salir.collidepoint(event.pos):
                    pygame.quit()
                    raise SystemExit

        # Usar la tecla ESC para salir de configuracion y tutorial
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state in ["config", "tutorial"]:
                    game_state = "menu"
                    
    # --- Dibujar según el estado ---
    if game_state == "menu":

        # Actualizar posicion del fondo
        bg_x -= scroll_speed
        if bg_x <= -bg_width:
            bg_x = 0

        # Fondo con un poco de blur
        menu_surface.blit(background, (bg_x, 0))
        menu_surface.blit(background, (bg_x + bg_width, 0))
        blurred = make_blur(menu_surface, factor=0.60, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

        screen.blit(titulo, (81, 65))
        screen.blit(botoninicio, rect_inicio.topleft)
        screen.blit(botonconfig, rect_config.topleft)
        screen.blit(botontuto, rect_tuto.topleft)
        screen.blit(botonsalir, rect_salir.topleft)

    elif game_state == "config":
        bg_x -= scroll_speed
        if bg_x <= -bg_width:
             bg_x = 0

        # Poner blur al menu principal
        menu_surface.blit(background, (bg_x, 0))
        menu_surface.blit(background, (bg_x + bg_width, 0))
        menu_surface.blit(titulo, (81, 65))
        menu_surface.blit(botoninicio, rect_inicio.topleft)
        menu_surface.blit(botonconfig, rect_config.topleft)
        menu_surface.blit(botontuto,   rect_tuto.topleft)
        menu_surface.blit(botonsalir,  rect_salir.topleft)

        blurred = make_blur(menu_surface, factor=0.40, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

        # Dibujar el panel
        screen.blit(config, config_rect.topleft)
        screen.blit(config_x, config_x_rect.topleft)
        
        # Regresar al menu
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if config_x_rect.collidepoint(event.pos):
                game_state = "menu"
                print("Cerrando configuración.")

    elif game_state == "tutorial":
        bg_x -= scroll_speed
        if bg_x <= -bg_width:
             bg_x = 0

        # Poner blur al menu principal
        menu_surface.blit(background, (bg_x, 0))
        menu_surface.blit(background, (bg_x + bg_width, 0))
        menu_surface.blit(titulo, (81, 65))
        menu_surface.blit(botoninicio, rect_inicio.topleft)
        menu_surface.blit(botonconfig, rect_config.topleft)
        menu_surface.blit(botontuto,   rect_tuto.topleft)
        menu_surface.blit(botonsalir,  rect_salir.topleft)

        blurred = make_blur(menu_surface, factor=0.40, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

        # Dibujar el panel
        screen.blit(tuto, tuto_rect.topleft)
        screen.blit(config_x, config_x_rect.topleft)
        screen.blit(botones_tuto, (481, 245))
        
        # Regresar al menu
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if config_x_rect.collidepoint(event.pos):
                game_state = "menu"
                print("Cerrando tutorial.")

    # === Aqui empieza el menu de los niveles ===
    elif game_state == "niveles":
        # Todo lo que vaya en este menu va dentro de este elif
        screen.blit(bg_niv, (0, 0))

    pygame.display.flip()