from pathlib import Path
import pygame 
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
            
        self.direccion = 1 
        self.activo = True  

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
        
        progreso = 1.0 - (distancia_actual / self.distancia_total)
        
        desviacion_y = 4 * self.altura_arco * progreso * (1 - progreso)
        
        x_int = int(self.x)
        y_int = int(self.y - desviacion_y)
        
        pos_x = x_int - self.ancho_actual // 2
        pos_y = y_int - self.alto_actual // 2 
        
        surface.blit(self.img_dardo, (pos_x, pos_y))

class Boton:

  def __init__(
      self,
      x,
      y,
      ancho,
      alto,
      texto,
      color_bg=(60, 60, 80),
      color_texto=(255, 255, 255),
      tamano_fuente=14,
  ):
    self.rect = pygame.Rect(x, y, ancho, alto)
    self.texto = texto
    self.color_bg = color_bg

    self.color_hover = (
        min(color_bg[0] + 30, 255),
        min(color_bg[1] + 30, 255),
        min(color_bg[2] + 30, 255),
    )
    self.color_texto = color_texto

    self.BASE_DIR = Path(__file__).resolve().parent.parent
    self.FONTS_DIR = self.BASE_DIR / "assets" / "fonts"
    ruta_fuente = self.FONTS_DIR / "PressStart2P-Regular.ttf"

    self.fuente = pygame.font.Font(str(ruta_fuente), tamano_fuente)

  def dibujar(self, surface):
    pos_mouse = pygame.mouse.get_pos()
    color_actual = (
        self.color_hover
        if self.rect.collidepoint(pos_mouse)
        else self.color_bg
    )

    pygame.draw.rect(surface, color_actual, self.rect, border_radius=6)
    pygame.draw.rect(
        surface, (150, 150, 200), self.rect, width=2, border_radius=6
    )

    txt_surface = self.fuente.render(self.texto, True, self.color_texto)
    txt_rect = txt_surface.get_rect(center=self.rect.center)
    surface.blit(txt_surface, txt_rect)

  def fue_clicado(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if self.rect.collidepoint(event.pos):
        return True
    return False
