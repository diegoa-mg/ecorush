# === Importar bibliotecas ===
import pygame
import os
from pathlib import Path

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
clock = pygame.time.Clock() 

# === Rutas relativas con pathlib ===
# BASE_DIR: carpeta donde esta el archivo main.py
BASE_DIR = Path(__file__).resolve().parent
# IMG_DIR: carpeta donde se guardan las imagenes del proyecto
IMG_DIR = BASE_DIR / "assets" / "img"

# === Helper para cargar imagen ===
"""
- name: nombre del archivo
- alpha: True usa conver_alpha() para png con transparencia
         False usa convert() para png sin transparencia
"""
def load_img(name, alpha=True):
    path = IMG_DIR / name # une la carpeta con el nombre del archivo
    surf = pygame.image.load(str(path)) # pygame necesita string, por eso se usa el str
    return surf.convert_alpha() if alpha else surf.convert()

# === BLUR (downscale/upscale) ===
def make_blur(surf, factor=0.25, passes=2):
    """Devuelve una copia borrosa de 'surf' aplicando smoothscale down/up."""
    out = surf
    for _ in range(passes):
        w = max(1, int(out.get_width()  * factor))
        h = max(1, int(out.get_height() * factor))
        out = pygame.transform.smoothscale(out, (w, h))
        out = pygame.transform.smoothscale(out, surf.get_size())
    return out

# === Cargar imágenes ===

# Imágenes Menú Principal 
background   = load_img("fondo2.png", alpha=False)  # Se pone ya que no necesita transparencia
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

# Imágenes del menú de niveles
titulo_niveles = load_img("titulo.png")  
boton_nivel1   = load_img("nivel_uno_menu.png")    
boton_nivel2   = load_img("nivel_dos_menu.png")    
boton_nivel3   = load_img("nivel_tres_menu.png")   
boton_volver   = load_img("flecha_para_regresar.png")    
boton_config_niv = load_img("configuracion_niveles.png") 

# Imagenes del selector de nivel individual
nivel_selector = load_img("cuadro_principal_personajes.png")  # Ventana azul selector
btn_facil      = load_img("difultad_facil_emoji.png")         # Botón fácil
btn_dificil    = load_img("difultad_dificil_emoji.png")       # Botón difícil  
personaje1     = load_img("seleccion_de_personajes_IZ.png")   # Personaje 1
personaje2     = load_img("seleccion_de_personajes_D.png")    # Personaje 2
btn_jugar      = load_img("play_jugar_N.png")                 # Botón play 
texto_N        = load_img("texto_N.png")                      # Texto del nivel

print("Imágenes cargadas correctamente para el selector de nivel") 

# === Escalar las imagenes ===

# Imagenes menu principal
background   = pygame.transform.scale(background, (WIDTH, HEIGHT))
titulo       = pygame.transform.scale(titulo, (1118, 178))
botoninicio  = pygame.transform.scale(botoninicio, (225.33, 226))
botonconfig  = pygame.transform.scale(botonconfig, (334.66, 85.33))
botontuto    = pygame.transform.scale(botontuto, (334.66, 85.33))
botonsalir   = pygame.transform.scale(botonsalir, (120, 118))
config       = pygame.transform.scale(config, (860, 488.66))
# botonones_config = pygame.transform.scale(botonconfig, ())
config_x     = pygame.transform.scale(config_x, (34, 33.33))
tuto         = pygame.transform.scale(tuto, (863.33, 485.33))
botones_tuto = pygame.transform.scale(botones_tuto, (318, 251.33))
bg_niv       = pygame.transform.scale(bg_niv, (WIDTH, HEIGHT))

# Imágenes del menú de niveles
titulo_niveles  = pygame.transform.scale(titulo_niveles, (600, 120))
boton_nivel1    = pygame.transform.scale(boton_nivel1, (853, 480))
boton_nivel2    = pygame.transform.scale(boton_nivel2, (853, 480))
boton_nivel3    = pygame.transform.scale(boton_nivel3, (853, 480))
boton_volver    = pygame.transform.scale(boton_volver, (100, 80))
boton_config_niv = pygame.transform.scale(boton_config_niv, (853, 400))

# Imagenes del selector de nivel
nivel_selector  = pygame.transform.scale(nivel_selector, (600, 350))
btn_facil       = pygame.transform.scale(btn_facil, (120, 40))
btn_dificil     = pygame.transform.scale(btn_dificil, (120, 40))
personaje1      = pygame.transform.scale(personaje1, (80, 80))
personaje2      = pygame.transform.scale(personaje2, (80, 80))
btn_jugar       = pygame.transform.scale(btn_jugar, (60, 60))

# === Definir rects de botones (hitboxes) ===

# Rects del menu principal
rect_inicio   = botoninicio.get_rect(topleft=(527, 310))
rect_config   = botonconfig.get_rect(topleft=(158, 380))
rect_tuto     = botontuto.get_rect(topleft=(793, 380))
rect_salir    = botonsalir.get_rect(topleft=(30, 572))
rect_regresar = config_x.get_rect(topleft=(244, 148.33))
config_rect   = config.get_rect(center=(WIDTH//2, HEIGHT//2))
config_x_rect = config_x.get_rect(topright=(config_rect.right-10, config_rect.top+10))
tuto_rect     = tuto.get_rect(center=(WIDTH//2, HEIGHT//2))

# Rects del menú de niveles
rect_nivel1 = boton_nivel1.get_rect(center=(500, 400))      # Nivel 1 a la izquierda
rect_nivel2 = boton_nivel2.get_rect(center=(640, 400))      # Nivel 2 al centro
rect_nivel3 = boton_nivel3.get_rect(center=(760, 415))      # Nivel 3 a la derecha
rect_volver = boton_volver.get_rect(bottomleft=(0, HEIGHT)) # Esquina inferior izquierda
rect_config_niv = boton_config_niv.get_rect(bottomright=(WIDTH-50, HEIGHT-30))  # Esquina inferior derecha

# Rects del selector de nivel individual
nivel_selector_rect = nivel_selector.get_rect(center=(WIDTH//2, HEIGHT//2))
rect_facil = btn_facil.get_rect(topleft=(nivel_selector_rect.left + 50, nivel_selector_rect.top + 100))
rect_dificil = btn_dificil.get_rect(topleft=(rect_facil.left, rect_facil.bottom + 20))
rect_personaje1 = personaje1.get_rect(topleft=(nivel_selector_rect.left + 250, nivel_selector_rect.top + 100))
rect_personaje2 = personaje2.get_rect(topleft=(rect_personaje1.right + 20, rect_personaje1.top))
rect_jugar = btn_jugar.get_rect(bottomright=(nivel_selector_rect.right - 20, nivel_selector_rect.bottom - 20))

# === Offset inicial (movimiento del fondo) ===
bg_width = background.get_width()
bg_height = background.get_height()
bg_x = 0  # desplazamiento inicial
scroll_speed = 2  # velocidad (px por frame)

# === Estado del juego ===
game_state = "menu"
previous_state ="menu"

# Variables del selector de nivel
nivel_seleccionado = 1      # 1, 2 o 3
dificultad_seleccionada = "facil"   # "facil" o "dificil"
personaje_seleccionado = 1  # 1 o 2

# === Superficie para renderizar el menú (para blur) ===
menu_surface = pygame.Surface((WIDTH, HEIGHT)).convert()

# === Bucle principal ===
running = True
while running:     
    clock.tick(FPS)  
        
    for event in pygame.event.get():         
        if event.type == pygame.QUIT:             
            running = False  

        # === Botones ===
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            # Botones del menu principal
            if game_state == "menu":
                if rect_inicio.collidepoint(event.pos):
                    game_state = "niveles"
                    print("Ir a MENU NIVELES")
                elif rect_config.collidepoint(event.pos):
                    previous_state = "menu"  # Recordar que venimos del menú principal
                    game_state = "config"
                    print("Ir a CONFIGURACIÓN")
                elif rect_tuto.collidepoint(event.pos):
                    game_state = "tutorial"
                    print("Ir a TUTORIAL") 
                elif rect_salir.collidepoint(event.pos):
                    pygame.quit()
                    raise SystemExit
            
            # Botones del menu niveles
            elif game_state == "niveles":
                if rect_nivel1.collidepoint(event.pos):
                    nivel_seleccionado = 1
                    game_state = "selector_nivel"
                    print("Seleccionar opciones para Nivel 1")
                elif rect_nivel2.collidepoint(event.pos):
                    nivel_seleccionado = 2
                    game_state = "selector_nivel"
                    print("Seleccionar opciones para Nivel 2")
                elif rect_nivel3.collidepoint(event.pos):
                    nivel_seleccionado = 3
                    game_state = "selector_nivel"
                    print("Seleccionar opciones para Nivel 3")
                elif rect_volver.collidepoint(event.pos):
                    game_state = "menu"
                    print("Regresando al menú principal")
                elif rect_config_niv.collidepoint(event.pos):
                    previous_state = "niveles"
                    game_state = "config"
                    print("Ir a CONFIGURACIÓN desde niveles")

            # Botones del selector de nivel individual
            elif game_state == "selector_nivel":
                if rect_facil.collidepoint(event.pos):
                    dificultad_seleccionada = "facil"
                    print("Dificultad: Fácil")
                elif rect_dificil.collidepoint(event.pos):
                    dificultad_seleccionada = "dificil"
                    print("Dificultad: Difícil")
                elif rect_personaje1.collidepoint(event.pos):
                    personaje_seleccionado = 1
                    print("Personaje 1 seleccionado")
                elif rect_personaje2.collidepoint(event.pos):
                    personaje_seleccionado = 2
                    print("Personaje 2 seleccionado")
                elif rect_jugar.collidepoint(event.pos):
                    game_state = f"juego_nivel{nivel_seleccionado}"
                    print(f"Iniciando Nivel {nivel_seleccionado} - Dificultad: {dificultad_seleccionada} - Personaje: {personaje_seleccionado}")
        
        # Usar la tecla ESC para salir de configuracion y tutorial
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state in ["config", "tutorial"]:
                game_state = "menu"
                    
    # === ZONA DE DIBUJO según el estado ===
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
        
        # Regresar al menu (click en X)
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
        
        # Regresar al menu (click en X)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if config_x_rect.collidepoint(event.pos):
                game_state = "menu"
                print("Cerrando tutorial.")

    # === Menú de niveles ===
    elif game_state == "niveles":

        # Fondo y UI de niveles
        screen.blit(bg_niv, (0, 0))
        
        # Dibujar título
        titulo_pos = titulo_niveles.get_rect(center=(WIDTH//2, 150))
        screen.blit(titulo_niveles, titulo_pos)

        # Dibujar botones de niveles
        screen.blit(boton_nivel1, rect_nivel1.topleft)
        screen.blit(boton_nivel2, rect_nivel2.topleft)
        screen.blit(boton_nivel3, rect_nivel3.topleft)

        # Dibujar botones de navegación
        screen.blit(boton_volver, rect_volver.topleft)
        screen.blit(boton_config_niv, rect_config_niv.topleft)

    # === Selector de nivel individual ===
    elif game_state == "selector_nivel":

        # Fondo con blur (puedes usar bg_niv o uno propio)
        menu_surface.blit(bg_niv, (0, 0))
        blurred = make_blur(menu_surface, factor=0.40, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))

        # Título
        titulo_pos = titulo.get_rect(center=(WIDTH//2, 100))
        screen.blit(titulo, titulo_pos)

        # Ventana azul del selector
        screen.blit(nivel_selector, nivel_selector_rect.topleft)

        # (Re)definir rects en este estado
        rect_facil = btn_facil.get_rect(topleft=(nivel_selector_rect.left + 50, nivel_selector_rect.top + 100))
        rect_dificil = btn_dificil.get_rect(topleft=(rect_facil.left, rect_facil.bottom + 20))
        rect_personaje1 = personaje1.get_rect(topleft=(nivel_selector_rect.left + 250, nivel_selector_rect.top + 100))
        rect_personaje2 = personaje2.get_rect(topleft=(rect_personaje1.right + 20, rect_personaje1.top))
        rect_jugar = btn_jugar.get_rect(bottomright=(nivel_selector_rect.right - 20, nivel_selector_rect.bottom - 20))

        # Botones de dificultad
        screen.blit(btn_facil, rect_facil.topleft)
        screen.blit(btn_dificil, rect_dificil.topleft)

        # Personajes
        screen.blit(personaje1, rect_personaje1.topleft)
        screen.blit(personaje2, rect_personaje2.topleft)

        # Botón jugar
        screen.blit(btn_jugar, rect_jugar.topleft)

        # Texto con el nivel seleccionado
        font = pygame.font.Font(None, 36)
        texto_nivel = font.render(f"Nivel {nivel_seleccionado}", True, WHITE)
        screen.blit(texto_nivel, (nivel_selector_rect.left + 20, nivel_selector_rect.top + 20))

    # === NIVELES (pantallas de carga/placeholder) ===
    elif game_state == "juego_nivel1":
        screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        texto_nivel = font.render(f"NIVEL 1", True, WHITE)
        texto_rect = texto_nivel.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        screen.blit(texto_nivel, texto_rect)
        font_small = pygame.font.Font(None, 36)
        texto_config = font_small.render(f"Dificultad: {dificultad_seleccionada.upper()}", True, WHITE)
        config_rect = texto_config.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(texto_config, config_rect)
        texto_personaje = font_small.render(f"Personaje: {personaje_seleccionado}", True, WHITE)
        personaje_rect = texto_personaje.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(texto_personaje, personaje_rect)
        texto_info = font_small.render("Presiona ESC para regresar", True, WHITE)
        info_rect = texto_info.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(texto_info, info_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = "niveles"
        
    elif game_state == "juego_nivel2":
        screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        texto_nivel = font.render(f"NIVEL 2", True, WHITE)
        texto_rect = texto_nivel.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        screen.blit(texto_nivel, texto_rect)
        font_small = pygame.font.Font(None, 36)
        texto_config = font_small.render(f"Dificultad: {dificultad_seleccionada.upper()}", True, WHITE)
        config_rect = texto_config.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(texto_config, config_rect)
        texto_personaje = font_small.render(f"Personaje: {personaje_seleccionado}", True, WHITE)
        personaje_rect = texto_personaje.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(texto_personaje, personaje_rect)
        texto_info = font_small.render("Presiona ESC para regresar", True, WHITE)
        info_rect = texto_info.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(texto_info, info_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = "niveles"
        
    elif game_state == "juego_nivel3":
        screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        texto_nivel = font.render(f"NIVEL 3", True, WHITE)
        texto_rect = texto_nivel.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        screen.blit(texto_nivel, texto_rect)
        font_small = pygame.font.Font(None, 36)
        texto_config = font_small.render(f"Dificultad: {dificultad_seleccionada.upper()}", True, WHITE)
        config_rect = texto_config.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(texto_config, config_rect)
        texto_personaje = font_small.render(f"Personaje: {personaje_seleccionado}", True, WHITE)
        personaje_rect = texto_personaje.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(texto_personaje, personaje_rect)
        texto_info = font_small.render("Presiona ESC para regresar", True, WHITE)
        info_rect = texto_info.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(texto_info, info_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = "niveles"

    pygame.display.flip()
