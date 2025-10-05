import pygame
from pathlib import Path

class ObjetoInteractuable:
    def __init__(self, x, y, imagen_path, nombre="objeto"):
        """
        Clase para objetos interactuables con imágenes
        x, y: posición del objeto
        imagen_path: ruta a la imagen del objeto
        nombre: nombre identificativo del objeto
        """
        self.nombre = nombre
        self.encendido = True
        
        # Cargar y redimensionar imagen a 32x32
        self.imagen_original = pygame.image.load(imagen_path).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen_original, (32, 32))
        
        # Crear rectángulo de colisión
        self.rect = pygame.Rect(x, y, 32, 32)
    
    def draw(self, surface):
        """Dibuja el objeto en la superficie"""
        if self.encendido:
            # Objeto encendido - imagen normal
            surface.blit(self.imagen, self.rect.topleft)
        else:
            # Objeto apagado - imagen con tinte rojo
            imagen_roja = self.imagen.copy()
            imagen_roja.fill((255, 0, 0, 180), None, pygame.BLEND_RGBA_MULT)
            surface.blit(imagen_roja, self.rect.topleft)
    
    def apagar(self):
        """Apaga el objeto"""
        self.encendido = False
    
    def encender(self):
        """Enciende el objeto"""
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
        
        # Cargar todas las imágenes de la carpeta objetos_interactuables
        self._cargar_objetos_interactuables()
    
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
            objeto = ObjetoInteractuable(
                x, y, 
                self.objetos_disponibles[nombre_imagen], 
                nombre_imagen
            )
            self.objetos_activos.append(objeto)
            return objeto
        else:
            print(f"Error: Imagen '{nombre_imagen}' no encontrada")
            return None
    
    def crear_objetos_por_defecto(self):
        """Crea objetos por defecto distribuidos en el mapa"""
        objetos_creados = []
        
        # Lista de objetos a crear con sus posiciones
        # Usando los objetos disponibles de la carpeta
        configuracion_objetos = [
            # (x, y, nombre_imagen)
            (200, 120, "lamparaencendida"),
            (600, 120, "pcencendida"),
            (1000, 120, "airedeventanaencendido"),
            (200, 360, "refrigerador encendido"),
            (600, 360, "ventilador encendido"),
            (1000, 360, "tarja llena de agua"),
            (200, 600, "lampaapagada"),
            (600, 600, "ventilador apagado"),
            (1000, 600, "tarja"),
        ]
        
        for x, y, nombre in configuracion_objetos:
            objeto = self.crear_objeto(x, y, nombre)
            if objeto:
                objetos_creados.append(objeto)
        
        return objetos_creados
    
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
    
    def verificar_colision(self, rect_jugador):
        """
        Verifica si el jugador colisiona con algún objeto
        Retorna: (hay_colision, objeto_colisionado)
        """
        for objeto in self.objetos_activos:
            if rect_jugador.colliderect(objeto.rect) and objeto.encendido:
                return True, objeto
        return False, None
    
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
