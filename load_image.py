import pygame

def load_and_scale(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

# Chargement des images de fond
background = load_and_scale("images/fond1.png", (1000, 600))
fond2_image = load_and_scale("images/fond2.png", (1000, 600))
debut_image = load_and_scale("images/debut.png", (1000, 600))
choix_perso_image = load_and_scale("images/choix_perso.png", (1000, 600))
maison1 = load_and_scale("images/maison1.jpg", (1000, 600))
maison2 = load_and_scale("images/maison2.png", (1000, 600))
etage = load_and_scale("images/etage.png", (1000, 600))
laboratoire = load_and_scale("images/laboratoire.png", (1000, 600))
fond_capture = load_and_scale("images/fond_combat.jpg", (1000, 600))
fond_victoire = load_and_scale("images/fond_victoire.png", (1000, 600))

#bouton du début
bouton_debut = pygame.image.load("images/bouton_debut.png")

#chargements des images personnages
james_p = pygame.image.load("images/james_p.png")
james_f = pygame.image.load("images/james_f.png")
jessie_p = pygame.image.load("images/jessie_p.png")
jessie_f = pygame.image.load("images/jessie_f.png")
chouette_p = pygame.image.load("images/chouette_p.png")
chouette_f = pygame.image.load("images/chouette_f.png")

#chargements des images de pokémons
carapuce = pygame.image.load("images/carapuce.png")
darkrai = pygame.image.load("images/darkrai.webp")
dracaufeu = pygame.image.load("images/dracaufeu.png")
dracolosse = pygame.image.load("images/dracolosse.png")
evoli = pygame.image.load("images/evoli.png")
herbizarre = pygame.image.load("images/herbizarre.jpg")
lucario = pygame.image.load("images/lucario.png")
metalosse = pygame.image.load("images/metalosse.webp")
mew = pygame.image.load("images/mew.webp")
nymphali = pygame.image.load("images/nymphali.png")
pikachu = pygame.image.load("images/pikachu.png")
carabaffe = pygame.image.load("images/carabaffe.png")



