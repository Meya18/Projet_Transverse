import pygame
import time

# Initialisation du mixer
pygame.mixer.init()

# Chemins vers les fichiers audio (remplace-les par tes vrais fichiers)
MUSIQUE_INTRO = "musique_intro.mp3"
MUSIQUE_COMBAT = "musique_combat.mp3"
MUSIQUE_CAPTURE = "musique_capture.mp3"

def jouer_musique(fichier, loop=True):
    pygame.mixer.music.load(fichier)
    pygame.mixer.music.play(-1 if loop else 0)

def arreter_musique():
    pygame.mixer.music.stop()

# Démo d'utilisation
if __name__ == "__main__":
    print("Musique d'intro...")
    jouer_musique(MUSIQUE_INTRO)
    time.sleep(5)  # On laisse jouer 5 secondes

    print("Combat !")
    jouer_musique(MUSIQUE_COMBAT)
    time.sleep(5)

    print("Capture d’un Pokémon !")
    jouer_musique(MUSIQUE_CAPTURE, loop=False)
    time.sleep(5)

    print("Fin")
    arreter_musique()


#utilisation dans le jeu
from musique_manager import jouer_musique, arreter_musique

# Quand le jeu commence
jouer_musique("musique_intro.mp3")

# Quand un combat commence
jouer_musique("musique_combat.mp3")

# Quand un Pokémon est capturé
jouer_musique("musique_capture.mp3", loop=False)


