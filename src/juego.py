from pathlib import Path
import pygame
from src.componentes import BarraPrecision

class JuegoDardos:
    def __init__(self, screen):
        self.screen = screen
        self.running = True 
        self.clock = pygame.time.Clock()
        
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.IMAGES_DIR = self.BASE_DIR / "assets" / "images"
        self.img_diana = pygame.image.load(str(self.IMAGES_DIR / "tablero" / "tablero.png")).convert_alpha()
        self.img_diana = pygame.transform.scale(self.img_diana, (500, 500))


        self.barra_h = BarraPrecision(x=390, y=640, ancho=500, alto=30, orientacion="H", velocidad=7)
        self.barra_v = BarraPrecision(x=1150, y=110, ancho=30, alto=500, orientacion="V", velocidad=7)
        
        # Coordenadas reales donde impactará el dardo en la diana
        self.dardo_x = None
        self.dardo_y = None
        
        # Estado inicial
        self.estado_actual = 'BARRA_H' 
        
    def procesar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.manejar_tiro()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.manejar_tiro()

    def manejar_tiro(self):
        if self.estado_actual == 'BARRA_H':
            self.dardo_x = self.barra_h.detener()
            self.estado_actual = 'BARRA_V'
            
        elif self.estado_actual == 'BARRA_V':
            self.dardo_y = self.barra_v.detener()
            self.estado_actual = 'RESULTADO'
            
        elif self.estado_actual == 'RESULTADO':
            self.reiniciar_juego()

    def reiniciar_juego(self):
        # Aquí también cambian los valores para cuando el juego se reinicie
        self.barra_h = BarraPrecision(x=390, y=640, ancho=500, alto=30, orientacion="H", velocidad=7)
        self.barra_v = BarraPrecision(x=1150, y=110, ancho=30, alto=500, orientacion="V", velocidad=7)
        self.dardo_x = None
        self.dardo_y = None
        self.estado_actual = 'BARRA_H'

    def actualizar(self):
        if self.estado_actual == 'BARRA_H':
            self.barra_h.actualizar()
        elif self.estado_actual == 'BARRA_V':
            self.barra_v.actualizar()

    def dibujar(self):
        
        self.screen.fill((30, 30, 40)) 
        
        self.screen.blit(self.img_diana, (390, 110))

        self.barra_h.dibujar(self.screen)
        self.barra_v.dibujar(self.screen)
        
        if self.estado_actual == 'RESULTADO' and self.dardo_x is not None and self.dardo_y is not None:
            x_pintar = int(self.dardo_x)
            y_pintar = int(self.dardo_y)
            
            # Dibujo del dardo 
            pygame.draw.circle(self.screen, (0, 150, 255), (x_pintar, y_pintar), 12)
            pygame.draw.circle(self.screen, (255, 255, 255), (x_pintar, y_pintar), 4)
            
        pygame.display.flip()

    def ejecutar(self):
        while self.running:
            self.procesar_eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(60)
