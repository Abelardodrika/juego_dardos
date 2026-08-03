from pathlib import Path
import pygame
import sys

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.BACKGROUNDS_DIR = self.BASE_DIR / "assets" / "backgrounds"
        self.FONTS_DIR = self.BASE_DIR / "assets" / "fonts" 
        
        self.img_fondo = pygame.image.load(str(self.BACKGROUNDS_DIR / "fondomenu.png")).convert()
        self.img_fondo = pygame.transform.scale(self.img_fondo, (self.WIDTH, self.HEIGHT))

        self.img_logo = pygame.image.load(str(self.BACKGROUNDS_DIR / "titulomenu.png")).convert_alpha()

        self.pos_logo_x = (self.WIDTH // 2) - (self.img_logo.get_width() // 2)
        self.pos_logo_y = 20
        
        pygame.font.init()
        ruta_fuente_arcade = str(self.FONTS_DIR / "PressStart2P-Regular.ttf")
        
        self.fuente_boton = pygame.font.Font(ruta_fuente_arcade, 18)
        
        self.ancho_btn = 200
        self.alto_btn = 60
        self.rect_boton = pygame.Rect(
            (self.WIDTH // 2) - (self.ancho_btn // 2),
            (self.HEIGHT // 2) + 80,
            self.ancho_btn,
            self.alto_btn
        )
        
        self.color_normal = (30, 144, 255)   
        self.color_hover = (0, 255, 150)       
        self.color_actual = self.color_normal

    def procesar_eventos(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.rect_boton.collidepoint(mouse_pos):
            self.color_actual = self.color_hover
        else:
            self.color_actual = self.color_normal

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect_boton.collidepoint(mouse_pos):
                    return True 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return True
        return False

    def dibujar(self):
        self.screen.blit(self.img_fondo, (0, 0))
        
        self.screen.blit(self.img_logo, (self.pos_logo_x, self.pos_logo_y))
        
        pygame.draw.rect(self.screen, self.color_actual, self.rect_boton, border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect_boton, width=3, border_radius=12)
        
        txt_boton = self.fuente_boton.render("JUGAR", True, (20, 20, 30))
        pos_btn_x = self.rect_boton.x + (self.ancho_btn // 2) - (txt_boton.get_width() // 2)
        pos_btn_y = self.rect_boton.y + (self.alto_btn // 2) - (txt_boton.get_height() // 2)
        self.screen.blit(txt_boton, (pos_btn_x, pos_btn_y))
        
        pygame.display.flip()
