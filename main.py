import pygame
from interface_capture import *
from music import (
    jouer_musique_accueil, arreter_musique_accueil,
    jouer_musique_jeu, arreter_musique_jeu,
    jouer_musique_fin, arreter_musique_fin
)
pygame.init()

# État initial
etat_jeu = "debut"
musique_accueil_jouee = False

# Définition de la fenêtre
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Jeu Team Rocket")

# Chargement des images de fond
background = pygame.image.load("images/fond1.png")
background = pygame.transform.scale(background, (1000, 600))
fond2_image = pygame.image.load("images/fond2.png")
fond2_image = pygame.transform.scale(fond2_image, (1000, 600))
debut_image = pygame.image.load("images/debut.jpeg")
debut_image = pygame.transform.scale(debut_image, (1000, 600))
choix_perso_image = pygame.image.load("images/choix_perso.jpg")
choix_perso_image = pygame.transform.scale(choix_perso_image, (1000, 600))
maison1 = pygame.image.load("images/maison1.jpg")
maison1 = pygame.transform.scale(maison1, (1000, 600))
maison2 = pygame.image.load("images/maison2.png")
maison2 = pygame.transform.scale(maison2, (1000, 600))
etage = pygame.image.load("images/etage.png")
etage = pygame.transform.scale(etage, (1000, 600))
laboratoire = pygame.image.load("images/laboratoire.png")
laboratoire = pygame.transform.scale(laboratoire, (1000, 600))

# Chargement des personnages pour la sélection
persos = {
    "james": pygame.image.load("images/james_p.png"),
    "jessie": pygame.image.load("images/jessie_p.png"),
    "chouette": pygame.image.load("images/chouette_p.png")
}

# Images correspondant au personnage sélectionné
joueur_images = {
    "james": pygame.image.load("images/james_f.png"),
    "jessie": pygame.image.load("images/jessie_f.png"),
    "chouette": pygame.image.load("images/chouette_f.png")
}

# Taille des personnages
perso_sizes = {
    "james": {"width": 300, "height": 300},
    "jessie": {"width": 300, "height": 300},
    "chouette": {"width": 300, "height": 300}
}

# Redimensionnement
for key in persos:
    persos[key] = pygame.transform.scale(persos[key], (perso_sizes[key]["width"], perso_sizes[key]["height"]))
for key in joueur_images:
    joueur_images[key] = pygame.transform.scale(joueur_images[key], (30, 30))

# Positions personnages
perso_positions = {
    "james": (225, 275),
    "jessie": (775, 275),
    "chouette": (500, 275)
}

# Police
font_titre = pygame.font.SysFont("Arial", 40, bold=True)
font_nom = pygame.font.SysFont("Arial", 30)

# Bouton début
bouton_largeur, bouton_hauteur = 300, 150
bouton_debut = pygame.image.load("images/bouton_debut.png")
bouton_debut = pygame.transform.scale(bouton_debut, (bouton_largeur, bouton_hauteur))
button_rect = bouton_debut.get_rect(center=(500, 500))
bouton_scale = 1.0

# Variables d'animation sélection
perso_scale = {"james": 1.0, "jessie": 1.0, "chouette": 1.0}
player_image = None

# Obstacles fond1
obstacles = [
    pygame.Rect(545, 290, 285, 125),
    pygame.Rect(205, 105, 220, 135),
    pygame.Rect(170, 200, 35, 40),
    pygame.Rect(585, 100, 240, 140),
    pygame.Rect(550, 200, 35, 40),
    pygame.Rect(205, 325, 215, 30),
    pygame.Rect(210, 425, 35, 20),
    pygame.Rect(540, 480, 255, 30),
    pygame.Rect(290, 510, 170, 90),
    pygame.Rect(0, 0, 500, 60),
    pygame.Rect(585, 0, 415, 60),
    pygame.Rect(0, 0, 80, 600),
    pygame.Rect(920, 0, 80, 600),
    pygame.Rect(80, 575, 155, 25),
    pygame.Rect(765, 575, 155, 25)
]

# Obstacles fond2
obstacles_fond2 = [
    pygame.Rect(0, 0, 1000, 60),
    pygame.Rect(710, 60, 290, 155),
    pygame.Rect(940, 215, 60, 85),
    pygame.Rect(890, 215, 50, 30),
    pygame.Rect(365, 60, 225, 60),
    pygame.Rect(40, 60, 30, 30),
    pygame.Rect(0, 190, 10, 410),
    pygame.Rect(10, 425, 55, 175),
    pygame.Rect(65, 545, 175, 55),
    pygame.Rect(480, 545, 520, 55),
    pygame.Rect(715, 485, 285, 60),
    pygame.Rect(830, 425, 170, 60),
    pygame.Rect(945, 360, 55, 65),
    pygame.Rect(305, 205, 110, 190),
    pygame.Rect(415, 175, 65, 190),
    pygame.Rect(480, 235, 60, 190),
    pygame.Rect(540, 300, 50, 125),
    pygame.Rect(160, 390, 55, 65),
    pygame.Rect(220, 420, 50, 65),
    pygame.Rect(710, 275, 30, 30),
    pygame.Rect(10, 200, 60, 15),
    pygame.Rect(130, 200, 175, 15),
    pygame.Rect(544, 120, 20, 150)
]

#obstacles maison 1
obstacles_maison1 = [
    pygame.Rect(0, 0, 175, 600),
    pygame.Rect(825, 0, 175, 600),
    pygame.Rect(175, 0, 650, 90),
    pygame.Rect(175, 555, 95, 45),
    pygame.Rect(270, 580, 75, 20),
    pygame.Rect(345, 555, 480, 45),
    pygame.Rect(175, 230, 45, 90),
    pygame.Rect(175, 370, 45, 90),
    pygame.Rect(780, 230, 45, 90),
    pygame.Rect(780, 370, 45, 90),
    pygame.Rect(440, 290, 165, 75),
    pygame.Rect(475, 250, 90, 40),
    pygame.Rect(220, 90, 80, 50),
    pygame.Rect(390, 90, 85, 50),
    pygame.Rect(570, 90, 80, 50),
    pygame.Rect(700, 90, 125, 50),
]

#obstacles maison 2
obstacles_maison2 = [
    pygame.Rect(0, 0, 1000, 130),
    pygame.Rect(0, 130, 380, 25),
    pygame.Rect(465, 130, 130, 25),
    pygame.Rect(850, 130, 150, 90),
    pygame.Rect(395, 260, 285, 125),
    pygame.Rect(0, 405, 70, 110),
    pygame.Rect(930, 405, 70, 110),
    pygame.Rect(0, 585, 360, 15),
    pygame.Rect(490, 585, 510, 15)
]

#obstacles étage
obstacles_etage = [
    pygame.Rect(0, 0, 1000, 210),
    pygame.Rect(0, 210, 200, 390),
    pygame.Rect(800, 210, 200, 390),
    pygame.Rect(200, 570, 600, 30),
    pygame.Rect(465, 190, 130, 50),
    pygame.Rect(675, 210, 125, 20),
    pygame.Rect(740, 230, 60, 35),
    pygame.Rect(655, 325, 90, 100)
]

#obstacles laboratoire
obstacles_laboratoire = [
    pygame.Rect(0, 0, 25, 600),
    pygame.Rect(25, 0, 1000, 130),
    pygame.Rect(955, 130, 45, 470),
    pygame.Rect(25, 470, 345, 130),
    pygame.Rect(555, 470, 400, 130),
    pygame.Rect(25, 130, 415, 30),
    pygame.Rect(635, 130, 320, 30),
    pygame.Rect(25, 160, 65, 165),
    pygame.Rect(560, 260, 230, 80),
    pygame.Rect(110, 225, 135, 140)
]

#ouverture de l'interface de capture
capture_fond2 = [
    pygame.Rect(160, 460, 5, 5),
    pygame.Rect(190, 520, 5, 5),
    pygame.Rect(280, 575, 5, 5),
    pygame.Rect(100, 310, 5, 5),
    pygame.Rect(220, 215, 5, 5),
    pygame.Rect(15, 370, 5, 5),
    pygame.Rect(425, 370, 5, 5),
    pygame.Rect(365, 430, 5, 5),
    pygame.Rect(450, 460, 5, 5),
    pygame.Rect(680, 65, 5, 5),
    pygame.Rect(680, 155, 5, 5),
    pygame.Rect(595, 95, 5, 5),
    pygame.Rect(280, 70, 5, 5)
]

# Rectangle passage de scène
passage_rect = [
    pygame.Rect(500, 0, 90, 30), #fond2
    pygame.Rect(260,240,20,2), #maison 1
    pygame.Rect(635,240,20,2), #maison 2
    pygame.Rect(675,420,20,2), #laboratoire
    pygame.Rect(270,575,70,2), #maison1 -> jeu
    pygame.Rect(360,595,125,2), #maison2 -> jeu
    pygame.Rect(260,210,80,2), #etage -> maison2
    pygame.Rect(360,595,120,2), #fond2 -> jeu
    pygame.Rect(845,120,5,90), #maison2 -> etage
    pygame.Rect(370, 595, 190, 5)  #laboratoire -> jeu
]

# Phrases à afficher
phrases_etage = [
    "Bienvenue dans ce jeu Team Rocket !",
    "Ton objectif est de capturer des Pokémon sauvages.",
    "Rends toi dans les hautes herbes pour les trouver.",
    "Utilise les touches directionnelles pour te déplacer.",
    "Bonne chance !"
]

phrase_index = 0
affichage_texte = True
texte_actuel = ""
caractere_index = 0
last_update_time = pygame.time.get_ticks()
vitesse_texte = 30

# Rectangle de la boîte de dialogue
dialogue_rect = pygame.Rect(50, 450, 900, 130)

def afficher_dialogue(screen, font, phrase, texte_actuel, dialogue_rect):
    pygame.draw.rect(screen, (255, 255, 255), dialogue_rect)
    pygame.draw.rect(screen, (0, 0, 0), dialogue_rect, 3)

    texte_surface = font.render(texte_actuel, True, (0, 0, 0))
    screen.blit(texte_surface, (dialogue_rect.x + 20, dialogue_rect.y + 20))

# Scènes
scenes = {
    "debut": {"fond": debut_image, "bouton": bouton_debut},
    "choix_perso": {"fond": choix_perso_image, "persos": persos},
    "jeu": {"fond": background, "joueur": None, "obstacles": obstacles},
    "fond2": {"fond": fond2_image, "obstacles": obstacles_fond2},
    "maison1": {"fond": maison1, "persos": persos},
    "maison2": {"fond": maison2, "persos": persos},
    "etage": {"fond": etage, "persos": persos},
    "laboratoire": {"fond": laboratoire, "persos": persos}
}

current_scene = "debut"
player = {"x": 385, "y": 370, "speed": 4, "image": None}

# Boucle du jeu
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_scene == "debut" and button_rect.collidepoint(event.pos):
                current_scene = "choix_perso"
            elif current_scene == "choix_perso":
                for perso, pos in perso_positions.items():
                    rect = pygame.Rect(pos[0] - 50, pos[1] - 50, 100, 100)
                    if rect.collidepoint(event.pos):
                        player["image"] = joueur_images[perso]
                        scenes["jeu"]["joueur"] = player
                        current_scene = "etage"

    screen.fill((255,255,255))

    if current_scene == "debut":
        screen.blit(scenes["debut"]["fond"], (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_x, mouse_y):
            if bouton_scale > 0.9:
                bouton_scale -= 0.01
        else:
            if bouton_scale < 1.0:
                bouton_scale += 0.01
        scaled_bouton = pygame.transform.scale(bouton_debut, (int(bouton_largeur * bouton_scale), int(bouton_hauteur * bouton_scale)))
        scaled_rect = scaled_bouton.get_rect(center=button_rect.center)
        screen.blit(scaled_bouton, scaled_rect.topleft)

    elif current_scene == "choix_perso":
        screen.blit(scenes["choix_perso"]["fond"], (0, 0))
        titre = font_titre.render("Choisissez votre personnage", True, (255,255,255))
        screen.blit(titre, (500 - titre.get_width() // 2, 30))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for perso, pos in perso_positions.items():
            rect = pygame.Rect(pos[0] - 50, pos[1] - 50, 100, 100)
            if rect.collidepoint(mouse_x, mouse_y):
                if perso_scale[perso] > 0.9:
                    perso_scale[perso] -= 0.01
            else:
                if perso_scale[perso] < 1.0:
                    perso_scale[perso] += 0.01
            scaled_perso = pygame.transform.scale(persos[perso], (int(perso_sizes[perso]["width"] * perso_scale[perso]), int(perso_sizes[perso]["height"] * perso_scale[perso])))

            scaled_rect = scaled_perso.get_rect(center=pos)
            screen.blit(scaled_perso, scaled_rect.topleft)
            nom = {"jessie": "Jessie", "james": "James", "chouette": "Effraie"}[perso]
            texte_nom = font_nom.render(nom, True, (0,0,0))
            screen.blit(texte_nom, (pos[0] - texte_nom.get_width() // 2, pos[1] + perso_sizes[perso]["height"] // 2))

    elif current_scene == "jeu":
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # Direction unique
        if keys[pygame.K_LEFT]:
            dx = -player["speed"]
        elif keys[pygame.K_RIGHT]:
            dx = player["speed"]
        elif keys[pygame.K_UP]:
            dy = -player["speed"]
        elif keys[pygame.K_DOWN]:
            dy = player["speed"]

        new_x = player["x"] + dx
        new_y = player["y"] + dy
        new_rect = pygame.Rect(new_x, new_y, 30, 30)

        if 0 <= new_x <= 970 and 0 <= new_y <= 570 and not any(new_rect.colliderect(obs) for obs in obstacles):
            player["x"], player["y"] = new_x, new_y

        screen.blit(scenes["jeu"]["fond"], (0, 0))

        if passage_rect[0].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 400, 560
            current_scene = "fond2"

        if passage_rect[1].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 290, 530
            current_scene = "maison1"

        if passage_rect[2].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 400, 560
            current_scene = "maison2"

        if passage_rect[3].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 440, 550
            current_scene = "laboratoire"

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))


    elif current_scene == "maison1":
        screen.blit(scenes["maison1"]["fond"], (0, 0))
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -player["speed"]
        elif keys[pygame.K_RIGHT]:
            dx = player["speed"]
        elif keys[pygame.K_UP]:
            dy = -player["speed"]
        elif keys[pygame.K_DOWN]:
            dy = player["speed"]

        new_x = player["x"] + dx
        new_y = player["y"] + dy
        new_rect = pygame.Rect(new_x, new_y, 30, 30)
        screen.blit(scenes["maison1"]["fond"], (0, 0))

        if 0 <= new_x <= 970 and 0 <= new_y <= 570 and not any(new_rect.colliderect(obs) for obs in obstacles_maison1):
            player["x"], player["y"] = new_x, new_y

        if passage_rect[4].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 260, 245
            current_scene = "jeu"

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    elif current_scene == "maison2":
        screen.blit(scenes["maison2"]["fond"], (0, 0))
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -player["speed"]
        elif keys[pygame.K_RIGHT]:
            dx = player["speed"]
        elif keys[pygame.K_UP]:
            dy = -player["speed"]
        elif keys[pygame.K_DOWN]:
            dy = player["speed"]

        new_x = player["x"] + dx
        new_y = player["y"] + dy
        new_rect = pygame.Rect(new_x, new_y, 30, 30)
        screen.blit(scenes["maison2"]["fond"], (0, 0))

        if 0 <= new_x <= 970 and 0 <= new_y <= 570 and not any(new_rect.colliderect(obs) for obs in obstacles_maison2):
            player["x"], player["y"] = new_x, new_y

        if passage_rect[8].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 280, 230
            current_scene = "etage"

        if passage_rect[5].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 635,245
            current_scene = "jeu"

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    elif current_scene == "etage":
        screen.blit(scenes["etage"]["fond"], (0, 0))

        if not affichage_texte:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0

            if keys[pygame.K_LEFT]:
                dx = -player["speed"]
            elif keys[pygame.K_RIGHT]:
                dx = player["speed"]
            elif keys[pygame.K_UP]:
                dy = -player["speed"]
            elif keys[pygame.K_DOWN]:
                dy = player["speed"]

            new_x = player["x"] + dx
            new_y = player["y"] + dy
            new_rect = pygame.Rect(new_x, new_y, 30, 30)

            if 0 <= new_x <= 970 and 0 <= new_y <= 570 and not any(
                    new_rect.colliderect(obs) for obs in obstacles_etage):
                player["x"], player["y"] = new_x, new_y

        if affichage_texte:
            now = pygame.time.get_ticks()
            if now - last_update_time > vitesse_texte:
                if caractere_index < len(phrases_etage[phrase_index]):
                    texte_actuel += phrases_etage[phrase_index][caractere_index]
                    caractere_index += 1
                    last_update_time = now

            afficher_dialogue(screen, font_nom, phrases_etage[phrase_index], texte_actuel, dialogue_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if affichage_texte and dialogue_rect.collidepoint(event.pos):
                if caractere_index >= len(phrases_etage[phrase_index]):
                    phrase_index += 1
                    if phrase_index >= len(phrases_etage):
                        affichage_texte = False
                    else:
                        texte_actuel = ""
                        caractere_index = 0


        if passage_rect[6].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 800,150
            current_scene = "maison2"

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    elif current_scene == "laboratoire":
        screen.blit(scenes["laboratoire"]["fond"], (0, 0))

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -player["speed"]
        elif keys[pygame.K_RIGHT]:
            dx = player["speed"]
        elif keys[pygame.K_UP]:
            dy = -player["speed"]
        elif keys[pygame.K_DOWN]:
            dy = player["speed"]

        new_x = player["x"] + dx
        new_y = player["y"] + dy
        new_rect = pygame.Rect(new_x, new_y, 30, 30)
        screen.blit(scenes["laboratoire"]["fond"], (0, 0))

        if 0 <= new_x <= 970 and 0 <= new_y <= 570 and not any(new_rect.colliderect(obs) for obs in obstacles_laboratoire):
            player["x"], player["y"] = new_x, new_y

        if passage_rect[9].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 670, 420
            current_scene = "jeu"

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    elif current_scene == "fond2":
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -player["speed"]
        elif keys[pygame.K_RIGHT]:
            dx = player["speed"]
        elif keys[pygame.K_UP]:
            dy = -player["speed"]
        elif keys[pygame.K_DOWN]:
            dy = player["speed"]


        new_x = player["x"] + dx
        new_y = player["y"] + dy
        new_rect = pygame.Rect(new_x, new_y, 30, 30)

        if 0 <= new_x <= 970 and 0 <= new_y <= 570 and not any(new_rect.colliderect(obs) for obs in obstacles_fond2):
            player["x"], player["y"] = new_x, new_y

        screen.blit(scenes["fond2"]["fond"], (0, 0))

        if passage_rect[7].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 530, 30
            current_scene = "jeu"

        if 0 <= new_x <= 970 and 0 <= new_y <= 570 and any(new_rect.colliderect(obs) for obs in capture_fond2):
            interface_capture(screen)

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

