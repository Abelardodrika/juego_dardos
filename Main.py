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
    
    estado_pantalla = 'MENU'
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        if estado_pantalla == 'MENU':
            if menu.procesar_eventos():
                estado_pantalla = 'JUEGO'
            menu.dibujar()
            
        elif estado_pantalla == 'JUEGO':
            juego.procesar_eventos()
            juego.actualizar()
            juego.dibujar()
            
            if not juego.running:
                running = False
                
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
