from pathlib import Path
import pygame # type: ignore
import math  

class BarraPrecision:
    def __init__(self, x, y, ancho, alto, orientacion="H", velocidad=5):
        
        self.rect_barra = pygame.Rect(x, y, ancho, alto)
        self.orientacion = orientacion
        self.velocidad = velocidad
        
        if self.orientacion == "H":
            self.indicador_pos = x
        else:
            self.indicador_pos = y
            
        self.direccion = 1  # 1 significa avanzando, -1 retrocediendo
        self.activo = True   # Controla si la barra se está moviendo o ya se detuvo

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.IMAGES_DIR = self.BASE_DIR / "assets" / "images"

        if self.orientacion == "H":
            self.img_fondo = pygame.image.load(str(self.IMAGES_DIR / "barras" / "barrahorizontal.png")).convert_alpha()
            self.img_marcador = pygame.image.load(str(self.IMAGES_DIR / "barras" / "punto.png")).convert_alpha()
        else:
            self.img_fondo = pygame.image.load(str(self.IMAGES_DIR / "barras" / "barravertical.png")).convert_alpha()
            self.img_marcador = pygame.image.load(str(self.IMAGES_DIR / "barras" / "punto.png")).convert_alpha()

    def actualizar(self):
        if not self.activo:
            return

        if self.orientacion == "H":
            self.indicador_pos += self.velocidad * self.direccion
            
            limite_derecho = self.rect_barra.right - self.img_marcador.get_width()
            if self.indicador_pos >= limite_derecho:
                self.indicador_pos = limite_derecho
                self.direccion = -1
            elif self.indicador_pos <= self.rect_barra.left:
                self.indicador_pos = self.rect_barra.left
                self.direccion = 1
        else:
            self.indicador_pos += self.velocidad * self.direccion
            
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
        surface.blit(self.img_fondo, self.rect_barra)
        
        if self.orientacion == "H":
            surface.blit(self.img_marcador, (self.indicador_pos, self.rect_barra.top))
        else:
            surface.blit(self.img_marcador, (self.rect_barra.left, self.indicador_pos))
class Dardo:
    def __init__(self, x_inicio, y_inicio):

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.IMAGES_DIR = self.BASE_DIR / "assets" / "images"

        self.img_dardo = pygame.image.load(str(self.IMAGES_DIR / "dardo" / "dardo.png")).convert_alpha()

        self.ancho_actual = self.img_dardo.get_width()
        self.alto_actual = self.img_dardo.get_height() 
        
        self.x_inicio = x_inicio
        self.y_inicio = y_inicio
        self.x = x_inicio
        self.y = y_inicio
        
        self.destino_x = 0
        self.destino_y = 0
        
        self.velocidad = 15.0  
        self.distancia_total = 1.0
        
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

        if distancia_actual <= self.velocidad:
            self.x = self.destino_x
            self.y = self.destino_y
            return True  
            
        self.x += (dx / distancia_actual) * self.velocidad
        self.y += (dy / distancia_actual) * self.velocidad
        
        return False  

    def dibujar(self, surface):
        dx = self.destino_x - self.x
        dy = self.destino_y - self.y
        distancia_actual = math.hypot(dx, dy)
        
        # Progreso del vuelo: va de 0.0 (inicio) a 1.0 (impacto)
        progreso = 1.0 - (distancia_actual / self.distancia_total)
        
        desviacion_y = 4 * self.altura_arco * progreso * (1 - progreso)
        
        x_int = int(self.x)
        y_int = int(self.y - desviacion_y)
        
        pos_x = x_int - self.ancho_actual // 2
        pos_y = y_int - self.alto_actual // 2 
        
        surface.blit(self.img_dardo, (pos_x, pos_y))
