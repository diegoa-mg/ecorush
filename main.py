# === Importar bibliotecas ===
import pygame
import os
import math
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
    # Devuelve una copia borrosa de 'surf' aplicando smoothscale down/up.
    out = surf
    for _ in range(passes):
        w = max(1, int(out.get_width()  * factor))
        h = max(1, int(out.get_height() * factor))
        out = pygame.transform.smoothscale(out, (w, h))
        out = pygame.transform.smoothscale(out, surf.get_size())
    return out

# === Cargar imágenes ===

# Imágenes Menú Principal 
bg_prin      = load_img("fondoprinci.png", alpha=False) # Se pone ya que no necesita transparencia
titulo       = load_img("titulo.png")
botoninicio  = load_img("botoninicio.png")
botonconfig  = load_img("botonconfig.png")
botontuto    = load_img("botontuto.png")
botonsalir   = load_img("botonsalir.png")
config       = load_img("config.png")
"""
botoninicio_hover = load_img("botoninicio.png")
botonconfig_hover = load_img("botonconfig.png")
botontuto_hover = load_img("botontuto.png")
botonsalir_hover = load_img("botonsalir.png")
"""

# botones_config = load_img("botones_config.png")
config_x     = load_img("config_x.png")
tuto         = load_img("tuto.png")
botones_tuto = load_img("botones_tutorial.png")
bg_niv       = load_img("fondoniv.png", alpha=False)

# Imágenes del menú de niveles
titulo_niveles = load_img("tituloniveles.png")
boton_nivel1   = load_img("nivel_uno_menu.png")    
boton_nivel2   = load_img("nivel_dos_menu.png")    
boton_nivel3   = load_img("nivel_tres_menu.png")   
boton_volver   = load_img("flecha_para_regresar.png")    
boton_config_niv = load_img("configuracion_niveles.png") 

# Imagenes del selector de nivel individual
nivel_selector = load_img("selector_nivel.png")  # Ventana azul selector

titulo_niv1 = load_img("tituloniv1.png")
titulo_niv2 = load_img("tituloniv2.png")
titulo_niv3 = load_img("tituloniv3.png")

btn_sencillo   = load_img("dificultad_sencillo.png")         # Botón fácil
btn_extremo    = load_img("dificultad_extremo.png")       # Botón difícil  
personaje1     = load_img("selec_pjizq.png")   # Personaje 1
personaje2     = load_img("selec_pjder.png")    # Personaje 2
btn_jugar      = load_img("play_jugar_N.png")                 # Botón play
nivel_x        = load_img("niv_x.png")

print("Imágenes cargadas correctamente para el selector de nivel") 

# === Escalar las imagenes ===

# Imagenes menu principal
bg_prin    = pygame.transform.scale(bg_prin, (2560, 720))
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
bg_niv       = pygame.transform.scale(bg_niv, (2560, 720))

# Imágenes del menú de niveles
titulo_niveles  = pygame.transform.scale(titulo_niveles, (1118, 178))
boton_nivel1    = pygame.transform.scale(boton_nivel1, (312.66, 130))
boton_nivel2    = pygame.transform.scale(boton_nivel2, (312.66, 130))
boton_nivel3    = pygame.transform.scale(boton_nivel3, (312.66, 130))
boton_volver    = pygame.transform.scale(boton_volver, (116.66, 118.66))
boton_config_niv = pygame.transform.scale(boton_config_niv, (119.33, 118.66))

# Imagenes del selector de nivel
titulo_niv1     = pygame.transform.scale(titulo_niv1, (1118, 178))
titulo_niv2     = pygame.transform.scale(titulo_niv2, (1118, 178))
titulo_niv3     = pygame.transform.scale(titulo_niv3, (1118, 178))
nivel_selector  = pygame.transform.scale(nivel_selector, (709.33, 294.66))
btn_sencillo     = pygame.transform.scale(btn_sencillo, (184.66, 70.66))
btn_extremo     = pygame.transform.scale(btn_extremo, (184.66, 70.66))
personaje1      = pygame.transform.scale(personaje1, (184.66, 116.66))
personaje2      = pygame.transform.scale(personaje2, (184.66, 116.66))
btn_jugar       = pygame.transform.scale(btn_jugar, (100, 100))
nivel_x         = pygame.transform.scale(nivel_x, (34, 33.33))

# === ANIMACION AL TITULO ===
def draw_title_animated(screen, base_surf, center_pos, mode="bob", t_ms=0, amp=1.5,): # amp = amplitud px
    """Dibuja el título con una animación elegida por 'mode' en 'center_pos'."""
    # tiempo en segundos para funciones senoidales
    t = t_ms / 750.0

    surf = base_surf
    rect = surf.get_rect(center=center_pos)

    if mode == "bob":
        dy = int(math.sin(t * 2.5) * amp)  # velocidad 2 Hz aprox.
        rect.centery += dy
        screen.blit(surf, rect.topleft)

# === ANIMACION A BOTONES ===
def make_hover_pair(surf, scale=1.05):
    w, h = surf.get_size()
    hover = pygame.transform.smoothscale(surf, (int(w*scale), int(h*scale)))
    return surf, hover

# === ANIMACION A SELECTOR ===


# Botones Menu Principal
botoninicio_orig, botoninicio_hover = make_hover_pair(botoninicio, 1.05)
botonconfig_orig, botonconfig_hover = make_hover_pair(botonconfig, 1.05)
botontuto_orig,  botontuto_hover  = make_hover_pair(botontuto,  1.05)
botonsalir_orig, botonsalir_hover = make_hover_pair(botonsalir, 1.05)

# Botones Menu Niveles
boton_nivel1_orig, boton_nivel1_hover = make_hover_pair(boton_nivel1, 1.05)
boton_nivel2_orig, boton_nivel2_hover = make_hover_pair(boton_nivel2, 1.05)
boton_nivel3_orig, boton_nivel3_hover = make_hover_pair(boton_nivel3, 1.05)
boton_volver_orig, boton_volver_hover = make_hover_pair(boton_volver, 1.05)
boton_config_niv_orig, boton_config_niv_hover = make_hover_pair(boton_config_niv, 1.05)

# Botones Selector Nivel
btn_sencillo_orig, btn_sencillo_hover = make_hover_pair(btn_sencillo, 1.05)
btn_extremo_orig, btn_extremo_hover = make_hover_pair(btn_extremo, 1.05)
# btn_jugar

# === Definir rects de botones (hitboxes) ===

# Rects del menu principal
rect_inicio   = botoninicio.get_rect(topleft=(527, 310))
rect_config   = botonconfig.get_rect(topleft=(158, 380))
rect_tuto     = botontuto.get_rect(topleft=(793, 380))
rect_salir    = botonsalir.get_rect(topleft=(30, 572))
rect_regresar = config_x.get_rect(topleft=(244, 148.33))
config_rect   = config.get_rect(center=(WIDTH//2, HEIGHT//2))
config_x_rect = config_x.get_rect(topright=(config_rect.right-20, config_rect.top+20))
tuto_rect     = tuto.get_rect(center=(WIDTH//2, HEIGHT//2))

# Rects del menú de niveles
rect_nivel1 = boton_nivel1.get_rect(topleft=(141, 355))
rect_nivel2 = boton_nivel2.get_rect(topleft=(483.67, 355))
rect_nivel3 = boton_nivel3.get_rect(topleft=(826.33, 355))
rect_volver = boton_volver.get_rect(topleft=(30, 572)) # Esquina inferior izquierda
rect_config_niv = boton_config_niv.get_rect(topleft=(1130.67, 572))  # Esquina inferior derecha

# Rects del selector de nivel individual
nivel_selector_rect = nivel_selector.get_rect(topleft=(285.335, 300))
rect_sencillo = btn_sencillo.get_rect(topleft=(480, 330))
rect_extremo = btn_extremo.get_rect(topleft=(680, 330))
rect_personaje1 = personaje1.get_rect(topleft=(480, 430))
rect_personaje2 = personaje2.get_rect(topleft=(680, 430))
rect_jugar = btn_jugar.get_rect(bottomright=(980, 490))
nivel_x_rect = nivel_x.get_rect(topleft=(945, 315))

# === Offset Menu Principal (movimiento del fondo menu principal) ===
bg_width = bg_prin.get_width()
bg_height = bg_prin.get_height()
bg_x = 0  # desplazamiento inicial
scroll_speed = 2  # velocidad (px por frame)

# === Offset Menu Niveles (movimiento del fondo menu niveles) ===
bg_niv_width = bg_niv.get_width()
bg_niv_height = bg_niv.get_height()
bg_niv_x = 0  # desplazamiento inicial
scroll_speed_niv = 1.4  # velocidad (px por frame)

# === Estado del juego ===
game_state = "menu"

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
                    game_state = "config"
                    print("Ir a CONFIGURACIÓN")
                elif rect_tuto.collidepoint(event.pos):
                    game_state = "tutorial"
                    print("Ir a TUTORIAL") 
                elif rect_salir.collidepoint(event.pos):
                    pygame.quit()
                    raise SystemExit
            
            # Botones en config y tutorial
            elif game_state == "config":
                # Regresar al menu (click en X)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if config_x_rect.collidepoint(event.pos):
                        game_state = "menu"
                        print("Cerrando configuración.")

            elif game_state == "tutorial":
                # Regresar al menu (click en X)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if config_x_rect.collidepoint(event.pos):
                        game_state = "menu"
                        print("Cerrando tutorial.")  

            elif game_state == "config_niv":
                # Regresar al menu (click en X)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if config_x_rect.collidepoint(event.pos):
                        game_state = "niveles"
                        print("Cerrando configuración.")

            # Botones del menu niveles
            elif game_state == "niveles":
                if rect_nivel1.collidepoint(event.pos):
                    nivel_seleccionado = 1
                    game_state = "selector_nivel1"
                    print("Seleccionar opciones para Nivel 1")
                elif rect_nivel2.collidepoint(event.pos):
                    nivel_seleccionado = 2
                    game_state = "selector_nivel2"
                    print("Seleccionar opciones para Nivel 2")
                elif rect_nivel3.collidepoint(event.pos):
                    nivel_seleccionado = 3
                    game_state = "selector_nivel3"
                    print("Seleccionar opciones para Nivel 3")
                elif rect_volver.collidepoint(event.pos):
                    game_state = "menu"
                    print("Regresando al menú principal")
                elif rect_config_niv.collidepoint(event.pos):
                    previous_state = "niveles"
                    game_state = "config_niv"
                    print("Ir a CONFIGURACIÓN en niveles")

            # Botones del selector de nivel individual
            elif game_state == "selector_nivel1" or game_state == "selector_nivel2" or game_state == "selector_nivel3":
                if rect_sencillo.collidepoint(event.pos):
                    dificultad_seleccionada = "facil"
                    print("Dificultad: Fácil")
                elif rect_extremo.collidepoint(event.pos):
                    dificultad_seleccionada = "dificil"
                    print("Dificultad: Difícil")
                elif rect_personaje1.collidepoint(event.pos):
                    personaje_seleccionado = 1
                    print("Personaje 1 seleccionado")
                elif rect_personaje2.collidepoint(event.pos):
                    personaje_seleccionado = 2
                    print("Personaje 2 seleccionado")
                elif rect_jugar.collidepoint(event.pos):
                    import nivel1  # import lazy para no cargarlo hasta que lo uses
                    nivel1.run(dificultad_seleccionada, personaje_seleccionado)
                    game_state = "niveles"     # volver después del nivel
                    # game_state = f"juego_nivel{nivel_seleccionado}"
                    print(f"Iniciando Nivel {nivel_seleccionado} - Dificultad: {dificultad_seleccionada} - Personaje: {personaje_seleccionado}")
                
                # Regresar a niveles
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if nivel_x_rect.collidepoint(event.pos):
                        game_state = "niveles"
                        print("Cerrando selector.")
        
        # Usar la tecla ESC para salir de configuracion y tutorial
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state in ["config", "tutorial"]:
                game_state = "menu"

        # Tecla ESC para salir de config en niveles
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state in ["config_niv", "selector_nivel1", "selector_nivel2", "selector_nivel3"]:
                game_state = "niveles"
                    
    # === ZONA DE DIBUJO según el estado ===
    if game_state == "menu":

        # Actualizar posicion del fondo
        bg_x -= scroll_speed
        if bg_x <= -bg_width:
            bg_x = 0

        # Fondo con un poco de blur
        menu_surface.blit(bg_prin, (bg_x, 0))
        menu_surface.blit(bg_prin, (bg_x + bg_width, 0))
        blurred = make_blur(menu_surface, factor=0.60, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

        # Centro del título a partir del topleft (81, 65)
        title_center = (81 + titulo.get_width()//2, 65 + titulo.get_height()//2)
        t_ms = pygame.time.get_ticks()

        # Titulo animado
        draw_title_animated(screen, titulo, title_center, mode="bob", t_ms=t_ms, amp=10)

        # Posición del mouse para hover
        mouse_pos = pygame.mouse.get_pos()

        # BOTON INICIO
        if rect_inicio.collidepoint(mouse_pos):
            r = botoninicio_hover.get_rect(center=rect_inicio.center)
            screen.blit(botoninicio_hover, r.topleft)
        else:
            screen.blit(botoninicio_orig, rect_inicio.topleft)

        # BOTON CONFIGURACIÓN
        if rect_config.collidepoint(mouse_pos):
            r = botonconfig_hover.get_rect(center=rect_config.center)
            screen.blit(botonconfig_hover, r.topleft)
        else:
            screen.blit(botonconfig_orig, rect_config.topleft)

        # BOTON TUTORIAL
        if rect_tuto.collidepoint(mouse_pos):
            r = botontuto_hover.get_rect(center=rect_tuto.center)
            screen.blit(botontuto_hover, r.topleft)
        else:
            screen.blit(botontuto_orig, rect_tuto.topleft)

        # BOTON SALIR
        if rect_salir.collidepoint(mouse_pos):
            r = botonsalir_hover.get_rect(center=rect_salir.center)
            screen.blit(botonsalir_hover, r.topleft)
        else:
            screen.blit(botonsalir_orig, rect_salir.topleft)

    elif game_state == "config":
        bg_x -= scroll_speed
        if bg_x <= -bg_width:
             bg_x = 0

        # Poner blur al menu principal
        menu_surface.blit(bg_prin, (bg_x, 0))
        menu_surface.blit(bg_prin, (bg_x + bg_width, 0))

        # Título animado sobre menu_surface
        t_ms = pygame.time.get_ticks()
        title_center = (81 + titulo.get_width()//2, 65 + titulo.get_height()//2)
        draw_title_animated(menu_surface, titulo, title_center, mode="bob", t_ms=t_ms, amp=6)

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

    elif game_state == "tutorial":
        bg_x -= scroll_speed
        if bg_x <= -bg_width:
            bg_x = 0

        # Poner blur al menu principal
        menu_surface.fill((0, 0, 0))  
        menu_surface.blit(bg_prin, (bg_x, 0))
        menu_surface.blit(bg_prin, (bg_x + bg_width, 0))
        
        # Título animado sobre menu_surface
        t_ms = pygame.time.get_ticks()
        title_center = (81 + titulo.get_width()//2, 65 + titulo.get_height()//2)
        draw_title_animated(menu_surface, titulo, title_center, mode="bob", t_ms=t_ms, amp=6)
        
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

    # === Menú de niveles ===
    elif game_state == "niveles":
        # Actualizar posicion del fondo    
        bg_niv_x -= scroll_speed_niv
        if bg_niv_x <= -bg_niv_width:
             bg_niv_x = 0

        # Fondo
        menu_surface.blit(bg_niv, (bg_niv_x, 0))
        menu_surface.blit(bg_niv, (bg_niv_x + bg_niv_width, 0))
        blurred = make_blur(menu_surface, factor=0.60, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))
        
        # Titulo
        screen.blit(titulo_niveles, (81, 65))

        # Posición del mouse para hover
        mouse_pos = pygame.mouse.get_pos()

        # BOTON NIVEL 1
        if rect_nivel1.collidepoint(mouse_pos):
            r = boton_nivel1_hover.get_rect(center=rect_nivel1.center)
            screen.blit(boton_nivel1_hover, r.topleft)
        else:
            screen.blit(boton_nivel1_orig, rect_nivel1.topleft)

        # BOTON NIVEL 2
        if rect_nivel2.collidepoint(mouse_pos):
            r = boton_nivel2_hover.get_rect(center=rect_nivel2.center)
            screen.blit(boton_nivel2_hover, r.topleft)
        else:
            screen.blit(boton_nivel2_orig, rect_nivel2.topleft)

        # BOTON NIVEL 3
        if rect_nivel3.collidepoint(mouse_pos):
            r = boton_nivel3_hover.get_rect(center=rect_nivel3.center)
            screen.blit(boton_nivel3_hover, r.topleft)
        else:
            screen.blit(boton_nivel3_orig, rect_nivel3.topleft)

        # BOTON VOLVER
        if rect_volver.collidepoint(mouse_pos):
            r = boton_volver_hover.get_rect(center=rect_volver.center)
            screen.blit(boton_volver_hover, r.topleft)
        else:
            screen.blit(boton_volver_orig, rect_volver.topleft)

        # BOTON CONFIG
        if rect_config_niv.collidepoint(mouse_pos):
            r = boton_config_niv_hover.get_rect(center=rect_config_niv.center)
            screen.blit(boton_config_niv_hover, r.topleft)
        else:
            screen.blit(boton_config_niv_orig, rect_config_niv.topleft)

    # === Config niveles ===
    elif game_state == "config_niv":
        # Actualizar posicion del fondo
        bg_niv_x -= scroll_speed_niv
        if bg_niv_x <= -bg_niv_width:
             bg_niv_x = 0
        
        # Poner blur al menu principal
        menu_surface.blit(bg_niv, (bg_niv_x, 0))
        menu_surface.blit(bg_niv, (bg_niv_x + bg_niv_width, 0))
        menu_surface.blit(titulo_niveles, (81, 65))
        menu_surface.blit(boton_nivel1, rect_nivel1.topleft)
        menu_surface.blit(boton_nivel2, rect_nivel2.topleft)
        menu_surface.blit(boton_nivel3, rect_nivel3.topleft)
        menu_surface.blit(boton_volver, rect_volver.topleft)
        menu_surface.blit(boton_config_niv, rect_config_niv.topleft)

        blurred = make_blur(menu_surface, factor=0.40, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

        # Dibujar el panel
        screen.blit(config, config_rect.topleft)
        screen.blit(config_x, config_x_rect.topleft)

    # === Selector de nivel individual ===
    elif game_state == "selector_nivel1":
        
        # Actualizar posicion del fondo
        bg_niv_x -= scroll_speed_niv
        if bg_niv_x <= -bg_niv_width:
             bg_niv_x = 0

        # Fondo con blur (puedes usar bg_niv o uno propio)
        menu_surface.blit(bg_niv, (bg_niv_x, 0))
        menu_surface.blit(bg_niv, (bg_niv_x + bg_niv_width, 0))
        blurred = make_blur(menu_surface, factor=0.60, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))

        # Titulo
        screen.blit(titulo_niv1, (81, 65))

        # Ventana azul del selector
        screen.blit(nivel_selector, nivel_selector_rect.topleft)
        screen.blit(nivel_x, nivel_x_rect.topleft)

        # Botones de dificultad
        screen.blit(btn_sencillo, rect_sencillo.topleft)
        screen.blit(btn_extremo, rect_extremo.topleft)

        # Personajes
        screen.blit(personaje1, rect_personaje1.topleft)
        screen.blit(personaje2, rect_personaje2.topleft)

        # Botón jugar
        screen.blit(btn_jugar, rect_jugar.topleft)

    elif game_state == "selector_nivel2":
        # Actualizar posicion del fondo    
        bg_niv_x -= scroll_speed_niv
        if bg_niv_x <= -bg_niv_width:
             bg_niv_x = 0

        # Fondo con blur (puedes usar bg_niv o uno propio)
        menu_surface.blit(bg_niv, (bg_niv_x, 0))
        menu_surface.blit(bg_niv, (bg_niv_x + bg_niv_width, 0))
        blurred = make_blur(menu_surface, factor=0.60, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))

        # Titulo
        screen.blit(titulo_niv2, (81, 65))

        # Ventana azul del selector
        screen.blit(nivel_selector, nivel_selector_rect.topleft)
        screen.blit(nivel_x, nivel_x_rect.topleft)

        # Botones de dificultad
        screen.blit(btn_sencillo, rect_sencillo.topleft)
        screen.blit(btn_extremo, rect_extremo.topleft)

        # Personajes
        screen.blit(personaje1, rect_personaje1.topleft)
        screen.blit(personaje2, rect_personaje2.topleft)

        # Botón jugar
        screen.blit(btn_jugar, rect_jugar.topleft)

    elif game_state == "selector_nivel3":
        # Actualizar posicion del fondo    
        bg_niv_x -= scroll_speed_niv
        if bg_niv_x <= -bg_niv_width:
             bg_niv_x = 0

        # Fondo con blur (puedes usar bg_niv o uno propio)
        menu_surface.blit(bg_niv, (bg_niv_x, 0))
        menu_surface.blit(bg_niv, (bg_niv_x + bg_niv_width, 0))
        blurred = make_blur(menu_surface, factor=0.60, passes=2)
        screen.blit(blurred, (0, 0))
        menu_surface.fill((0, 0, 0))

        # Titulo
        screen.blit(titulo_niv3, (81, 65))

        # Ventana azul del selector
        screen.blit(nivel_selector, nivel_selector_rect.topleft)
        screen.blit(nivel_x, nivel_x_rect.topleft)

        # Botones de dificultad
        screen.blit(btn_sencillo, rect_sencillo.topleft)
        screen.blit(btn_extremo, rect_extremo.topleft)

        # Personajes
        screen.blit(personaje1, rect_personaje1.topleft)
        screen.blit(personaje2, rect_personaje2.topleft)

        # Botón jugar
        screen.blit(btn_jugar, rect_jugar.topleft)

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
