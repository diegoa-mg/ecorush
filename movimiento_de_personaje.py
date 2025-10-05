import pygame
from pathlib import Path

class AnimacionPersonaje:
    def __init__(self, assets_path):
        """
        Clase para manejar las animaciones del personaje
        assets_path: ruta a la carpeta de assets
        """
        self.assets_path = Path(assets_path)
        self.animaciones = {}
        self.direccion_actual = "idle"
        self.frame_actual = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 200  # milisegundos entre frames (más lento para mejor fluidez)
        
        # Cargar todas las animaciones
        self._cargar_animaciones()
        
    def _cargar_animaciones(self):
        """Carga todas las imágenes de animación"""
        movimiento_path = self.assets_path / "movimiento de personaje"
        
        # Animación hacia adelante (arriba)
        self.animaciones["arriba"] = [
            pygame.image.load(movimiento_path / "frame1.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frame2.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frame3.png").convert_alpha()
        ]
        
        # Animación hacia la derecha
        self.animaciones["derecha"] = [
            pygame.image.load(movimiento_path / "frame lderecho1.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frame lderecho2.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frame lderecho3.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frame lderecho4.png").convert_alpha()
        ]
        
        # Animación hacia la izquierda
        self.animaciones["izquierda"] = [
            pygame.image.load(movimiento_path / "frime lizquierdo1.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frime lizquierdo2.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frime lizquierdo3.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frime lizquierdo4.png").convert_alpha()
        ]
        
        # Animación hacia abajo (usando frames básicos)
        self.animaciones["abajo"] = [
            pygame.image.load(movimiento_path / "frame adelante1.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frame adelante2.png").convert_alpha(),
            pygame.image.load(movimiento_path / "frame adelante3.png").convert_alpha()
        ]
        
        # Animación idle (reposo) - usando frame1
        self.animaciones["idle"] = [
            pygame.image.load(movimiento_path / "frame adelante1.png").convert_alpha()
        ]
        
        # Redimensionar todas las imágenes a un tamaño consistente
        for direccion, frames in self.animaciones.items():
            for i, frame in enumerate(frames):
                self.animaciones[direccion][i] = pygame.transform.scale(frame, (40,40))
    
    def actualizar(self, direccion, esta_moviendose, corriendo=False):
        """
        Actualiza la animación basada en la dirección y si se está moviendo
        direccion: "arriba", "abajo", "izquierda", "derecha"
        esta_moviendose: True si el personaje se está moviendo
        corriendo: True si el personaje está corriendo (Shift presionado)
        """
        tiempo_actual = pygame.time.get_ticks()
        
        # Ajustar velocidad de animación según si está corriendo
        velocidad_actual = self.velocidad_animacion // 2 if corriendo else self.velocidad_animacion
        
        # Determinar la dirección de animación
        if esta_moviendose and direccion in self.animaciones:
            nueva_direccion = direccion
        else:
            nueva_direccion = "idle"
        
        # Si cambió la dirección, reiniciar la animación
        if nueva_direccion != self.direccion_actual:
            self.direccion_actual = nueva_direccion
            self.frame_actual = 0
            self.tiempo_ultimo_frame = tiempo_actual
        
        # Avanzar al siguiente frame si ha pasado suficiente tiempo
        if tiempo_actual - self.tiempo_ultimo_frame >= velocidad_actual:
            self.frame_actual = (self.frame_actual + 1) % len(self.animaciones[self.direccion_actual])
            self.tiempo_ultimo_frame = tiempo_actual
    
    def obtener_frame_actual(self):
        """Retorna la imagen del frame actual"""
        return self.animaciones[self.direccion_actual][self.frame_actual]
    
    def obtener_direccion_movimiento(self, teclas_presionadas):
        """
        Determina la dirección del movimiento basada en las teclas presionadas
        Retorna: (direccion, esta_moviendose)
        """
        from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d
        
        # Verificar si se está moviendo
        esta_moviendose = any([
            teclas_presionadas[K_UP] or teclas_presionadas[K_w],
            teclas_presionadas[K_DOWN] or teclas_presionadas[K_s],
            teclas_presionadas[K_LEFT] or teclas_presionadas[K_a],
            teclas_presionadas[K_RIGHT] or teclas_presionadas[K_d]
        ])
        
        # Determinar dirección prioritaria (si se presionan múltiples teclas)
        if teclas_presionadas[K_UP] or teclas_presionadas[K_w]:
            direccion = "arriba"
        elif teclas_presionadas[K_DOWN] or teclas_presionadas[K_s]:
            direccion = "abajo"
        elif teclas_presionadas[K_LEFT] or teclas_presionadas[K_a]:
            direccion = "izquierda"
        elif teclas_presionadas[K_RIGHT] or teclas_presionadas[K_d]:
            direccion = "derecha"
        else:
            direccion = "idle"
        
        return direccion, esta_moviendose
