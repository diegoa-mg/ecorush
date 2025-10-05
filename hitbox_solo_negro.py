import pygame

class HitboxSoloNegro:
    def __init__(self, imagen_mapa, umbral_negro=30):
        """
        Sistema que SOLO detecta píxeles negros (paredes) y NO las áreas de colores
        """
        self.mapa = imagen_mapa
        self.umbral = umbral_negro
        self.ancho, self.alto = imagen_mapa.get_size()
        
        # Crear máscara SOLO para píxeles negros
        self.mascara = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self._crear_mascara_solo_negro()
    
    def _crear_mascara_solo_negro(self):
        """Crea máscara SOLO para píxeles negros, ignorando áreas de colores"""
        for y in range(self.alto):
            for x in range(self.ancho):
                color = self.mapa.get_at((x, y))
                
                # Solo detectar píxeles que sean NEGROS (no azules, grises, etc.)
                # Un píxel es negro si R, G y B son todos muy bajos
                if (color[0] < self.umbral and 
                    color[1] < self.umbral and 
                    color[2] < self.umbral and
                    color[3] > 200):  # Y no es transparente
                    
                    self.mascara.set_at((x, y), (255, 0, 0, 128))  # Rojo para debug
    
    def verificar_colision(self, rect):
        """
        Verifica colisión SOLO con píxeles negros (paredes)
        """
        # Verificar puntos clave del rectángulo
        puntos = [
            (rect.left, rect.top),
            (rect.right-1, rect.top),
            (rect.left, rect.bottom-1),
            (rect.right-1, rect.bottom-1),
            (rect.centerx, rect.centery)
        ]
        
        for x, y in puntos:
            if 0 <= x < self.ancho and 0 <= y < self.alto:
                color = self.mascara.get_at((x, y))
                if color[0] > 0:  # Si hay rojo en la máscara (píxel negro detectado)
                    return True
        return False
    
    def dibujar_debug(self, surface):
        """Dibuja SOLO las áreas negras detectadas"""
        surface.blit(self.mascara, (0, 0))
    
    def ajustar_sensibilidad(self, nuevo_umbral):
        """Permite ajustar la sensibilidad de detección de negro"""
        self.umbral = nuevo_umbral
        self._crear_mascara_solo_negro()
