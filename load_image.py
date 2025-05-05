import pygame

def load_and_scale(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

# Chargement des images de fond
background = load_and_scale("images/fond1.png", (1000, 600))
fond2_image = load_and_scale("images/fond2.png", (1000, 600))
debut_image = load_and_scale("images/debut.jpeg", (1000, 600))
choix_perso_image = load_and_scale("images/choix_perso.jpg", (1000, 600))
maison1 = load_and_scale("images/maison1.jpg", (1000, 600))
maison2 = load_and_scale("images/maison2.png", (1000, 600))
etage = load_and_scale("images/etage.png", (1000, 600))
laboratoire = load_and_scale("images/laboratoire.png", (1000, 600))