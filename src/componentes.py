from pathlib import Path
import pygame # type: ignore

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
            # En la barra horizontal, Y siempre es la parte superior de la barra
            surface.blit(self.img_marcador, (self.indicador_pos, self.rect_barra.top))
        else:
            # En la barra vertical, X siempre es la parte izquierda de la barra
            surface.blit(self.img_marcador, (self.rect_barra.left, self.indicador_pos))
