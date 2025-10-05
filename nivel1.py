import pygame
from pathlib import Path
from settings import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, load_img
from movimiento_de_personaje import AnimacionPersonaje
from objetos_interactuables import GestorObjetosInteractuables


def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    from pygame.locals import (
        K_UP, K_DOWN, K_LEFT, K_RIGHT,
        K_w, K_a, K_s, K_d,
        K_LSHIFT, K_e, QUIT
    )

    # Imagen del botón E
    img_boton_E = load_img("E_personaje.png")
    img_boton_E = pygame.transform.scale(img_boton_E, (50, 50))  # ajusta el tamaño

    MAPA = load_img("mapafinal.png")
    MAPA = pygame.transform.scale(MAPA, (WIDTH, HEIGHT))

    # Sistema de hitbox desactivado
    # hitbox_sistema = HitboxManual()
    
    # Inicializar gestor de objetos interactuables
    assets_path = Path(__file__).parent / "assets"
    gestor_objetos = GestorObjetosInteractuables(assets_path)

    img_temporizador = load_img("temporizador.png")
    img_temporizador = pygame.transform.scale(img_temporizador, (180, 80))

    img_advertencia = load_img("advertencia_objetos.png")
    img_advertencia = pygame.transform.scale(img_advertencia, (50, 50))  # ajusta el tamaño

    img_estante = load_img("estante.png")
    img_estante = pygame.transform.scale(img_estante, (100, 100))  # ajusta el tamaño

    # Fuente
    font = pygame.font.SysFont("Arial", 36)

    # Función para verificar colisiones - DESACTIVADA
    def colisiona_con_obstaculo(rect):
        # Sistema de hitbox desactivado - puedes moverte libremente
        return False

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
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_DOWN] or pressed_keys[K_s]: 
                self.rect.move_ip(0, 5)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_LEFT] or pressed_keys[K_a]: 
                self.rect.move_ip(-5, 0)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]: 
                self.rect.move_ip(5, 0)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect

            # Movimiento rápido con Shift
            if pressed_keys[K_LSHIFT]:  # correr más rápido
                old_rect = self.rect.copy()
                
                if pressed_keys[K_UP] or pressed_keys[K_w]: 
                    self.rect.move_ip(0, -6.5)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_DOWN] or pressed_keys[K_s]: 
                    self.rect.move_ip(0, 6.5)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_LEFT] or pressed_keys[K_a]: 
                    self.rect.move_ip(-6.5, 0)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_RIGHT] or pressed_keys[K_d]: 
                    self.rect.move_ip(6.5, 0)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect

            # Actualizar animación (incluyendo si está corriendo)
            corriendo = pressed_keys[K_LSHIFT]
            self.animacion.actualizar(direccion, esta_moviendose, corriendo)
            self.surf = self.animacion.obtener_frame_actual()

            self.rect.clamp_ip(screen.get_rect())  # no salir de pantalla

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

    # Crear hitbox del estante (ajustada para mejor colisión)
    estante_x = WIDTH - img_estante.get_width() - 263  # 263 píxeles del borde derecho
    estante_y = HEIGHT - img_estante.get_height() - 150  # 150 píxeles del borde inferior
    # Hitbox más precisa: cubre el área sólida del estante
    hitbox_margin = 7  # margen muy pequeño para colisión precisa
    estante_rect = pygame.Rect(
        estante_x + hitbox_margin, 
        estante_y + hitbox_margin, 
        img_estante.get_width() - (hitbox_margin * 2), 
        img_estante.get_height() - (hitbox_margin * 2)
    )

    # Crear objetos interactuables con imágenes (32x32)
    objetos = gestor_objetos.crear_objetos_por_defecto()
    
    # Mostrar objetos disponibles (opcional)
    gestor_objetos.listar_objetos_disponibles()

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
        hay_colision, objeto_colisionado = gestor_objetos.verificar_colision(player.rect)
        
        if hay_colision:
            super_boton_visible = True
            objeto_actual = objeto_colisionado

        # Si presiono E y hay un objeto actual → se apaga
        if super_boton_visible and pressed_keys[K_e]:
            gestor_objetos.apagar_objeto(objeto_actual)
            super_boton_visible = False
            objeto_actual = None
            print("⚡ Objeto apagado ⚡")

        # === No hay campo de visión limitada ===
        
        # === Dibujar ===
        screen.blit(MAPA, (0, 0))  # dibuja el mapa de fondo
        
        # Descomentar esta línea para ver los hitbox durante el desarrollo
        # hitbox_sistema.dibujar_debug(screen)
        
        screen.blit(player.surf, player.rect)

        # Dibujar el estante en la parte inferior derecha
        estante_x = WIDTH - img_estante.get_width() - 263 # 20 píxeles del borde derecho
        estante_y = HEIGHT - img_estante.get_height() - 150 # 20 píxeles del borde inferior
        screen.blit(img_estante, (estante_x, estante_y))

        # Dibujar todos los objetos interactuables
        gestor_objetos.dibujar_todos(screen)

        # Dibujar el temporizador arriba al centro
        # === Dibujar temporizador con fondo estilo ===
        timer_rect = img_temporizador.get_rect(midtop=(WIDTH//2, 10))
        screen.blit(img_temporizador, timer_rect.topleft)

        # Texto del tiempo (negro con borde blanco para efecto 2D)
        timer_str = f"{minutes:02}:{seconds:02}"
        base_text = font.render(timer_str, True, BLACK)   # texto negro
        outline = font.render(timer_str, True, WHITE)     # borde blanco

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

        pygame.display.flip()
