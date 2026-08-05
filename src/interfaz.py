from pathlib import Path
import sys
import pygame
from src.audio import GestorAudio
from src.componentes import Boton


class MenuPrincipal:

  def __init__(self, screen):
    self.screen = screen
    self.WIDTH = screen.get_width()
    self.HEIGHT = screen.get_height()

    self.BASE_DIR = Path(__file__).resolve().parent.parent
    self.BACKGROUNDS_DIR = self.BASE_DIR / "assets" / "backgrounds"

    self.img_fondo = pygame.image.load(
        str(self.BACKGROUNDS_DIR / "fondomenu.png")
    ).convert()
    self.img_fondo = pygame.transform.scale(
        self.img_fondo, (self.WIDTH, self.HEIGHT)
    )

    self.img_logo = pygame.image.load(
        str(self.BACKGROUNDS_DIR / "titulomenu.png")
    ).convert_alpha()
    self.pos_logo_x = (self.WIDTH // 2) - (self.img_logo.get_width() // 2)
    self.pos_logo_y = 20

    self.pos_x_btn = (self.WIDTH // 2) - 110
    self.pos_y_jugar = (self.HEIGHT // 2) + 40
    self.pos_y_musica = (self.HEIGHT // 2) + 115

    self.btn_jugar = Boton(
        x=self.pos_x_btn,
        y=self.pos_y_jugar,
        ancho=220,
        alto=55,
        texto="JUGAR",
        color_bg=(30, 144, 255),
    )

    self.musica_activa = True
    self.btn_musica = Boton(
        x=self.pos_x_btn,
        y=self.pos_y_musica,
        ancho=220,
        alto=55,
        texto="MUSICA: ON",
        color_bg=(30, 144, 255),
    )

    self.audio = GestorAudio()
    self.audio.cargar_musica_fondo("musica_juego.mp3")

    self.audio.cargar_efecto("click", "click.mp3")

  def procesar_eventos(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if self.btn_jugar.fue_clicado(event):
        self.audio.reproducir_efecto("click") 
        return True

      if self.btn_musica.fue_clicado(event):
        self.audio.reproducir_efecto("click") 
        self.musica_activa = not self.musica_activa

        if self.musica_activa:
          self.btn_musica = Boton(
              x=self.pos_x_btn,
              y=self.pos_y_musica,
              ancho=220,
              alto=55,
              texto="MUSICA: ON",
              color_bg=(30, 144, 255),
          )
          self.audio.cargar_musica_fondo("musica_juego.mp3")
        else:
          self.btn_musica = Boton(
              x=self.pos_x_btn,
              y=self.pos_y_musica,
              ancho=220,
              alto=55,
              texto="MUSICA: OFF",
              color_bg=(100, 100, 100),
          )
          self.audio.detener_musica()

      elif event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
          return True

    return False

  def dibujar(self):
    self.screen.blit(self.img_fondo, (0, 0))
    self.screen.blit(self.img_logo, (self.pos_logo_x, self.pos_logo_y))

    self.btn_jugar.dibujar(self.screen)
    self.btn_musica.dibujar(self.screen)

    pygame.display.flip()
