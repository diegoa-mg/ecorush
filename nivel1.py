import pygame
from pathlib import Path
from settings import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, load_img, make_hover_pair, make_blur
from movimiento_de_personaje import AnimacionPersonaje
from objetos_interactuables import GestorObjetosInteractuables
from objetos_decorativos import GestorObjetosDecorativos

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    # === Importar teclas ===
    from pygame.locals import (
        K_UP, K_DOWN, K_LEFT, K_RIGHT,
        K_w, K_a, K_s, K_d,
        K_LSHIFT, K_e, K_ESCAPE, QUIT
    )

    # === Cargar imagenes ===
    # Juego (nivel 1)
    img_boton_E         = load_img("E_personaje.png")
    MAPA                = load_img("mapafinal.png")
    img_temporizador    = load_img("temporizador.png")
    img_advertencia     = load_img("advertencia_objetos.png")
    barra_energia       = load_img("barra_energia.png")
    barra_energia_atras = load_img("barra_energia_detras.png")
    btn_pausa           = load_img("boton_pausa_juego.png")

    pantalla_ganador    = load_img("ganador.png")
    pantalla_perdedor   = load_img("perdedor.png")

    # Pausa
    titulo_pausa    = load_img("titulo_pausa.png")
    btn_continuar   = load_img("btn_continuar.png")
    btn_config      = load_img("btn_config.png")
    btn_salir       = load_img("btn_salir.png")
    
    # Config
    config       = load_img("config.png")
    config_x     = load_img("config_x.png")

    # === Escalar imagenes ===
    # Juego
    MAPA                = pygame.transform.scale(MAPA, (WIDTH, HEIGHT))
    img_boton_E         = pygame.transform.scale(img_boton_E, (50, 50))
    img_temporizador    = pygame.transform.scale(img_temporizador, (144, 54))
    img_advertencia     = pygame.transform.scale(img_advertencia, (50, 50))
    barra_energia       = pygame.transform.scale(barra_energia, (174, 51))
    barra_energia_atras = pygame.transform.scale(barra_energia_atras, (174, 51))
    btn_pausa           = pygame.transform.scale(btn_pausa, (51, 51))

    pantalla_ganador    = pygame.transform.scale(pantalla_ganador, (WIDTH, HEIGHT))
    pantalla_perdedor   = pygame.transform.scale(pantalla_perdedor, (WIDTH, HEIGHT))

    # Pausa
    titulo_pausa    = pygame.transform.scale(titulo_pausa, (646.66, 98))
    btn_continuar   = pygame.transform.scale(btn_continuar, (301.33, 76))
    btn_config      = pygame.transform.scale(btn_config, (301.33, 76))
    btn_salir       = pygame.transform.scale(btn_salir, (301.33, 76))

    # Config
    config       = pygame.transform.scale(config, (860, 488.66))
    config_x     = pygame.transform.scale(config_x, (34, 33.33))

    # === Animacion de botones en pausa ===
    btn_pausa_orig, btn_pausa_hover         = make_hover_pair(btn_pausa, 1.05)

    btn_continuar_orig, btn_continuar_hover = make_hover_pair(btn_continuar, 1.05)
    btn_config_orig, btn_config_hover       = make_hover_pair(btn_config, 1.05)
    btn_salir_orig, btn_salir_hover         = make_hover_pair(btn_salir, 1.05)
    config_x_orig, config_x_hover           = make_hover_pair(config_x, 1.05)

    # === Hitbox de botones ===
    rect_pausa      = btn_pausa.get_rect(topleft=(1199, 30))
    rect_conti      = btn_continuar.get_rect(topleft=(489.335, 300))
    rect_config     = btn_config.get_rect(topleft=(489.335, 400))
    rect_salir      = btn_salir.get_rect(topleft=(489.335, 500))
    config_rect     = config.get_rect(center=(WIDTH//2, HEIGHT//2))
    config_x_rect   = config_x.get_rect(topright=(config_rect.right-20, config_rect.top+20))
    
    # Inicializar gestor de objetos interactuables
    assets_path = Path(__file__).parent / "assets"
    gestor_objetos = GestorObjetosInteractuables(assets_path)
    # Configurar modo de colocación de hitbox y offsets por objeto
    gestor_objetos.configurar_modo_hitbox("centro")
    gestor_objetos.configurar_offset_hitbox_por_objeto({"pcencendida": (2, -1)})
    # Inicializar decorativos y crearlos según posiciones configuradas
    gestor_decorativos = GestorObjetosDecorativos(assets_path)
    decorativos = gestor_decorativos.crear_decorativos_por_defecto()

    # Fuente
    font = pygame.font.SysFont("Arial", 36)

    # Crear una máscara de colisión desde el mapa original
    # Crear superficie base sin transparencia
    mapa_colision = MAPA.convert()

    MASK_COLOR = (0, 0, 0)
    THRESHOLD = 40  # tolerancia

    # Crear una máscara vacía
    MAPA_MASK = pygame.Mask((WIDTH, HEIGHT))

    # Rellenar la máscara donde hay negro (o casi negro)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = mapa_colision.get_at((x, y))
            # Si los tres canales son menores que el umbral => negro
            if color[0] < THRESHOLD and color[1] < THRESHOLD and color[2] < THRESHOLD:
                MAPA_MASK.set_at((x, y), 1)
        
    # Función para verificar si una posición colisiona con áreas negras o el estante
    def colisiona_con_negro(rect):
        # Verificar los cuatro puntos de las esquinas del rectángulo
        puntos_a_verificar = [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom),
            (rect.centerx, rect.centery)
        ]
        
        for x, y in puntos_a_verificar:
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                if MAPA_MASK.get_at((x, y)):
                    return True
        return False

    def choca_con_mapa(rect):
        # Recorre el contorno del rect en pasos pequeños
        step = 2
        # lados horizontales
        for x in range(rect.left, rect.right, step):
            y1, y2 = rect.top, rect.bottom-1
            if 0 <= x < WIDTH and 0 <= y1 < HEIGHT and MAPA_MASK.get_at((x, y1)): return True
            if 0 <= x < WIDTH and 0 <= y2 < HEIGHT and MAPA_MASK.get_at((x, y2)): return True
        # lados verticales
        for y in range(rect.top, rect.bottom, step):
            x1, x2 = rect.left, rect.right-1
            if 0 <= x1 < WIDTH and 0 <= y < HEIGHT and MAPA_MASK.get_at((x1, y)): return True
            if 0 <= x2 < WIDTH and 0 <= y < HEIGHT and MAPA_MASK.get_at((x2, y)): return True
        return False
    
    def debug_dibujar_mask(screen, MAPA_MASK):
        """Dibuja en rojo las zonas detectadas como colisión (paredes negras)."""
        debug_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if MAPA_MASK.get_at((x, y)):
                    debug_surface.set_at((x, y), (255, 0, 0, 80))  # rojo semitransparente
        screen.blit(debug_surface, (0, 0))

    def colisiona_con_obstaculo(rect):
        # Colisión con paredes del mapa (negras)
        for x in range(rect.left, rect.right, 5):
            for y in range(rect.top, rect.bottom, 5):
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    if MAPA_MASK.get_at((x, y)):
                        return True

        # Objetos interactuables
        for rb in gestor_objetos.obtener_rects_bloqueo():
            if rect.colliderect(rb):
                return True

        # Objetos decorativos
        for rb in gestor_decorativos.obtener_rects_bloqueo():
            if rect.colliderect(rb):
                return True

        return False

    # Variable de energia
    MAX_ENERGY = 100

    # === Jugador ===
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            # Inicializar animaciones
            assets_path = Path(__file__).parent / "assets"
            self.animacion = AnimacionPersonaje(assets_path)
            
            # Usar el primer frame como superficie inicial
            self.surf = self.animacion.obtener_frame_actual()
            self.rect = self.surf.get_rect(center=(WIDTH//2, HEIGHT//2))

        def update(self, pressed_keys):
            # Guardar la posición actual para poder volver a ella si hay colisión
            old_rect = self.rect.copy()
            
            # Obtener dirección y estado de movimiento para animaciones
            direccion, esta_moviendose = self.animacion.obtener_direccion_movimiento(pressed_keys)
            
            # Movimiento normal
            if pressed_keys[K_UP] or pressed_keys[K_w]: 
                self.rect.move_ip(0, -5)
                self.update_energy(-0.1)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_DOWN] or pressed_keys[K_s]: 
                self.rect.move_ip(0, 5)
                self.update_energy(-0.1)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_LEFT] or pressed_keys[K_a]: 
                self.rect.move_ip(-5, 0)
                self.update_energy(-0.1)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]: 
                self.rect.move_ip(5, 0)
                self.update_energy(-0.1)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect

            # Movimiento rápido con Shift
            if pressed_keys[K_LSHIFT]:  # correr más rápido
                old_rect = self.rect.copy()
                
                if pressed_keys[K_UP] or pressed_keys[K_w]: 
                    self.rect.move_ip(0, -5.5)
                    self.update_energy(-0.5)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_DOWN] or pressed_keys[K_s]: 
                    self.rect.move_ip(0, 5.5)
                    self.update_energy(-0.5)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_LEFT] or pressed_keys[K_a]: 
                    self.rect.move_ip(-5.5, 0)
                    self.update_energy(-0.5)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_RIGHT] or pressed_keys[K_d]: 
                    self.rect.move_ip(5.5, 0)
                    self.update_energy(-0.5)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect

            # Actualizar animación (incluyendo si está corriendo)
            corriendo = pressed_keys[K_LSHIFT]
            self.animacion.actualizar(direccion, esta_moviendose, corriendo)
            self.surf = self.animacion.obtener_frame_actual()

            self.rect.clamp_ip(screen.get_rect())  # no salir de pantalla

            # ENERGIA
            self.energy = MAX_ENERGY

    # ENERGIA
    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, MAX_ENERGY))

    def draw_energy_bar(self, screen):
        bar_width = 345
        bar_height = 99
        x_offset = 10
        y_offset = 10

        pygame.draw.rect(screen, MAX_ENERGY, (x_offset, y_offset, bar_width * (self.energy / MAX_ENERGY), bar_height))

    # === Objeto interactivo ===
    class Objeto:
        def __init__(self, x, y, w, h):
            self.rect = pygame.Rect(x, y, w, h)
            self.encendido = True

        def draw(self, surface):
            # Dibujar objeto - siempre amarillo cuando está encendido
            if self.encendido:
                pygame.draw.rect(surface, YELLOW, self.rect)
            else:
                pygame.draw.rect(surface, RED, self.rect)

    # Crear jugador
    player = Player()

    # Crear objetos interactuables con imágenes (32x32)
    objetos = gestor_objetos.crear_objetos_por_defecto()
    
    # Mostrar objetos disponibles (opcional)
    gestor_objetos.listar_objetos_disponibles()

    # Control de super botón
    super_boton_visible = False
    objeto_actual = None  # guarda el objeto con el que chocamos

    # === Temporizador ===
    START_TIME = 1 * 60  # 3 minutos en segundos
    start_ticks = pygame.time.get_ticks()

    # === Estado del juego ===
    game_state = "juego" # juego, pausa, config
    total_pause_ms = 0  # acumulado de tiempo en pausa
    pause_started = None  # instante en que empezó la pausa (ms)

    # Imagen de fondo borrosa que se usará mientras esté en pausa
    paused_bg = None  # cache del blur 

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return "niveles"

            # === BOTONES PAUSA ===
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "juego":
                    if rect_pausa.collidepoint(event.pos):
                        snapshot = screen.copy()
                        paused_bg = make_blur(snapshot, factor=0.4, passes=2)
                        game_state = "pausa"
                        pause_started = pygame.time.get_ticks() # <-- se marca inicio de pausa
                
                elif game_state == "pausa":
                    if rect_conti.collidepoint(event.pos):
                        print("Continuando el nivel...")
                        # Ajuste del temporizador al salir de pausa:
                        delta = pygame.time.get_ticks() - pause_started
                        total_pause_ms += delta # <-- se acumula el tiempo pausado
                        start_ticks += delta # <-- si mantienes temporizador con start_ticks  
                        pause_started = None
                        game_state = "juego"
        
                    if rect_config.collidepoint(event.pos):
                        print("Ir a CONFIGURACION en el nivel")
                        game_state = "config"

                    if rect_salir.collidepoint(event.pos):
                        print("Regresando al menu Niveles")
                        return "niveles"
                
                elif game_state == "config":
                    if config_x_rect.collidepoint(event.pos):
                        print("Cerrando configuración.")
                        game_state = "pausa"

            # === ESC ===
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state == "juego":
                    print("Pausando.")
                    snapshot = screen.copy()
                    paused_bg = make_blur(snapshot, factor=0.4, passes=2)
                    game_state = "pausa"
                    pause_started = pygame.time.get_ticks() # <-- se marca inicio de pausa

                elif game_state == "pausa":
                    print("Continuando el nivel...")
                    delta = pygame.time.get_ticks() - pause_started
                    total_pause_ms += delta # <-- se acumula el tiempo pausado
                    start_ticks += delta # <-- si mantienes temporizador con start_ticks        
                    pause_started = None
                    game_state = "juego"
                    
                elif game_state == "config":
                    print("Cerrando configuración.")
                    game_state = "pausa"

        if game_state == "juego":
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
            hay_colision, objeto_colisionado = gestor_objetos.verificar_colision(player.rect)
            
            if hay_colision:
                super_boton_visible = True
                objeto_actual = objeto_colisionado

            # Si presiono E y hay un objeto actual → se apaga
            if super_boton_visible and pressed_keys[K_e]:
                objeto_actual.encendido = False
                super_boton_visible = False
                objeto_actual = None
                print("⚡ Objeto apagado ⚡")

            # === No hay campo de visión limitada ===
        
        # === DIBUJAR ===
        if game_state == "juego":
            screen.blit(MAPA, (0, 0))  # dibuja el mapa de fondo

            # Dibujar decorativos (muebles, alfombras, etc.)
            gestor_decorativos.dibujar_todos(screen)

            # (Estante removido: ahora no se dibuja ni carga)

            # Dibujar todos los objetos interactuables
            gestor_objetos.dibujar_todos(screen)

            # Dibujar personaje
            screen.blit(player.surf, player.rect)

            # Dibujar el temporizador arriba al centro
            # === Dibujar temporizador con fondo estilo ===
            timer_rect = img_temporizador.get_rect(midtop=(WIDTH//2, 30))
            screen.blit(img_temporizador, timer_rect.topleft)

            # Texto del tiempo (negro con borde blanco para efecto 2D)
            timer_str = f"{minutes:02}:{seconds:02}"
            base_text = font.render(timer_str, True, BLACK)   # texto negro
            outline = font.render(timer_str, True, WHITE)     # borde blanco

            # Dibujar barra de energia y boton de pausa
            screen.blit(barra_energia_atras, (30, 30))
            screen.blit(barra_energia, (30, 30))

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # BOTON PAUSA
            if rect_pausa.collidepoint(mouse_pos):
                r = btn_pausa_hover.get_rect(center=rect_pausa.center)
                screen.blit(btn_pausa_hover, r.topleft)
            else:
                screen.blit(btn_pausa_orig, rect_pausa.topleft)

            # Dibujar bordes alrededor (efecto 2D)
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                screen.blit(outline, (timer_rect.centerx - outline.get_width()//2 + dx,
                                    timer_rect.centery - outline.get_height()//2 + dy))

            # Dibujar el texto principal
            screen.blit(base_text, (timer_rect.centerx - base_text.get_width()//2,
                                    timer_rect.centery - base_text.get_height()//2))

            if super_boton_visible:
                boton_rect = img_boton_E.get_rect(midbottom=(player.rect.centerx, player.rect.top - 10))
                screen.blit(img_boton_E, boton_rect.topleft)

            # (Depuración) Mostrar máscara de colisión si presionas F1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_F1]:
                debug_dibujar_mask(screen, MAPA_MASK)

        elif game_state == "pausa":
            # Fondo (nivel) con blur
            screen.blit(paused_bg, (0, 0))

            # (Opcional) oscurecer un poco encima
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, (0, 0))

            # Titulo 
            screen.blit(titulo_pausa, (316.67, 150))

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # BOTON CONTINUAR
            if rect_conti.collidepoint(mouse_pos):
                r = btn_continuar_hover.get_rect(center=rect_conti.center)
                screen.blit(btn_continuar_hover, r.topleft)
            else:
                screen.blit(btn_continuar_orig, rect_conti.topleft)

            # BOTON CONFIGURACION
            if rect_config.collidepoint(mouse_pos):
                    r = btn_config_hover.get_rect(center=rect_config.center)
                    screen.blit(btn_config_hover, r.topleft)
            else:
                screen.blit(btn_config_orig, rect_config.topleft)

            # BOTON SALIR
            if rect_salir.collidepoint(mouse_pos):
                r = btn_salir_hover.get_rect(center=rect_salir.center)
                screen.blit(btn_salir_hover, r.topleft)
            else:
                screen.blit(btn_salir_orig, rect_salir.topleft)
            
        elif game_state == "config":
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

        pygame.display.flip()

        # === Condiciones de fin de juego ===
        if time_left <= 0:
            snapshot = screen.copy()
            paused_bg = make_blur(snapshot, factor=0.4, passes=2)

            # Fondo (nivel) con blur
            screen.blit(paused_bg, (0, 0))

            # (Opcional) oscurecer un poco encima
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, (0, 0))

            screen.blit(pantalla_perdedor, (0,0))
            pygame.display.flip()
            pygame.time.delay(3000)
            return "niveles"
        
        elif all(not obj.encendido for obj in objetos):
            snapshot = screen.copy()
            paused_bg = make_blur(snapshot, factor=0.4, passes=2)
            
            # Fondo (nivel) con blur
            screen.blit(paused_bg, (0, 0))

            # (Opcional) oscurecer un poco encima
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, (0, 0))

            screen.blit(pantalla_ganador, (0,0))
            pygame.display.flip()
            pygame.time.delay(3000)
            return "niveles"