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
        
        # Carga del tablero (500x500 en posición 390, 110)
        self.img_diana = pygame.image.load(str(self.IMAGES_DIR / "tablero" / "tablero.png")).convert_alpha()
        self.img_diana = pygame.transform.scale(self.img_diana, (500, 500))

        self.img_fondo = pygame.image.load(str(self.BACKGROUNDS_DIR / "fondogame.png")).convert_alpha()
        self.img_fondo = pygame.transform.scale(self.img_fondo, (self.WIDTH,self.HEIGHT)) 

        # Centro matemático exacto de la diana (390 + 250, 110 + 250)
        self.centro_x = 390 + (500 / 2) # 640
        self.centro_y = 110 + (500 / 2) # 360

        # Orden estándar de los números en una diana (empezando desde arriba a 90° en sentido horario)
        self.SECTORES = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

        # Barras de precisión
        self.barra_h = BarraPrecision(x=390, y=640, ancho=500, alto=30, orientacion="H", velocidad=7)
        self.barra_v = BarraPrecision(x=1150, y=110, ancho=30, alto=500, orientacion="V", velocidad=7)
        
        self.dardo_x = None
        self.dardo_y = None
        
        # --- 2. CREAMOS EL DARDO EN SU POSICIÓN INICIAL FIJA ---
        self.dardo = Dardo(x_inicio=640, y_inicio=700)
        
        self.historial_dardos = [] # Tuplas: (x, y, es_jugador)
        
        # --- REGLA 251 PUNTOS ---
        self.PUNTAJE_INICIAL = 251
        self.puntos_jugador = self.PUNTAJE_INICIAL
        self.puntos_ia = self.PUNTAJE_INICIAL
        
        self.ultimo_descuento = 0
        self.texto_evaluacion = ""
        
        self.dardos_jugador = 3
        self.dardos_ia = 3
        
        self.turno_actual = 'JUGADOR' # 'JUGADOR' o 'IA'
        
        self.tiempo_ia = 0
        self.objetivo_ia_x = 0
        self.objetivo_ia_y = 0

        # Fuentes
        pygame.font.init()
        self.fuente_ui = pygame.font.SysFont("Arial", 20, bold=True)
        self.fuente_grande = pygame.font.SysFont("Arial", 30, bold=True)
        
        # Estados: 'BARRA_H' -> 'BARRA_V' -> 'LANZAMIENTO' -> 'RESULTADO' -> 'GAME_OVER'
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
        # La IA apunta al sector del 20 con un margen de error aleatorio
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
            
            # --- 3. EL JUGADOR DISPARA: DISPARAMOS EL LANZAMIENTO ANIMADO ---
            self.dardo.iniciar_vuelo(self.dardo_x, self.dardo_y)
            self.estado_actual = 'LANZAMIENTO'

    def calcular_puntuacion_exacta(self, x, y):
        dx = x - self.centro_x
        dy = y - self.centro_y
        distancia = math.sqrt(dx**2 + dy**2)

        # 1. Fuera de la diana (Radio > 210px)
        if distancia > 210:
            self.texto_evaluacion = "¡FUERA DE TABLERO! (0 Pts)"
            return 0

        # 2. Centro Perfecto (Double Bull: 50 Pts)
        if distancia <= 10:
            self.texto_evaluacion = "¡BULLSEYE DOBLE! (-50 Pts)"
            return 50

        # 3. Anillo Verde (Single Bull: 25 Pts)
        if distancia <= 25:
            self.texto_evaluacion = "¡BULLSEYE SENCILLO! (-25 Pts)"
            return 25

        # 4. Cálculo del ángulo trigonométrico
        angulo_rad = math.atan2(-dy, dx)
        angulo_deg = math.degrees(angulo_rad)
        
        # Convertir ángulo trigonométrico a reloj
        angulo_reloj = (90 - angulo_deg) % 360
        
        # Cada sector cubre 18 grados
        indice_sector = int(((angulo_reloj + 9) % 360) / 18)
        numero_base = self.SECTORES[indice_sector]

        # 5. Determinación de multiplicadores por radio
        if 110 <= distancia <= 130:
            multiplicador = 3
            tipo = f"TRIPLE {numero_base}"
        elif 190 <= distancia <= 210:
            multiplicador = 2
            tipo = f"DOBLE {numero_base}"
        else:
            multiplicador = 1
            tipo = f"SENCILLO {numero_base}"

        puntos_obtenidos = numero_base * multiplicador
        self.texto_evaluacion = f"¡{tipo}! (-{puntos_obtenidos} Pts)"
        return puntos_obtenidos

    def procesar_impacto(self):
        puntos_descuento = self.calcular_puntuacion_exacta(self.dardo_x, self.dardo_y)
        self.ultimo_descuento = puntos_descuento

        if self.turno_actual == 'JUGADOR':
            if self.puntos_jugador - puntos_descuento >= 0:
                self.puntos_jugador -= puntos_descuento
            else:
                self.texto_evaluacion = "¡SE PASÓ DE 0! (Anulado)"

            self.dardos_jugador -= 1
            self.historial_dardos.append((self.dardo_x, self.dardo_y, True))
        else:
            if self.puntos_ia - puntos_descuento >= 0:
                self.puntos_ia -= puntos_descuento
            else:
                self.texto_evaluacion = "¡MÁQUINA SE PASÓ! (Anulado)"

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
                
        # --- 7. NUEVO ESTADO COMPARTIDO: ACTUALIZA EL VUELO DEL DARDO ---
        if self.estado_actual == 'LANZAMIENTO':
            finalizo_vuelo = self.dardo.actualizar()
            if finalizo_vuelo:
                # Al impactar la diana, procesamos los descuentos y las reglas del juego
                self.procesar_impacto()

    def dibujar_interface(self):
        rect_ui = pygame.Rect(30, 110, 320, 500)
        pygame.draw.rect(self.screen, (20, 20, 30), rect_ui, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 150), rect_ui, width=2, border_radius=10)
        
        str_turno = "TURNO: JUGADOR" if self.turno_actual == 'JUGADOR' else "TURNO: MÁQUINA"
        col_turno = (0, 255, 255) if self.turno_actual == 'JUGADOR' else (255, 150, 0)
        txt_turno = self.fuente_grande.render(str_turno, True, col_turno)

        txt_j1 = self.fuente_ui.render(f"JUGADOR: {self.puntos_jugador} Pts", True, (0, 255, 150))
        txt_d_j1 = self.fuente_ui.render(f"Dardos restantes: {self.dardos_jugador}", True, (180, 180, 180))
        
        txt_ia = self.fuente_ui.render(f"MÁQUINA: {self.puntos_ia} Pts", True, (255, 100, 100))
        txt_d_ia = self.fuente_ui.render(f"Dardos restantes: {self.dardos_ia}", True, (180, 180, 180))

        self.screen.blit(txt_turno, (45, 130))
        self.screen.blit(txt_j1, (45, 180))
        self.screen.blit(txt_d_j1, (45, 210))
        
        self.screen.blit(txt_ia, (45, 260))
        self.screen.blit(txt_d_ia, (45, 290))
        
        if self.estado_actual == 'RESULTADO' and self.texto_evaluacion:
            txt_eval = self.fuente_ui.render(self.texto_evaluacion, True, (255, 220, 0))
            self.screen.blit(txt_eval, (45, 350))
            
            txt_cont = self.fuente_ui.render("ESPACIO para continuar...", True, (150, 150, 150))
            self.screen.blit(txt_cont, (45, 410))

        if self.estado_actual == 'GAME_OVER':
            if self.puntos_jugador < self.puntos_ia:
                res_txt = "¡HAS GANADO!"
                col_res = (0, 255, 100)
            elif self.puntos_ia < self.puntos_jugador:
                res_txt = "¡MÁQUINA GANA!"
                col_res = (255, 50, 50)
            else:
                res_txt = "¡EMPATE TÉCNICO!"
                col_res = (255, 255, 0)
                
            txt_go = self.fuente_grande.render(res_txt, True, col_res)
            txt_reiniciar = self.fuente_ui.render("ESPACIO para reiniciar", True, (255, 255, 255))
            self.screen.blit(txt_go, (45, 380))
            self.screen.blit(txt_reiniciar, (45, 430))

    def dibujar(self):
        self.screen.blit(self.img_fondo, (0,0)) 
        
        # Tablero
        self.screen.blit(self.img_diana, (390, 110))

        # Barras
        self.barra_h.dibujar(self.screen)
        self.barra_v.dibujar(self.screen)
        
        # Historial de dardos (Azul = Jugador, Rojo = IA)
        for px, py, es_jugador in self.historial_dardos:
            color_dardo = (0, 150, 255) if es_jugador else (255, 50, 50)
            pygame.draw.circle(self.screen, color_dardo, (int(px), int(py)), 10)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(px), int(py)), 3)

        # --- 8. DIBUJAR LA ANIMACIÓN PARABÓLICA DEL DARDO ---
        if self.estado_actual in ['LANZAMIENTO', 'RESULTADO']:
            self.dardo.dibujar(self.screen)

        # Brillo especial indicador en el estado estático de RESULTADO
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
