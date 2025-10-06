import pygame
from pathlib import Path

# === Configuración editable de posiciones ===
# Puedes ajustar aquí las coordenadas (x, y) de cada objeto por nombre.
# Ejemplo: "airedeventanaencendido": (250, 200)
POSICIONES_OBJETOS = {
    "airedeventanaencendido": (1200, 475),
    "lamparaencendida": (1200, 614),
    "refrigerador encendido": (885, 35),
    "tarjallenadeagua": (400, 30),
    "pcencendida": (925, 225),
    "ventiladorencendido": (600, 360),
    # Agrega más si lo deseas:
    # "ventilador encendido": (600, 360),
}

class ObjetoInteractuable:
    def __init__(self, x, y, imagen_encendida_path, nombre="objeto", imagen_apagada_path=None, hitbox_size=None, hitbox_top_left=None, hitbox_offset=None, hitbox_mode: str = "base"):
        """
        Clase para objetos interactuables con imágenes de encendido/apagado.
        x, y: posición del objeto
        imagen_encendida_path: ruta a la imagen del objeto encendido
        imagen_apagada_path: ruta opcional a la imagen del objeto apagado
        nombre: nombre identificativo del objeto
        """
        self.nombre = nombre
        self.encendido = True
        
        # Tamaños
        self.display_size = 80  # solicitado: imágenes de 40x40
        # hitbox_size puede ser int (cuadrado) o tupla (ancho, alto)
        if isinstance(hitbox_size, (list, tuple)) and len(hitbox_size) == 2:
            lado_w, lado_h = int(hitbox_size[0]), int(hitbox_size[1])
        elif isinstance(hitbox_size, (int, float)):
            lado_w = lado_h = int(hitbox_size)
        else:
            lado_w = lado_h = 37

        # Cargar y redimensionar imagen encendida
        encendida = pygame.image.load(imagen_encendida_path).convert_alpha()
        self.imagen_encendida = pygame.transform.scale(encendida, (self.display_size, self.display_size))

        # Cargar y redimensionar imagen apagada si existe
        self.imagen_apagada = None
        if imagen_apagada_path:
            try:
                apagada = pygame.image.load(imagen_apagada_path).convert_alpha()
                self.imagen_apagada = pygame.transform.scale(apagada, (self.display_size, self.display_size))
            except FileNotFoundError:
                self.imagen_apagada = None

        # Rect de imagen (posición de dibujo)
        self.image_rect = pygame.Rect(x, y, self.display_size, self.display_size)

        # Hitbox: modo de colocación
        # - "coords": usa (x, y) como top-left (si se provee)
        # - "centro": centrada en el centro de la imagen
        # - "base": centrada en la base del sprite (default)
        if hitbox_mode == "coords" and hitbox_top_left is not None:
            self.rect_bloqueo = pygame.Rect(int(hitbox_top_left[0]), int(hitbox_top_left[1]), lado_w, lado_h)
        elif hitbox_mode == "centro":
            bloque_x = self.image_rect.centerx - lado_w // 2
            bloque_y = self.image_rect.centery - lado_h // 2
            self.rect_bloqueo = pygame.Rect(bloque_x, bloque_y, lado_w, lado_h)
        else:  # "base"
            bloque_x = self.image_rect.centerx - lado_w // 2
            bloque_y = self.image_rect.bottom - lado_h
            self.rect_bloqueo = pygame.Rect(bloque_x, bloque_y, lado_w, lado_h)
        # Aplicar offset (dx, dy) si está configurado
        if hitbox_offset is not None:
            try:
                dx, dy = int(hitbox_offset[0]), int(hitbox_offset[1])
                self.rect_bloqueo.move_ip(dx, dy)
            except Exception:
                pass
        # Área de interacción ligeramente mayor para permitir pulsar E en el borde
        self.rect_interaccion = self.rect_bloqueo.inflate(8, 8)

    def draw(self, surface):
        """Dibuja el objeto en la superficie"""
        if self.encendido:
            surface.blit(self.imagen_encendida, self.image_rect.topleft)
        else:
            # Si hay imagen apagada, úsala; si no, aplicar tinte rojo
            if self.imagen_apagada:
                surface.blit(self.imagen_apagada, self.image_rect.topleft)
            else:
                imagen_roja = self.imagen_encendida.copy()
                imagen_roja.fill((255, 0, 0, 180), None, pygame.BLEND_RGBA_MULT)
                surface.blit(imagen_roja, self.image_rect.topleft)

        # No dibujar el borde azul de la hitbox

    def apagar(self):
        """Apaga el objeto (cambia a imagen apagada si existe)"""
        self.encendido = False

    def encender(self):
        """Enciende el objeto (restaura imagen encendida)"""
        self.encendido = True

class GestorObjetosInteractuables:
    def __init__(self, assets_path):
        """
        Gestor para cargar todos los objetos interactuables de la carpeta
        assets_path: ruta a la carpeta de assets
        """
        self.assets_path = Path(assets_path)
        self.objetos_disponibles = {}
        self.objetos_activos = []
        self.config_posiciones = None  # permite sobreescribir con un dict
        # Depuración: mostrar hitbox de bloqueo en rojo
        self.mostrar_hitbox = True
        # Tamaños de hitbox por objeto (nombre -> (ancho, alto) o int)
        self.tamanos_hitbox = {
            # Ancho ligeramente mayor para estos objetos
            "airedeventanaencendido": (45, 37),
            "tarjallenadeagua": (43, 37),
        }
        # Offset de hitbox por objeto (nombre -> (dx, dy))
        self.offsets_hitbox = {}
        # Modo de colocación de la hitbox: "coords" | "centro" | "base"
        self.modo_hitbox = "coords"
        # Icono de advertencia para objetos encendidos
        self.icono_advertencia = None
        try:
            icon_path = self.assets_path / "img" / "advertencia_objetos.png"
            icon = pygame.image.load(str(icon_path)).convert_alpha()
            # Escalar el icono para que se vea proporcionado con 40x40
            self.icono_advertencia = pygame.transform.scale(icon, (35, 35))
        except Exception as e:
            print(f"[Advertencia] No se pudo cargar 'advertencia_objetos.png': {e}")
        # Mapeos especiales de nombres encendida -> apagada según assets
        self.mapeo_apagado_especial = {
            "lamparaencendida": "lampaapagada",
            "airedeventanaencendido": "airedeventana1apagado",
            # Nuevos mapeos: usar EXACTAMENTE los nombres de archivo (stem)
            "refrigerador encendido": "refrigeradorapagado",
            "tarjallenadeagua": "tarja",
            "pcencendida": "pc",
            "ventiladorencendido": "ventilador_apagado",
        }
        
        # Cargar todas las imágenes de la carpeta objetos_interactuables
        self._cargar_objetos_interactuables()

    def configurar_posiciones(self, posiciones: dict):
        """Define un diccionario {nombre_objeto: (x, y)} para crear objetos en esas coordenadas."""
        self.config_posiciones = posiciones
    
    def _cargar_objetos_interactuables(self):
        """Carga todas las imágenes de la carpeta objetos_interactuables"""
        objetos_path = self.assets_path / "objetos_interactuables"
        
        if objetos_path.exists():
            # Obtener todos los archivos .png de la carpeta
            for archivo in objetos_path.glob("*.png"):
                # Crear nombre sin extensión
                nombre = archivo.stem
                self.objetos_disponibles[nombre] = str(archivo)
                print(f"Objeto cargado: {nombre}")
        else:
            print("Error: Carpeta 'objetos_interactuables' no encontrada")
    
    def crear_objeto(self, x, y, nombre_imagen):
        """
        Crea un nuevo objeto interactuable
        x, y: posición
        nombre_imagen: nombre de la imagen (sin .png)
        """
        if nombre_imagen in self.objetos_disponibles:
            # Intentar encontrar la imagen "apagada" correspondiente
            base_candidatos = [
                self.mapeo_apagado_especial.get(nombre_imagen, ""),
                nombre_imagen.replace("encendida", "apagada"),
                nombre_imagen.replace("encendido", "apagado"),
                nombre_imagen.replace("encendida", ""),
                nombre_imagen.replace("encendido", ""),
            ]
            # Añadir variantes sin espacios para coincidir con assets como "refrigeradorapagado"
            posibles_apagados = base_candidatos + [c.replace(" ", "") for c in base_candidatos if c]
            imagen_apagada_path = None
            for candidato in posibles_apagados:
                if candidato in self.objetos_disponibles:
                    imagen_apagada_path = self.objetos_disponibles[candidato]
                    break

            tam_hitbox = self.tamanos_hitbox.get(nombre_imagen)
            hitbox_top_left = (x, y) if self.modo_hitbox == "coords" else None
            hitbox_offset = self.offsets_hitbox.get(nombre_imagen)

            objeto = ObjetoInteractuable(
                x, y,
                self.objetos_disponibles[nombre_imagen],
                nombre_imagen,
                imagen_apagada_path,
                hitbox_size=tam_hitbox,
                hitbox_top_left=hitbox_top_left,
                hitbox_offset=hitbox_offset,
                hitbox_mode=self.modo_hitbox
            )
            self.objetos_activos.append(objeto)
            return objeto
        else:
            print(f"Error: Imagen '{nombre_imagen}' no encontrada")
            return None
    
    def crear_objetos_por_defecto(self):
        """Crea objetos según POSICIONES_OBJETOS o self.config_posiciones."""
        objetos_creados = []

        posiciones = self.config_posiciones if self.config_posiciones else POSICIONES_OBJETOS

        for nombre, (x, y) in posiciones.items():
            objeto = self.crear_objeto(x, y, nombre)
            if objeto:
                objetos_creados.append(objeto)

        return objetos_creados

    def configurar_hitbox_por_objeto(self, tamanos: dict):
        """Define tamaños de hitbox por nombre de objeto (int o (ancho, alto))."""
        self.tamanos_hitbox = dict(tamanos)

    def configurar_offset_hitbox_por_objeto(self, offsets: dict):
        
        """
        Define offsets (dx, dy) para la hitbox por nombre de objeto.
        Ejemplo: {"pcencendida": (4, 0), "tarjallenadeagua": (3, -2)}
        """
        self.offsets_hitbox = dict(offsets)

    def configurar_modo_hitbox(self, modo: str):
        """
        Define el modo global de colocación de hitbox:
        - "coords": top-left en la coordenada del objeto
        - "centro": centrada en el centro de la imagen
        - "base": centrada en la base del sprite
        """
        if modo in ("coords", "centro", "base"):
            self.modo_hitbox = modo
    
    def crear_todos_los_objetos(self):
        """Crea un objeto de cada tipo disponible en posiciones distribuidas"""
        objetos_creados = []
        x_inicial = 100
        y_inicial = 100
        separacion = 150
        
        x, y = x_inicial, y_inicial
        for nombre in self.objetos_disponibles.keys():
            objeto = self.crear_objeto(x, y, nombre)
            if objeto:
                objetos_creados.append(objeto)
            
            # Mover a la siguiente posición
            x += separacion
            if x > 1200:  # Si se sale del ancho, bajar fila
                x = x_inicial
                y += separacion
        
        return objetos_creados
    
    def dibujar_todos(self, surface):
        """Dibuja todos los objetos activos"""
        for objeto in self.objetos_activos:
            objeto.draw(surface)
            # Dibujar advertencia sobre objetos encendidos
            if self.icono_advertencia and objeto.encendido:
                icon_w, icon_h = self.icono_advertencia.get_size()
                x = objeto.image_rect.centerx - icon_w // 2
                y = objeto.image_rect.top - icon_h - 4  # pequeño margen superior
                surface.blit(self.icono_advertencia, (x, y))
            # Depuración de hitbox: contorno rojo de la hitbox de bloqueo
            if self.mostrar_hitbox:
                try:
                    import pygame
                    pygame.draw.rect(surface, (255, 0, 0), objeto.rect_bloqueo, 2)
                    # Mostrar también el área de interacción en amarillo
                    pygame.draw.rect(surface, (255, 255, 0), objeto.rect_interaccion, 1)
                except Exception:
                    pass
    
    def verificar_colision(self, rect_jugador):
        """
        Verifica si el jugador colisiona con algún objeto
        Retorna: (hay_colision, objeto_colisionado)
        """
        for objeto in self.objetos_activos:
            # Usar área de interacción (no el centro) para permitir presionar E estando cerca
            if rect_jugador.colliderect(objeto.rect_interaccion) and objeto.encendido:
                return True, objeto
        return False, None

    def obtener_rects_bloqueo(self):
        """Devuelve rectángulos que bloquean el movimiento del jugador."""
        return [obj.rect_bloqueo for obj in self.objetos_activos]
    
    def apagar_objeto(self, objeto):
        """Apaga un objeto específico"""
        objeto.apagar()
    
    def obtener_objetos_encendidos(self):
        """Retorna lista de objetos que están encendidos"""
        return [obj for obj in self.objetos_activos if obj.encendido]
    
    def obtener_objetos_apagados(self):
        """Retorna lista de objetos que están apagados"""
        return [obj for obj in self.objetos_activos if not obj.encendido]
    
    def listar_objetos_disponibles(self):
        """Lista todos los objetos disponibles"""
        print("Objetos disponibles:")
        for nombre in self.objetos_disponibles.keys():
            print(f"  - {nombre}")
