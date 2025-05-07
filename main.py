import pygame
from interface_capture import *
from music import MusicManager
from obstacles import *
from load_image import *
from joueur import *

pygame.init()

# État initial
etat_jeu = "debut"
musique_accueil_jouee = False

# Définition de la fenêtre
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Jeu Team Rocket")

music_manager = MusicManager()
music_manager.set_etat("intro")

# Police
font_nom = pygame.font.SysFont("Arial", 30)

# Bouton début
bouton_largeur, bouton_hauteur = 300, 150
bouton_debut = pygame.transform.scale(bouton_debut, (bouton_largeur, bouton_hauteur))
button_rect = bouton_debut.get_rect(center=(500, 500))
bouton_scale = 1.0

# Chargement des personnages pour la sélection
persos = {
    "james": james_p,
    "jessie": jessie_p,
    "chouette": chouette_p
}

# Images correspondant au personnage sélectionné
joueur_images = {
    "james": james_f,
    "jessie": jessie_f,
    "chouette": chouette_f
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

# Variables d'animation sélection
perso_scale = {"james": 1.0, "jessie": 1.0, "chouette": 1.0}
player_image = None

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
            texte_nom = font_nom.render(nom, True, (255,255,255))
            screen.blit(texte_nom, (pos[0] - texte_nom.get_width() // 2, pos[1] + perso_sizes[perso]["height"] // 2))

    elif current_scene == "jeu":
        music_manager.set_etat("jeu")
        deplacer_joueur(obstacles, player)

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
        deplacer_joueur(obstacles_maison1, player)

        if passage_rect[4].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 260, 245
            current_scene = "jeu"

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    elif current_scene == "maison2":
        screen.blit(scenes["maison2"]["fond"], (0, 0))
        deplacer_joueur(obstacles_maison2, player)

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
            deplacer_joueur(obstacles_etage, player)

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

        deplacer_joueur(obstacles_laboratoire, player)

        if passage_rect[9].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
            player["x"], player["y"] = 670, 420
            current_scene = "jeu"

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    elif current_scene == "fond2":
        deplacer_joueur(obstacles_fond2, player)
        screen.blit(scenes["fond2"]["fond"], (0, 0))

        player_rect = pygame.Rect(player["x"], player["y"], 30, 30)

        if passage_rect[7].colliderect(player_rect):
            player["x"], player["y"] = 530, 30
            current_scene = "jeu"

        if 0 <= player["x"] <= 970 and 0 <= player["y"] <= 570 and any(
                player_rect.colliderect(obs) for obs in capture_fond2):
            music_manager.set_etat("combat")
            interface_capture(screen)

        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

