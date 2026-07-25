import sys
import pygame
from src.juego import JuegoDardos

def main():
    pygame.init()
    pygame.mixer.init() 
    
    # Resolución base exigida por el launcher
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Juego de Dardos")
    
    juego = JuegoDardos(screen)
    juego.ejecutar()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
