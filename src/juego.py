from pathlib import Path
import math
import random
import pygame
from src.componentes import BarraPrecision, Dardo 

class JuegoDardos:
    def __init__(self, screen):
        self.screen = screen
        self.running = True 
        self.clock = pygame.time.Clock()
        
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.IMAGES_DIR = self.BASE_DIR / "assets" / "images"
        self.BACKGROUNDS_DIR = self.BASE_DIR / "assets" / "backgrounds"
        self.FONTS_DIR = self.BASE_DIR / "assets" / "fonts"  # RUTA DE LA FUENTE
        
        self.img_diana = pygame.image.load(str(self.IMAGES_DIR / "tablero" / "tablero.png")).convert_alpha()
        self.img_diana = pygame.transform.scale(self.img_diana, (500, 500))

        self.img_fondo = pygame.image.load(str(self.BACKGROUNDS_DIR / "fondogame.png")).convert_alpha()
        self.img_fondo = pygame.transform.scale(self.img_fondo, (self.WIDTH, self.HEIGHT)) 

        self.centro_x = 390 + (500 / 2) 
        self.centro_y = 110 + (500 / 2) 

        self.SECTORES = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

        self.barra_h = BarraPrecision(x=390, y=640, ancho=500, alto=30, orientacion="H", velocidad=7)
        self.barra_v = BarraPrecision(x=1150, y=110, ancho=30, alto=500, orientacion="V", velocidad=7)
        
        self.dardo_x = None
        self.dardo_y = None
        
        self.dardo = Dardo(x_inicio=640, y_inicio=700)
        
        self.historial_dardos = [] # Tuplas: (x, y, es_jugador)
        
        self.PUNTAJE_INICIAL = 251
        self.puntos_jugador = self.PUNTAJE_INICIAL
        self.puntos_ia = self.PUNTAJE_INICIAL
        
        self.ultimo_descuento = 0
        self.texto_evaluacion = ""
        
        self.dardos_jugador = 3
        self.dardos_ia = 3
        
        self.turno_actual = 'JUGADOR' 
        
        self.tiempo_ia = 0
        self.objetivo_ia_x = 0
        self.objetivo_ia_y = 0

        pygame.font.init()
        ruta_fuente_arcade = str(self.FONTS_DIR / "PressStart2P-Regular.ttf")
        
        self.fuente_ui = pygame.font.Font(ruta_fuente_arcade, 12)
        self.fuente_grande = pygame.font.Font(ruta_fuente_arcade, 18)
        
        self.estado_actual = 'BARRA_H' 

    def procesar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.turno_actual == 'JUGADOR' and self.estado_actual in ['BARRA_H', 'BARRA_V']:
                        self.manejar_tiro_jugador()
                    elif self.estado_actual == 'RESULTADO':
                        self.pasar_siguiente_turno()
                    elif self.estado_actual == 'GAME_OVER':
                        self.reiniciar_juego_completo()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.turno_actual == 'JUGADOR' and self.estado_actual in ['BARRA_H', 'BARRA_V']:
                        self.manejar_tiro_jugador()
                    elif self.estado_actual == 'RESULTADO':
                        self.pasar_siguiente_turno()
                    elif self.estado_actual == 'GAME_OVER':
                        self.reiniciar_juego_completo()

    def preparar_tiro_ia(self):
        error_x = random.randint(-90, 90)
        error_y = random.randint(-90, 90)
        self.objetivo_ia_x = self.centro_x + error_x
        self.objetivo_ia_y = self.centro_y + error_y

    def manejar_tiro_jugador(self):
        if self.estado_actual == 'BARRA_H':
            self.dardo_x = self.barra_h.detener()
            self.estado_actual = 'BARRA_V'
            
        elif self.estado_actual == 'BARRA_V':
            self.dardo_y = self.barra_v.detener()
            self.dardo.iniciar_vuelo(self.dardo_x, self.dardo_y)
            self.estado_actual = 'LANZAMIENTO'

    def calcular_puntuacion_exacta(self, x, y):
        dx = x - self.centro_x
        dy = y - self.centro_y
        distancia = math.sqrt(dx**2 + dy**2)

        if distancia > 210:
            self.texto_evaluacion = "OUT OF BOARD!"
            return 0

        if distancia <= 10:
            self.texto_evaluacion = "DBL BULLSEYE! (-50)"
            return 50

        if distancia <= 25:
            self.texto_evaluacion = "SGL BULLSEYE! (-25)"
            return 25

        angulo_rad = math.atan2(-dy, dx)
        angulo_deg = math.degrees(angulo_rad)
        angulo_reloj = (90 - angulo_deg) % 360
        indice_sector = int(((angulo_reloj + 9) % 360) / 18)
        numero_base = self.SECTORES[indice_sector]

        if 110 <= distancia <= 130:
            multiplicador = 3
            tipo = f"TRIPLE {numero_base}"
        elif 190 <= distancia <= 210:
            multiplicador = 2
            tipo = f"DOUBLE {numero_base}"
        else:
            multiplicador = 1
            tipo = f"SINGLE {numero_base}"

        puntos_obtenidos = numero_base * multiplicador
        self.texto_evaluacion = f"{tipo}! (-{puntos_obtenidos})"
        return puntos_obtenidos

    def procesar_impacto(self):
        puntos_descuento = self.calcular_puntuacion_exacta(self.dardo_x, self.dardo_y)
        self.ultimo_descuento = puntos_descuento

        if self.turno_actual == 'JUGADOR':
            if self.puntos_jugador - puntos_descuento >= 0:
                self.puntos_jugador -= puntos_descuento
            else:
                self.texto_evaluacion = "BUSTED! (Anulado)"

            self.dardos_jugador -= 1
            self.historial_dardos.append((self.dardo_x, self.dardo_y, True))
        else:
            if self.puntos_ia - puntos_descuento >= 0:
                self.puntos_ia -= puntos_descuento
            else:
                self.texto_evaluacion = "CPU BUSTED! (Anulado)"

            self.dardos_ia -= 1
            self.historial_dardos.append((self.dardo_x, self.dardo_y, False))

        self.estado_actual = 'RESULTADO'

        if self.puntos_jugador == 0 or self.puntos_ia == 0:
            self.estado_actual = 'GAME_OVER'

    def pasar_siguiente_turno(self):
        if self.puntos_jugador == 0 or self.puntos_ia == 0 or (self.dardos_jugador == 0 and self.dardos_ia == 0):
            self.estado_actual = 'GAME_OVER'
            return

        if self.turno_actual == 'JUGADOR' and self.dardos_ia > 0:
            self.turno_actual = 'IA'
            self.preparar_tiro_ia()
        elif self.turno_actual == 'IA' and self.dardos_jugador > 0:
            self.turno_actual = 'JUGADOR'

        self.barra_h = BarraPrecision(x=390, y=640, ancho=500, alto=30, orientacion="H", velocidad=7)
        self.barra_v = BarraPrecision(x=1150, y=110, ancho=30, alto=500, orientacion="V", velocidad=7)
        self.dardo_x = None
        self.dardo_y = None
        self.tiempo_ia = pygame.time.get_ticks()
        
        self.dardo = Dardo(x_inicio=640, y_inicio=700)
        self.estado_actual = 'BARRA_H'

    def reiniciar_juego_completo(self):
        self.puntos_jugador = self.PUNTAJE_INICIAL
        self.puntos_ia = self.PUNTAJE_INICIAL
        self.ultimo_descuento = 0
        self.texto_evaluacion = ""
        self.dardos_jugador = 3
        self.dardos_ia = 3
        self.historial_dardos.clear()
        self.turno_actual = 'JUGADOR'
        self.barra_h = BarraPrecision(x=390, y=640, ancho=500, alto=30, orientacion="H", velocidad=7)
        self.barra_v = BarraPrecision(x=1150, y=110, ancho=30, alto=500, orientacion="V", velocidad=7)
        self.dardo_x = None
        self.dardo_y = None
        
        self.dardo = Dardo(x_inicio=640, y_inicio=700)
        self.estado_actual = 'BARRA_H'

    def actualizar(self):
        if self.turno_actual == 'IA':
            tiempo_actual = pygame.time.get_ticks()
            if self.estado_actual == 'BARRA_H':
                self.barra_h.actualizar()
                if abs(self.barra_h.indicador_pos - self.objetivo_ia_x) < 15 or (tiempo_actual - self.tiempo_ia > 1200):
                    self.dardo_x = self.barra_h.detener()
                    self.estado_actual = 'BARRA_V'
                    self.tiempo_ia = tiempo_actual
                    
            elif self.estado_actual == 'BARRA_V':
                self.barra_v.actualizar()
                if abs(self.barra_v.indicador_pos - self.objetivo_ia_y) < 15 or (tiempo_actual - self.tiempo_ia > 1200):
                    self.dardo_y = self.barra_v.detener()
                    self.dardo.iniciar_vuelo(self.dardo_x, self.dardo_y)
                    self.estado_actual = 'LANZAMIENTO'
        else:
            if self.estado_actual == 'BARRA_H':
                self.barra_h.actualizar()
            elif self.estado_actual == 'BARRA_V':
                self.barra_v.actualizar()
                
        if self.estado_actual == 'LANZAMIENTO':
            finalizo_vuelo = self.dardo.actualizar()
            if finalizo_vuelo:
                self.procesar_impacto()

    def dibujar_interface(self):
        rect_ui = pygame.Rect(30, 110, 340, 500)
        pygame.draw.rect(self.screen, (20, 20, 30), rect_ui, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 150), rect_ui, width=2, border_radius=10)
        
        str_turno = "1P TURN" if self.turno_actual == 'JUGADOR' else "CPU TURN"
        col_turno = (0, 255, 255) if self.turno_actual == 'JUGADOR' else (255, 150, 0)
        txt_turno = self.fuente_grande.render(str_turno, True, col_turno)

        txt_j1 = self.fuente_ui.render(f"1P SCORE: {self.puntos_jugador}", True, (0, 255, 150))
        txt_d_j1 = self.fuente_ui.render(f"DARTS: {self.dardos_jugador}", True, (160, 160, 160))
        
        txt_ia = self.fuente_ui.render(f"CPU SCORE: {self.puntos_ia}", True, (255, 100, 100))
        txt_d_ia = self.fuente_ui.render(f"DARTS: {self.dardos_ia}", True, (160, 160, 160))

        self.screen.blit(txt_turno, (45, 140))
        self.screen.blit(txt_j1, (45, 200))
        self.screen.blit(txt_d_j1, (45, 230))
        
        self.screen.blit(txt_ia, (45, 290))
        self.screen.blit(txt_d_ia, (45, 320))
        
        if self.estado_actual == 'RESULTADO' and self.texto_evaluacion:
            txt_eval = self.fuente_ui.render(self.texto_evaluacion, True, (255, 220, 0))
            self.screen.blit(txt_eval, (45, 380))
            
            txt_cont = self.fuente_ui.render("PRESS SPACE...", True, (130, 130, 130))
            self.screen.blit(txt_cont, (45, 440))

        if self.estado_actual == 'GAME_OVER':
            if self.puntos_jugador < self.puntos_ia:
                res_txt = "YOU WIN!"
                col_res = (0, 255, 100)
            elif self.puntos_ia < self.puntos_jugador:
                res_txt = "CPU WINS!"
                col_res = (255, 50, 50)
            else:
                res_txt = "DRAW GAME!"
                col_res = (255, 255, 0)
                
            txt_go = self.fuente_grande.render(res_txt, True, col_res)
            txt_reiniciar = self.fuente_ui.render("SPACE TO RESTART", True, (255, 255, 255))
            self.screen.blit(txt_go, (45, 390))
            self.screen.blit(txt_reiniciar, (45, 440))

    def dibujar(self):
        self.screen.blit(self.img_fondo, (0, 0)) 
        self.screen.blit(self.img_diana, (390, 110))

        self.barra_h.dibujar(self.screen)
        self.barra_v.dibujar(self.screen)
        
        for px, py, es_jugador in self.historial_dardos:
            color_dardo = (0, 150, 255) if es_jugador else (255, 50, 50)
            pygame.draw.circle(self.screen, color_dardo, (int(px), int(py)), 10)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(px), int(py)), 3)

        if self.estado_actual in ['LANZAMIENTO', 'RESULTADO']:
            self.dardo.dibujar(self.screen)

        if self.estado_actual == 'RESULTADO' and self.dardo_x is not None and self.dardo_y is not None:
            col_actual = (0, 255, 255) if self.turno_actual == 'JUGADOR' else (255, 150, 0)
            pygame.draw.circle(self.screen, col_actual, (int(self.dardo_x), int(self.dardo_y)), 12)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(self.dardo_x), int(self.dardo_y)), 4)
            
        self.dibujar_interface()
        pygame.display.flip()

    def ejecutar(self):
        while self.running:
            self.procesar_eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(60)
