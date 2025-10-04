import pygame
from pathlib import Path
from settings import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, load_img

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

    # Crear una máscara de colisión para las áreas negras del mapa
    MAPA_MASK = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = MAPA.get_at((x, y))
            # Si el color es negro o muy cercano al negro (considerando transparencia)
            if color[0] < 30 and color[1] < 30 and color[2] < 30:
                MAPA_MASK.set_at((x, y), (255, 0, 0, 128))  # Marcar áreas negras

    img_temporizador = load_img("temporizador.png")
    img_temporizador = pygame.transform.scale(img_temporizador, (180, 80))

    img_advertencia = load_img("advertencia_objetos.png")
    img_advertencia = pygame.transform.scale(img_advertencia, (50, 50))  # ajusta el tamaño

    img_estante = load_img("estante.png")
    img_estante = pygame.transform.scale(img_estante, (100, 100))  # ajusta el tamaño

    # Fuente
    font = pygame.font.SysFont("Arial", 36)

    # Función para verificar si una posición colisiona con áreas negras o el estante
    def colisiona_con_negro(rect):
        # Verificar colisión con el estante primero
        if rect.colliderect(estante_rect):
            return True
        
        # Verificar los cuatro puntos de las esquinas del rectángulo
        puntos_a_verificar = [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom),
            (rect.centerx, rect.centery)
        ]
        
        for x, y in puntos_a_verificar:
            # Asegurarse de que las coordenadas estén dentro de los límites
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Si el punto está en un área negra (marcada en rojo en la máscara)
                color = MAPA_MASK.get_at((x, y))
                if color[0] > 0:  # Si hay rojo en la máscara (área negra)
                    return True
        return False

    # === Jugador ===
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.surf = pygame.Surface((40, 40))
            self.surf.fill(WHITE)
            self.rect = self.surf.get_rect(center=(WIDTH//2, HEIGHT//2))

        def update(self, pressed_keys):
            # Guardar la posición actual para poder volver a ella si hay colisión
            old_rect = self.rect.copy()
            
            # Movimiento normal
            if pressed_keys[K_UP] or pressed_keys[K_w]: 
                self.rect.move_ip(0, -5)
                if colisiona_con_negro(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_DOWN] or pressed_keys[K_s]: 
                self.rect.move_ip(0, 5)
                if colisiona_con_negro(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_LEFT] or pressed_keys[K_a]: 
                self.rect.move_ip(-5, 0)
                if colisiona_con_negro(self.rect):
                    self.rect = old_rect
                    
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]: 
                self.rect.move_ip(5, 0)
                if colisiona_con_negro(self.rect):
                    self.rect = old_rect

            # Movimiento rápido con Shift
            if pressed_keys[K_LSHIFT]:  # correr más rápido
                old_rect = self.rect.copy()
                
                if pressed_keys[K_UP] or pressed_keys[K_w]: 
                    self.rect.move_ip(0, -6.5)
                    if colisiona_con_negro(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_DOWN] or pressed_keys[K_s]: 
                    self.rect.move_ip(0, 6.5)
                    if colisiona_con_negro(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_LEFT] or pressed_keys[K_a]: 
                    self.rect.move_ip(-6.5, 0)
                    if colisiona_con_negro(self.rect):
                        self.rect = old_rect
                        
                if pressed_keys[K_RIGHT] or pressed_keys[K_d]: 
                    self.rect.move_ip(6.5, 0)
                    if colisiona_con_negro(self.rect):
                        self.rect = old_rect

            self.rect.clamp_ip(screen.get_rect())  # no salir de pantalla

    # === Objeto interactivo ===
    # === Objeto interactivo con advertencia independiente ===
    class Objeto:
        def __init__(self, x, y, w, h, tiempo_amarillo, tiempo_rojo):
            self.rect = pygame.Rect(x, y, w, h)
            self.encendido = True
            self.start_time = pygame.time.get_ticks()
            self.tiempo_amarillo = tiempo_amarillo
            self.tiempo_rojo = tiempo_rojo

        def draw(self, surface):
            # Dibujar objeto normal
            if self.encendido:
                pygame.draw.rect(surface, YELLOW, self.rect)
            else:
                pygame.draw.rect(surface, RED, self.rect)

            # Calcular tiempo transcurrido
            if self.encendido:
                elapsed = (pygame.time.get_ticks() - self.start_time) // 1000  

                # Fase amarilla
                if elapsed < self.tiempo_amarillo:
                    temp = img_advertencia.copy()
                    temp.fill((255, 255, 0, 180), None, pygame.BLEND_RGBA_MULT)
                    surface.blit(temp, (self.rect.centerx - 30, self.rect.top - 70))

                # Fase roja
                elif self.tiempo_amarillo <= elapsed < self.tiempo_rojo:
                    temp = img_advertencia.copy()
                    temp.fill((255, 0, 0, 220), None, pygame.BLEND_RGBA_MULT)
                    surface.blit(temp, (self.rect.centerx - 30, self.rect.top - 70))

                # Pasado el tiempo rojo → desaparece solo
                elif elapsed >= self.tiempo_rojo:
                    self.encendido = False

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

    # Crear varios objetos
    objetos = [
        Objeto(300, 200, 80, 80, tiempo_amarillo=10, tiempo_rojo=15),  # 10s amarillo → 15s rojo → desaparece
        Objeto(600, 400, 80, 80, tiempo_amarillo=20, tiempo_rojo=25),  # 20s amarillo → 25s rojo → desaparece
        Objeto(900, 250, 80, 80, tiempo_amarillo=30, tiempo_rojo=35)   # 30s amarillo → 35s rojo → desaparece
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

        # === No hay campo de visión limitada ===
        
        # === Dibujar ===
        screen.blit(MAPA, (0, 0))  # dibuja el mapa de fondo
        
        # Descomentar esta línea para ver la máscara de colisión durante el desarrollo
        # screen.blit(MAPA_MASK, (0, 0))
        
        screen.blit(player.surf, player.rect)

        # Dibujar el estante en la parte inferior derecha
        estante_x = WIDTH - img_estante.get_width() - 263 # 20 píxeles del borde derecho
        estante_y = HEIGHT - img_estante.get_height() - 150 # 20 píxeles del borde inferior
        screen.blit(img_estante, (estante_x, estante_y))

        for obj in objetos:
            obj.draw(screen)

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

        # === Condiciones de fin de juego ===
        if time_left <= 0:
            end_text = font.render("PERDISTE", True, RED) # MENSAJE TEMPORAL
            screen.fill(BLACK)
            screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2))
            pygame.display.flip()
            pygame.time.delay(2000)
            return "niveles"
        
        elif all(not obj.encendido for obj in objetos):
            end_text = font.render("GANASTE", True, WHITE) # MENSAJE TEMPORAL
            screen.fill(BLACK)
            screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2))
            pygame.display.flip()
            pygame.time.delay(2000)
            return "niveles"