import pygame
from pathlib import Path
import re

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
        """Carga todas las imágenes de animación de forma tolerante a cambios de nombre"""
        movimiento_path = self.assets_path / "movimiento de personaje"

        def natural_key(s: str):
            return [int(text) if text.isdigit() else text for text in re.split(r"(\d+)", s)]

        grupos = {
            "arriba": [],
            "derecha": [],
            "izquierda": [],
            "abajo": [],
        }

        # Agrupar por palabras clave en el nombre
        for archivo in movimiento_path.glob("*.png"):
            stem = archivo.stem.lower()
            if any(k in stem for k in ["arriba", "up", "atras", "espalda"]):
                grupos["arriba"].append(archivo)
            elif any(k in stem for k in ["derecha", "derecho", "right"]):
                grupos["derecha"].append(archivo)
            elif any(k in stem for k in ["izquierda", "izquierdo", "left"]):
                grupos["izquierda"].append(archivo)
            elif any(k in stem for k in ["adelante", "abajo", "down"]):
                grupos["abajo"].append(archivo)

        # Orden natural por número si existe
        for dir_key in grupos:
            grupos[dir_key].sort(key=lambda p: natural_key(p.stem))

        def cargar_lista(rutas):
            frames = []
            for ruta in rutas:
                try:
                    frames.append(pygame.image.load(ruta).convert_alpha())
                except FileNotFoundError:
                    print(f"[Animación] No se encontró: {ruta}")
            return frames

        # Cargar usando agrupación; si algún grupo vacío, intentar con nombres antiguos
        self.animaciones["arriba"] = cargar_lista(grupos["arriba"]) or cargar_lista([
            movimiento_path / "frame1.png",
            movimiento_path / "frame2.png",
            movimiento_path / "frame3.png",
        ])
        self.animaciones["derecha"] = cargar_lista(grupos["derecha"]) or cargar_lista([
            movimiento_path / "framelderecho1.png",
            movimiento_path / "framelderecho2.png",
            movimiento_path / "framelderecho3.png",
            movimiento_path / "framelderecho4.png",
        ])
        self.animaciones["izquierda"] = cargar_lista(grupos["izquierda"]) or cargar_lista([
            movimiento_path / "frimelizquierdo1.png",
            movimiento_path / "frimelizquierdo2.png",
            movimiento_path / "frimelizquierdo3.png",
            movimiento_path / "frimelizquierdo4.png",
        ])
        self.animaciones["abajo"] = cargar_lista(grupos["abajo"]) or cargar_lista([
            movimiento_path / "frameadelante1.png",
            movimiento_path / "frameadelante2.png",
            movimiento_path / "frameadelante3.png",
        ])

        # Si algún grupo sigue vacío, crear un placeholder para evitar crash
        for dir_key in ["arriba", "derecha", "izquierda", "abajo"]:
            if not self.animaciones[dir_key]:
                print(f"[Animación] Advertencia: No se encontraron frames para '{dir_key}'. Usando placeholder.")
                ph = pygame.Surface((40, 40), pygame.SRCALPHA)
                ph.fill((255, 0, 255, 180))
                self.animaciones[dir_key] = [ph]

        # Animación idle: tomar primer frame de 'abajo' si existe, si no, de cualquier dirección
        idle_frame = self.animaciones["abajo"][0] if self.animaciones["abajo"] else self.animaciones["arriba"][0]
        self.animaciones["idle"] = [idle_frame]
        
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
