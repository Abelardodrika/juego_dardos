from pathlib import Path
import pygame

class GestorAudio:
    def __init__(self):
        pygame.mixer.init()
        
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.AUDIO_DIR = self.BASE_DIR / "assets" / "sounds"
        
        self.volumen_musica = 0.5
        self.volumen_sfx = 0.7
        
        self.sonidos = {}

    def cargar_musica_fondo(self, nombre_archivo):
        ruta = str(self.AUDIO_DIR / nombre_archivo)
        try:
            pygame.mixer.music.stop()  
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(self.volumen_musica)
            pygame.mixer.music.play(-1) 
        except pygame.error:
            print(f"Advertencia: No se pudo cargar la música en {ruta}")

    def detener_musica(self):
        pygame.mixer.music.stop()

    def pausar_musica(self):
        pygame.mixer.music.pause()

    def despausar_musica(self):
        pygame.mixer.music.unpause()

    def cargar_efecto(self, clave, nombre_archivo):
        ruta = str(self.AUDIO_DIR / nombre_archivo)
        try:
            sound = pygame.mixer.Sound(ruta)
            sound.set_volume(self.volumen_sfx)
            self.sonidos[clave] = sound
        except pygame.error:
            print(f"Advertencia: No se pudo cargar el sonido {nombre_archivo}")

    def reproducir_efecto(self, clave):
        if clave in self.sonidos:
            self.sonidos[clave].play()

    def cambiar_volumen_musica(self, nuevo_volumen):
        self.volumen_musica = max(0.0, min(1.0, nuevo_volumen))
        pygame.mixer.music.set_volume(self.volumen_musica)

    def cambiar_volumen_sfx(self, nuevo_volumen):
        self.volumen_sfx = max(0.0, min(1.0, nuevo_volumen))
        for sonido in self.sonidos.values():
            sonido.set_volume(self.volumen_sfx)
