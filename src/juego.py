from pathlib import Path
import math
import pygame
from src.componentes import BarraPrecision, Dardo # <-- 1. IMPORTAMOS EL DARDO

class JuegoDardos:
    def __init__(self, screen):
        self.screen = screen
        self.running = True 
        self.clock = pygame.time.Clock()
        
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.IMAGES_DIR = self.BASE_DIR / "assets" / "images"
        
        # Carga del tablero (500x500 en posición 390, 110)
        self.img_diana = pygame.image.load(str(self.IMAGES_DIR / "tablero" / "tablero.png")).convert_alpha()
        self.img_diana = pygame.transform.scale(self.img_diana, (500, 500))

        # Centro matemático exacto de la diana
        self.centro_x = 390 + (500 / 2) # 640
        self.centro_y = 110 + (500 / 2) # 360

        # Barras de precisión
        self.barra_h = BarraPrecision(x=390, y=640, ancho=500, alto=30, orientacion="H", velocidad=7)
        self.barra_v = BarraPrecision(x=1150, y=110, ancho=30, alto=500, orientacion="V", velocidad=7)
        
        # Coordenadas reales donde impactará el dardo
        self.dardo_x = None
        self.dardo_y = None
        
        # --- 2. POSICIÓN FIJA INICIAL DEL DARDO ---
        self.dardo = Dardo(x_inicio=640, y_inicio=700)
        
        # Historial de disparos en la ronda para dibujarlos en la diana
        self.historial_dardos = [] # Almacena tuplas (x, y)
        
        # --- SISTEMA DE PUNTUACIÓN Y VIDAS ---
        self.puntaje_total = 0
        self.ultimo_puntaje = 0
        self.texto_evaluacion = ""
        self.dardos_restantes = 3
        
        # Fuente para la interfaz
        pygame.font.init()
        self.fuente_ui = pygame.font.SysFont("Arial", 24, bold=True)
        self.fuente_grande = pygame.font.SysFont("Arial", 36, bold=True)
        
        # Estados del juego: 'BARRA_H' -> 'BARRA_V' -> 'LANZAMIENTO' -> 'RESULTADO' -> 'GAME_OVER'
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
            
            # --- 3. INICIAMOS EL VUELO DEL DARDO Y CAMBIAMOS A 'LANZAMIENTO' ---
            self.dardo.iniciar_vuelo(self.dardo_x, self.dardo_y)
            self.estado_actual = 'LANZAMIENTO'
            
        elif self.estado_actual == 'RESULTADO':
            if self.dardos_restantes > 0:
                self.siguiente_lanzamiento()
            else:
                self.estado_actual = 'GAME_OVER'
                
        elif self.estado_actual == 'GAME_OVER':
            self.reiniciar_juego_completo()

    def calcular_puntuacion(self):
        # Teorema de Pitágoras para hallar la distancia al centro exacto
        distancia = math.sqrt((self.dardo_x - self.centro_x)**2 + (self.dardo_y - self.centro_y)**2)
        
        # Anillos concéntricos basados en el tamaño de 500x500 (Radio máximo = 250px)
        if distancia <= 20:
            self.ultimo_puntaje = 100
            self.texto_evaluacion = "¡CENTRO PERFECTO! (100 Pts)"
        elif distancia <= 60:
            self.ultimo_puntaje = 50
            self.texto_evaluacion = "¡EXCELENTE TIRO! (50 Pts)"
        elif distancia <= 120:
            self.ultimo_puntaje = 25
            self.texto_evaluacion = "¡BUEN TIRO! (25 Pts)"
        elif distancia <= 220:
            self.ultimo_puntaje = 10
            self.texto_evaluacion = "TIRO REGULAR (10 Pts)"
        else:
            self.ultimo_puntaje = 0
            self.texto_evaluacion = "¡FUERA DE LA DIANA! (0 Pts)"
            
        self.puntaje_total += self.ultimo_puntaje

    def siguiente_lanzamiento(self):
        self.barra_h = BarraPrecision(x=390, y=640, ancho=500, alto=30, orientacion="H", velocidad=7)
        self.barra_v = BarraPrecision(x=1150, y=110, ancho=30, alto=500, orientacion="V", velocidad=7)
        self.dardo_x = None
        self.dardo_y = None
        
        # --- 4. REESTABLECER EL DARDO ABAJO PARA EL SIGUIENTE TIRO ---
        self.dardo = Dardo(x_inicio=640, y_inicio=700)
        self.estado_actual = 'BARRA_H'

    def reiniciar_juego_completo(self):
        self.puntaje_total = 0
        self.ultimo_puntaje = 0
        self.texto_evaluacion = ""
        self.dardos_restantes = 3
        self.historial_dardos.clear()
        self.siguiente_lanzamiento()

    def actualizar(self):
        if self.estado_actual == 'BARRA_H':
            self.barra_h.actualizar()
        elif self.estado_actual == 'BARRA_V':
            self.barra_v.actualizar()
            
        # --- 5. ACTUALIZAR EL VUELO Y CALCULAR PUNTOS AL LLEGAR ---
        elif self.estado_actual == 'LANZAMIENTO':
            finalizo_vuelo = self.dardo.actualizar()
            if finalizo_vuelo:
                # Calculamos los puntos y guardamos en historial JUSTO al impactar
                self.calcular_puntuacion()
                self.historial_dardos.append((self.dardo_x, self.dardo_y))
                self.dardos_restantes -= 1
                self.estado_actual = 'RESULTADO'

    def dibujar_interface(self):
        rect_ui = pygame.Rect(30, 110, 320, 500)
        pygame.draw.rect(self.screen, (20, 20, 30), rect_ui, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 150), rect_ui, width=2, border_radius=10)
        
        txt_titulo = self.fuente_grande.render("PUNTAJE", True, (255, 255, 255))
        txt_puntos = self.fuente_grande.render(f"{self.puntaje_total} Pts", True, (0, 255, 150))
        txt_dardos = self.fuente_ui.render(f"Dardos restantes: {self.dardos_restantes}", True, (200, 200, 200))
        
        self.screen.blit(txt_titulo, (50, 130))
        self.screen.blit(txt_puntos, (50, 180))
        self.screen.blit(txt_dardos, (50, 240))
        
        if self.estado_actual in ['RESULTADO', 'GAME_OVER'] and self.texto_evaluacion:
            txt_eval = self.fuente_ui.render(self.texto_evaluacion, True, (255, 220, 0))
            self.screen.blit(txt_eval, (50, 300))
            
            if self.estado_actual == 'RESULTADO':
                txt_continuar = self.fuente_ui.render("Presiona ESPACIO...", True, (150, 150, 150))
                self.screen.blit(txt_continuar, (50, 420))
                
        if self.estado_actual == 'GAME_OVER':
            txt_go = self.fuente_grande.render("¡FIN DE LA RONDA!", True, (255, 50, 50))
            txt_reiniciar = self.fuente_ui.render("ESPACIO para reiniciar", True, (255, 255, 255))
            self.screen.blit(txt_go, (50, 380))
            self.screen.blit(txt_reiniciar, (50, 430))

    def dibujar(self):
        self.screen.fill((30, 30, 40)) 
        
        # Dibujar Tablero
        self.screen.blit(self.img_diana, (390, 110))

        # Dibujar Barras
        self.barra_h.dibujar(self.screen)
        self.barra_v.dibujar(self.screen)
        
        # Dibujar todos los dardos clavados previamente en la ronda
        for px, py in self.historial_dardos:
            pygame.draw.circle(self.screen, (0, 100, 200), (int(px), int(py)), 10)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(px), int(py)), 3)

        # --- 6. DIBUJAR EL DARDO HACIENDO SU PARÁBOLA ---
        if self.estado_actual in ['LANZAMIENTO', 'RESULTADO']:
            self.dardo.dibujar(self.screen)

        # Dibujar el dardo actual con brillo especial sobre el impacto
        if self.estado_actual == 'RESULTADO' and self.dardo_x is not None and self.dardo_y is not None:
            x_pintar = int(self.dardo_x)
            y_pintar = int(self.dardo_y)
            
            pygame.draw.circle(self.screen, (0, 255, 255), (x_pintar, y_pintar), 12)
            pygame.draw.circle(self.screen, (255, 255, 255), (x_pintar, y_pintar), 4)
            
        # Dibujar la interfaz de texto y puntos
        self.dibujar_interface()
            
        pygame.display.flip()

    def ejecutar(self):
        while self.running:
            self.procesar_eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(60)
