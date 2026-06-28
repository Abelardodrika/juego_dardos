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

    def actualizar(self):
        if not self.activo:
            return

        # Movimiento tipo Ping-Pong (Vaivén)
        if self.orientacion == "H":
            self.indicador_pos += self.velocidad * self.direccion
            # Si toca el borde derecho o izquierdo, cambia de dirección
            if self.indicador_pos >= self.rect_barra.right or self.indicador_pos <= self.rect_barra.left:
                self.direccion *= -1
        else:
            self.indicador_pos += self.velocidad * self.direccion
            # Si toca el borde inferior o superior, cambia de dirección
            if self.indicador_pos >= self.rect_barra.bottom or self.indicador_pos <= self.rect_barra.top:
                self.direccion *= -1

    def detener(self):
        self.activo = False
        return self.indicador_pos

    def dibujar(self, surface):
        # Dibujar el fondo de la barra (Gris)
        pygame.draw.rect(surface, (100, 100, 100), self.rect_barra)
        
        # Dibujar los bordes de la barra (Blanco)
        pygame.draw.rect(surface, (255, 255, 255), self.rect_barra, 2)
        
        # Dibujar el indicador (Línea Roja de precisión)
        if self.orientacion == "H":
            pygame.draw.line(surface, (255, 0, 0), (self.indicador_pos, self.rect_barra.top), (self.indicador_pos, self.rect_barra.bottom), 4)
        else:
            pygame.draw.line(surface, (255, 0, 0), (self.rect_barra.left, self.indicador_pos), (self.rect_barra.right, self.indicador_pos), 4)