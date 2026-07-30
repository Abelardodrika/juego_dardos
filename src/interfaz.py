from pathlib import Path
import pygame

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        
        # Rutas del sistema para los assets del menú
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.BACKGROUNDS_DIR = self.BASE_DIR / "assets" / "backgrounds"
        
        # Cargar y escalar el fondo del menú (usando tu asset)
        self.img_fondo = pygame.image.load(str(self.BACKGROUNDS_DIR / "fondomenu.png")).convert()
        self.img_fondo = pygame.transform.scale(self.img_fondo, (self.WIDTH, self.HEIGHT))

        self.img_logo = pygame.image.load(str(self.BACKGROUNDS_DIR / "titulomenu.png")).convert_alpha()

        self.pos_logo_x = (self.WIDTH // 2) - (self.img_logo.get_width() // 2)
        self.pos_logo_y = 20 # Altura a la que aparecerá el título en el menú
        
        # Inicializar fuentes
        pygame.font.init()
        self.fuente_boton = pygame.font.SysFont("Arial", 30, bold=True)
        
        # Configuración del botón "JUGAR" (centrado en la pantalla)
        self.ancho_btn = 200
        self.alto_btn = 60
        self.rect_boton = pygame.Rect(
            (self.WIDTH // 2) - (self.ancho_btn // 2),
            (self.HEIGHT // 2) + 80,
            self.ancho_btn,
            self.alto_btn
        )
        
        # Colores del botón
        self.color_normal = (30, 144, 255)    # Azul brillante
        self.color_hover = (0, 255, 150)       # Verde menta al pasar el cursor
        self.color_actual = self.color_normal

    def procesar_eventos(self):
        """Devuelve True si el usuario hace clic en JUGAR para iniciar el juego"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Efecto Hover: Cambiar color si el cursor está sobre el botón
        if self.rect_boton.collidepoint(mouse_pos):
            self.color_actual = self.color_hover
        else:
            self.color_actual = self.color_normal

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect_boton.collidepoint(mouse_pos):
                    return True # Señal para cambiar de pantalla e iniciar el juego
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return True
        return False

    def dibujar(self):
        # 1. Dibujar el fondo
        self.screen.blit(self.img_fondo, (0, 0))
        
        # 2. Dibujar el título con una ligera sombra oscura detrás
        self.screen.blit(self.img_logo, (self.pos_logo_x, self.pos_logo_y))
        
        
        # 3. Dibujar la caja del botón
        pygame.draw.rect(self.screen, self.color_actual, self.rect_boton, border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect_boton, width=3, border_radius=12)
        
        # 4. Texto del botón
        txt_boton = self.fuente_boton.render("JUGAR", True, (20, 20, 30))
        pos_btn_x = self.rect_boton.x + (self.ancho_btn // 2) - (txt_boton.get_width() // 2)
        pos_btn_y = self.rect_boton.y + (self.alto_btn // 2) - (txt_boton.get_height() // 2)
        self.screen.blit(txt_boton, (pos_btn_x, pos_btn_y))
        
        pygame.display.flip()
