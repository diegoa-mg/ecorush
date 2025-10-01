import pygame, os, math, sys
from settings import WIDTH, HEIGHT, FPS, load_img, make_blur, make_hover_pair, draw_title_animated

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    # === Cargar imágenes ===
    bg_prin      = load_img("fondoprinci.png", alpha=False) # Se pone ya que no necesita transparencia
    titulo       = load_img("titulo.png")
    botoninicio  = load_img("botoninicio.png")
    botonconfig  = load_img("botonconfig.png")
    botontuto    = load_img("botontuto.png")
    botonsalir   = load_img("botonsalir.png")
    config       = load_img("config.png")
    config_x     = load_img("config_x.png")
    tuto         = load_img("tuto.png")
    botones_tuto = load_img("botones_tutorial.png")

    # === Escalar las imagenes ===
    bg_prin    = pygame.transform.scale(bg_prin, (2560, 720))
    titulo       = pygame.transform.scale(titulo, (1118, 178))
    botoninicio  = pygame.transform.scale(botoninicio, (225.33, 226))
    botonconfig  = pygame.transform.scale(botonconfig, (334.66, 85.33))
    botontuto    = pygame.transform.scale(botontuto, (334.66, 85.33))
    botonsalir   = pygame.transform.scale(botonsalir, (120, 118))
    config       = pygame.transform.scale(config, (860, 488.66))
    config_x     = pygame.transform.scale(config_x, (34, 33.33))
    tuto         = pygame.transform.scale(tuto, (863.33, 485.33))
    botones_tuto = pygame.transform.scale(botones_tuto, (318, 251.33))

    # === Animacion de botones ===
    botoninicio_orig, botoninicio_hover = make_hover_pair(botoninicio, 1.05)
    botonconfig_orig, botonconfig_hover = make_hover_pair(botonconfig, 1.05)
    botontuto_orig,  botontuto_hover  = make_hover_pair(botontuto,  1.05)
    botonsalir_orig, botonsalir_hover = make_hover_pair(botonsalir, 1.05)
    config_x_orig, config_x_hover = make_hover_pair(config_x, 1.05)

    # === Definir rects de botones (hitboxes) ===
    rect_inicio   = botoninicio.get_rect(topleft=(527, 310))
    rect_config   = botonconfig.get_rect(topleft=(158, 380))
    rect_tuto     = botontuto.get_rect(topleft=(793, 380))
    rect_salir    = botonsalir.get_rect(topleft=(30, 572))
    rect_regresar = config_x.get_rect(topleft=(244, 148.33))
    config_rect   = config.get_rect(center=(WIDTH//2, HEIGHT//2))
    config_x_rect = config_x.get_rect(topright=(config_rect.right-20, config_rect.top+20))
    tuto_rect     = tuto.get_rect(center=(WIDTH//2, HEIGHT//2))

    # === Offset Menu Principal (movimiento del fondo menu principal) ===
    bg_width = bg_prin.get_width()
    bg_height = bg_prin.get_height()
    bg_x = 0  # desplazamiento inicial
    scroll_speed = 2  # velocidad (px por frame)

    # === Superficie para renderizar el menú (para blur) ===
    menu_surface = pygame.Surface((WIDTH, HEIGHT)).convert()

    # === Estado del juego ===
    game_state = "menu"

    # === Bucle principal ===
    running = True
    while running:     
        clock.tick(FPS)  
            
        for event in pygame.event.get():         
            if event.type == pygame.QUIT:             
                return "quit"

            # === Botones ===
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Botones del menu principal
                if game_state == "menu":
                    if rect_config.collidepoint(event.pos):
                        game_state = "config"
                        print("Ir a CONFIGURACIÓN")
                    elif rect_tuto.collidepoint(event.pos):
                        game_state = "tutorial"
                        print("Ir a TUTORIAL")
                    elif rect_inicio.collidepoint(event.pos):
                        print("Ir a MENU NIVELES")
                        return "niveles"
                    elif rect_salir.collidepoint(event.pos):
                        print("Cerrando el juego...")
                        return "quit"

                # Botones en config y tutorial
                elif game_state == "config":
                    if config_x_rect.collidepoint(event.pos):
                        game_state = "menu"
                        print("Cerrando configuración.")

                elif game_state == "tutorial":
                    if config_x_rect.collidepoint(event.pos):
                        game_state = "menu"
                        print("Cerrando tutorial.") 

            # Usar la tecla ESC para salir de configuracion
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state in "config":
                    game_state = "menu"
                    print("Cerrando configuración.")
            
            # Usar la tecla ESC para salir de tutorial
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state in "tutorial":
                    game_state = "menu"
                    print("Cerrando tutorial.") 
                        
        # === ZONA DE DIBUJO ===
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

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # X
            if config_x_rect.collidepoint(mouse_pos):
                r = config_x_hover.get_rect(center=config_x_rect.center)
                screen.blit(config_x_hover, r.topleft)
            else:
                screen.blit(config_x_orig, config_x_rect.topleft)

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
            
            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # X
            if config_x_rect.collidepoint(mouse_pos):
                r = config_x_hover.get_rect(center=config_x_rect.center)
                screen.blit(config_x_hover, r.topleft)
            else:
                screen.blit(config_x_orig, config_x_rect.topleft)
            
            screen.blit(botones_tuto, (481, 245))

        pygame.display.flip()
    
    return "menu"
