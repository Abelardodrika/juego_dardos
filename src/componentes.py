from pathlib import Path
import pygame # type: ignore
import math   

class BarraPrecision:
    def __init__(self, x, y, ancho, alto, orientacion="H", velocidad=5):
        """
        orientacion: "H" para barra horizontal, "V" para barra vertical
        """
        self.rect_barra = pygame.Rect(x, y, ancho, alto)
        self.orientacion = orientacion
        self.velocidad = velocidad
        
        # El indicador es la línea que se mueve dentro de la barra
        if self.orientacion == "H":
            self.indicador_pos = x
        else:
            self.indicador_pos = y
            
        self.direccion = 1  # 1 significa avanzando, -1 retrocediendo
        self.activo = True   # Controla si la barra se está moviendo o ya se detuvo

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.IMAGES_DIR = self.BASE_DIR / "assets" / "images"

        if self.orientacion == "H":
            # Fondo y Mira Horizontal
            self.img_fondo = pygame.image.load(str(self.IMAGES_DIR / "barras" / "barrahorizontal.png")).convert_alpha()
            self.img_marcador = pygame.image.load(str(self.IMAGES_DIR / "barras" / "punto.png")).convert_alpha()
        else:
            # Fondo y Mira Vertical
            self.img_fondo = pygame.image.load(str(self.IMAGES_DIR / "barras" / "barravertical.png")).convert_alpha()
            self.img_marcador = pygame.image.load(str(self.IMAGES_DIR / "barras" / "punto.png")).convert_alpha()

    def actualizar(self):
        if not self.activo:
            return

        # Movimiento tipo Ping-Pong ajustado para que el punto rebote por dentro
        if self.orientacion == "H":
            self.indicador_pos += self.velocidad * self.direccion
            
            # Restamos el ancho del marcador para que rebote exacto en el borde derecho interno
            limite_derecho = self.rect_barra.right - self.img_marcador.get_width()
            if self.indicador_pos >= limite_derecho:
                self.indicador_pos = limite_derecho
                self.direccion = -1
            elif self.indicador_pos <= self.rect_barra.left:
                self.indicador_pos = self.rect_barra.left
                self.direccion = 1
        else:
            self.indicador_pos += self.velocidad * self.direccion
            
            # Restamos el alto del marcador para que rebote exacto en el borde inferior interno
            limite_inferior = self.rect_barra.bottom - self.img_marcador.get_height()
            if self.indicador_pos >= limite_inferior:
                self.indicador_pos = limite_inferior
                self.direccion = -1
            elif self.indicador_pos <= self.rect_barra.top:
                self.indicador_pos = self.rect_barra.top
                self.direccion = 1

    def detener(self):
        self.activo = False
        if self.orientacion == "H":
            return self.indicador_pos + (self.img_marcador.get_width() / 2)
        else:
            return self.indicador_pos + (self.img_marcador.get_height() / 2)

    def dibujar(self, surface):
        # 1. Dibujar el fondo de la barra Pixel Art
        surface.blit(self.img_fondo, self.rect_barra)
        
        # 2. Dibujar la mira láser pixel art encima del fondo
        if self.orientacion == "H":
            # En la barra horizontal, Y siempre es la parte superior de la barra
            surface.blit(self.img_marcador, (self.indicador_pos, self.rect_barra.top))
        else:
            # En la barra vertical, X siempre es la parte izquierda de la barra
            surface.blit(self.img_marcador, (self.rect_barra.left, self.indicador_pos))
class Dardo:
    def __init__(self, x_inicio, y_inicio):
        # El dardo mantiene siempre su tamaño fijo en 2D
        self.ancho_actual = 6
        self.alto_actual = 30
        
        # Puntos de origen
        self.x_inicio = x_inicio
        self.y_inicio = y_inicio
        self.x = x_inicio
        self.y = y_inicio
        
        # Destinos calculados
        self.destino_x = 0
        self.destino_y = 0
        
        self.velocidad = 15.0  
        self.distancia_total = 1.0
        
        # Altura máxima en píxeles que alcanzará la curva en el aire
        self.altura_arco = 120 

    def iniciar_vuelo(self, dest_x, dest_y):
        self.x = self.x_inicio
        self.y = self.y_inicio
        self.destino_x = dest_x
        self.destino_y = dest_y
        
        dx = self.destino_x - self.x
        dy = self.destino_y - self.y
        self.distancia_total = math.hypot(dx, dy)
        if self.distancia_total == 0: 
            self.distancia_total = 1.0

    def actualizar(self):
        dx = self.destino_x - self.x
        dy = self.destino_y - self.y
        distancia_actual = math.hypot(dx, dy)

        # Si el dardo llega al objetivo del tiro
        if distancia_actual <= self.velocidad:
            self.x = self.destino_x
            self.y = self.destino_y
            return True  
            
        # Desplazamiento lineal básico por debajo del capó
        self.x += (dx / distancia_actual) * self.velocidad
        self.y += (dy / distancia_actual) * self.velocidad
        
        return False  

    def dibujar(self, surface):
        """Aplica la desviación matemática de la parábola solo al dibujar"""
        dx = self.destino_x - self.x
        dy = self.destino_y - self.y
        distancia_actual = math.hypot(dx, dy)
        
        # Progreso del vuelo: va de 0.0 (inicio) a 1.0 (impacto)
        progreso = 1.0 - (distancia_actual / self.distancia_total)
        
        # Ecuación cuadrática para formar el arco perfecto
        desviacion_y = 4 * self.altura_arco * progreso * (1 - progreso)
        
        # Restamos en Y para elevar visualmente el dardo hacia arriba de la pantalla
        x_int = int(self.x)
        y_int = int(self.y - desviacion_y)
        
        rect_barra = pygame.Rect(
            x_int - self.ancho_actual // 2, 
            y_int - self.alto_actual // 2, 
            self.ancho_actual, 
            self.alto_actual
        )
        pygame.draw.rect(surface, (255, 50, 50), rect_barra)
