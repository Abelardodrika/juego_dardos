import sys
import pygame
from src.interfaz import MenuPrincipal
from src.juego import JuegoDardos

def main():
  pygame.init()
  pygame.mixer.init()

  SCREEN_WIDTH = 1280
  SCREEN_HEIGHT = 720

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Juego de Dardos")

  menu = MenuPrincipal(screen)
  juego = JuegoDardos(screen)

  estado_pantalla = "MENU"

  clock = pygame.time.Clock()
  running = True

  while running:
    if estado_pantalla == "MENU":
      if menu.procesar_eventos():
        juego.musica_activa = menu.musica_activa
        if juego.musica_activa:
          juego.audio.cargar_musica_fondo("musica_juego.mp3")
        else:
           juego.audio.detener_musica()
        juego.reiniciar_juego_completo()
        juego.running = True
        estado_pantalla = "JUEGO"

      menu.dibujar()

    elif estado_pantalla == "JUEGO":
      juego.procesar_eventos()
      juego.actualizar()
      juego.dibujar()

      if not juego.running:
        estado_pantalla = "MENU"

        if menu.musica_activa:
            menu.audio.cargar_musica_fondo("musica_juego.mp3")
        else:
            menu.audio.detener_musica()        

    clock.tick(60)

  pygame.quit()
  sys.exit()


if __name__ == "__main__":
  main()
