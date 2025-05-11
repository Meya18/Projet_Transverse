import pygame

# Initialisation du mixer
pygame.mixer.init()

# Chemins des musiques
MUSIQUE_INTRO = "musique/musique_intro.mp3"
MUSIQUE_JEU = "musique/musique_jeu.mp3"
MUSIQUE_COMBAT = "musique/musique_combat.mp3"
MUSIQUE_FIN = "musique/musique_fin.mp3"

class MusicManager:
    def __init__(self):
        self.etat = None
        self.musique_actuelle = None

    def jouer_musique(self, fichier, loop=True):
        if self.musique_actuelle != fichier:
            pygame.mixer.music.load(fichier)
            pygame.mixer.music.play(-1 if loop else 0)
            self.musique_actuelle = fichier

    def arreter_musique(self):
        pygame.mixer.music.stop()
        self.musique_actuelle = None

    def set_etat(self, nouvel_etat):
        if nouvel_etat == self.etat:
            return  # Ne rien faire si pas de changement
        self.etat = nouvel_etat

        if nouvel_etat == "intro":
            self.jouer_musique(MUSIQUE_INTRO)

        elif nouvel_etat == "jeu":
            self.jouer_musique(MUSIQUE_JEU)

        elif nouvel_etat == "combat":
            self.jouer_musique(MUSIQUE_COMBAT)

        elif nouvel_etat == "fin":
            self.jouer_musique(MUSIQUE_FIN)

    def gerer_evenement(self, event):
        if event.type == pygame.USEREVENT and self.etat == "capture":
            self.set_etat("jeu")
