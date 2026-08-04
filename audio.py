from pathlib import Path
import pygame

class GestorAudio:
    def __init__(self):
        pygame.mixer.init()
        
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.AUDIO_DIR = self.BASE_DIR / "assets" / "audio"
        
        # Volúmenes iniciales (de 0.0 a 1.0)
        self.volumen_musica = 0.5
        self.volumen_sfx = 0.7
        
        # Diccionario para almacenar efectos de sonido cortos
        self.sonidos = {}

    def cargar_musica_fondo(self, nombre_archivo):
        """Carga y reproduce música de fondo en bucle."""
        ruta = str(self.AUDIO_DIR / nombre_archivo)
        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(self.volumen_musica)
            pygame.mixer.music.play(-1) # -1 significa bucle infinito
        except pygame.error:
            print(f"Advertencia: No se pudo cargar la música en {ruta}")

    def cargar_efecto(self, clave, nombre_archivo):
        """Carga un efecto de sonido corto."""
        ruta = str(self.AUDIO_DIR / nombre_archivo)
        try:
            sound = pygame.mixer.Sound(ruta)
            sound.set_volume(self.volumen_sfx)
            self.sonidos[clave] = sound
        except pygame.error:
            print(f"Advertencia: No se pudo cargar el sonido {nombre_archivo}")

    def reproducir_efecto(self, clave):
        """Reproduce un efecto si existe en la memoria."""
        if clave in self.sonidos:
            self.sonidos[clave].play()

    def cambiar_volumen_musica(self, nuevo_volumen):
        """Ajusta el volumen de la música (0.0 a 1.0)."""
        self.volumen_musica = max(0.0, min(1.0, nuevo_volumen))
        pygame.mixer.music.set_volume(self.volumen_musica)

    def cambiar_volumen_sfx(self, nuevo_volumen):
        """Ajusta el volumen de los efectos de sonido (0.0 a 1.0)."""
        self.volumen_sfx = max(0.0, min(1.0, nuevo_volumen))
        for sonido in self.sonidos.values():
            sonido.set_volume(self.volumen_sfx)
