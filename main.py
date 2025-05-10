#import
import pygame
from interface_capture import *
from interface_capture import inventory, INVENTORY_SLOTS, SLOT_SIZE, SLOT_MARGIN, WIDTH, HEIGHT
from music import MusicManager
from obstacles import *
from load_image import *
from joueur import *
from scene_debut import *
from scene_choix_perso import *
from scene_maison1 import *
from scene_maison2 import *
from scene_laboratoire import *


pygame.init()

# État initial
game_start_ticks = pygame.time.get_ticks()
game_won = False
show_inventory = False
victory_time_ms = 0
etat_jeu = "debut"
musique_accueil_jouee = False

# Définition de la fenêtre
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Jeu Team Rocket")

# fonction pour dessiner l’inventaire sur toutes les scènes
def draw_inventory(surface):
    total_w = INVENTORY_SLOTS * SLOT_SIZE + (INVENTORY_SLOTS - 1) * SLOT_MARGIN
    start_x = SLOT_MARGIN
    y = HEIGHT - SLOT_SIZE - SLOT_MARGIN
    for i in range(INVENTORY_SLOTS):
        x = start_x + i * (SLOT_SIZE + SLOT_MARGIN)
        pygame.draw.rect(surface, (200, 200, 200), (x, y, SLOT_SIZE, SLOT_SIZE), 2)
        if i < len(inventory):
            img = pygame.transform.scale(inventory[i], (SLOT_SIZE - 4, SLOT_SIZE - 4))
            surface.blit(img, (x + 2, y + 2))
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
dimensions_perso = 50
for key in joueur_images:
    joueur_images[key] = pygame.transform.scale(joueur_images[key], (dimensions_perso, dimensions_perso))

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
vitesse_texte = 10

# Rectangle de la boîte de dialogue
dialogue_rect = pygame.Rect(50, 450, 900, 130)

def afficher_dialogue(screen, font, phrase, texte_actuel, dialogue_rect):
    pygame.draw.rect(screen, (255, 255, 255), dialogue_rect)
    pygame.draw.rect(screen, (0, 0, 0), dialogue_rect, 3)

    texte_surface = font.render(texte_actuel, True, (0, 0, 0))
    screen.blit(texte_surface, (dialogue_rect.x + 20, dialogue_rect.y + 20))

def get_resized_player_image(player_image, size):
    return pygame.transform.scale(player_image, (size, size))

# Scènes
scenes = {
    "debut": {"fond": debut_image, "bouton": bouton_debut},
    "choix_perso": {"fond": choix_perso_image, "persos": persos},
    "jeu": {"fond": background, "joueur": None, "obstacles": obstacles},
    "fond2": {"fond": fond2_image, "obstacles": obstacles_fond2},
    "maison1": {"fond": maison1, "persos": persos},
    "maison2": {"fond": maison2, "persos": persos},
    "etage": {"fond": etage, "persos": persos},
    "laboratoire": {"fond": laboratoire, "persos": persos},
    "fond_victoire": {"fond": fond_victoire, "persos": persos},
}

current_scene = "debut"
player = {"x": 385, "y": 370, "speed": 4, "image": None}

# Boucle du jeu
running = True
clock = pygame.time.Clock()
capture_cooldown = False
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
                        player["capture_image"] = persos[perso]
                        scenes["jeu"]["joueur"] = player
                        current_scene = "etage"
    # écran de victoire si l'inventaire est plein
    if len(inventory) >= INVENTORY_SLOTS:
        if not game_won:
            victory_time_ms = pygame.time.get_ticks() - game_start_ticks
            game_won = True
        # calcul du temps gelé
        total_s = victory_time_ms // 1000
        minutes = total_s // 60
        seconds = total_s % 60
        # fond victoire
        screen.blit(scenes["fond_victoire"]["fond"], (0, 0))
        music_manager.set_etat("fin")
        # dessiner l’inventaire centré
        total_w = INVENTORY_SLOTS * SLOT_SIZE + (INVENTORY_SLOTS - 1) * SLOT_MARGIN
        start_x = (WIDTH - total_w) // 2
        y_inv = (HEIGHT - SLOT_SIZE) // 2 + 100
        for i in range(INVENTORY_SLOTS):
            x = start_x + i * (SLOT_SIZE + SLOT_MARGIN)
            # tracer chaque case
            pygame.draw.rect(screen, (0, 0, 0), (x, y_inv, SLOT_SIZE, SLOT_SIZE), 2)
            # si un item capturé correspond, l’afficher
            if i < len(inventory):
                img = pygame.transform.scale(inventory[i], (SLOT_SIZE - 4, SLOT_SIZE - 4))
                screen.blit(img, (x + 2, y_inv + 2))
        # afficher le temps gelé au-dessus
        timer_text = f"Temps de jeu : {minutes}m{seconds}s"
        timer_surf = font_nom.render(timer_text, True, (0, 0, 0))
        timer_rect = timer_surf.get_rect(center=(WIDTH // 2, y_inv - 30))
        screen.blit(timer_surf, timer_rect)
        pygame.display.flip()
        continue
    screen.blit(scenes["fond_victoire"]["fond"], (0, 0))


    if current_scene == "debut":
        bouton_scale = afficher_scene_debut(screen, scenes, button_rect, bouton_debut, bouton_scale)

    elif current_scene == "choix_perso":
        afficher_scene_choix_perso(screen, scenes, persos, perso_positions, perso_sizes, perso_scale, font_nom)

    elif current_scene == "jeu":
        dimensions_perso = 30
        music_manager.set_etat("jeu")
        deplacer_joueur(obstacles, player, dimensions_perso)

        screen.blit(scenes["jeu"]["fond"], (0, 0))

        if passage_rect[0].colliderect(pygame.Rect(player["x"], player["y"], dimensions_perso, dimensions_perso)):
            player["x"], player["y"] = 400, 560
            current_scene = "fond2"

        if passage_rect[1].colliderect(pygame.Rect(player["x"], player["y"], dimensions_perso, dimensions_perso)):
            player["x"], player["y"] = 290, 510
            current_scene = "maison1"

        if passage_rect[2].colliderect(pygame.Rect(player["x"], player["y"], dimensions_perso, dimensions_perso)):
            player["x"], player["y"] = 400, 540
            current_scene = "maison2"

        if passage_rect[3].colliderect(pygame.Rect(player["x"], player["y"], dimensions_perso, dimensions_perso)):
            player["x"], player["y"] = 440, 530
            current_scene = "laboratoire"

        if player["image"]:
            resized_image = get_resized_player_image(player["image"], dimensions_perso)
            screen.blit(resized_image, (player["x"], player["y"]))

    elif current_scene == "laboratoire":
        dimensions_perso = 50
        current_scene = afficher_scene_laboratoire(screen, scenes, player, dimensions_perso)

    elif current_scene == "maison1":
        dimensions_perso = 50
        current_scene = afficher_scene_maison1(screen, scenes["maison1"]["fond"], player, dimensions_perso)

    elif current_scene == "maison2":
        dimensions_perso = 50
        current_scene = afficher_scene_maison2(screen, scenes["maison2"]["fond"], player, dimensions_perso)

    elif current_scene == "etage":
        screen.blit(scenes["etage"]["fond"], (0, 0))
        dimensions_perso = 50
        if not affichage_texte:
            deplacer_joueur(obstacles_etage, player, dimensions_perso)

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
                        show_inventory = True
                    else:
                        texte_actuel = ""
                        caractere_index = 0


        if passage_rect[6].colliderect(pygame.Rect(player["x"], player["y"], dimensions_perso, dimensions_perso)):
            player["x"], player["y"] = 780,150
            current_scene = "maison2"

        if player["image"]:
            resized_image = get_resized_player_image(player["image"], dimensions_perso)
            screen.blit(resized_image, (player["x"], player["y"]))

    elif current_scene == "fond2":
        dimensions_perso = 30
        deplacer_joueur(obstacles_fond2, player, dimensions_perso)
        screen.blit(scenes["fond2"]["fond"], (0, 0))

        player_rect = pygame.Rect(player["x"], player["y"], dimensions_perso, dimensions_perso)

        if passage_rect[7].colliderect(player_rect):
            player["x"], player["y"] = 530, 30
            current_scene = "jeu"

        # ne lancer le mini-jeu qu’une seule fois à l’entrée
        colliding = (0 <= player["x"] <= 970 and 0 <= player["y"] <= 570 and any(player_rect.colliderect(obs) for obs in capture_fond2))
        if colliding and not capture_cooldown:
            interface_capture(screen, player["capture_image"])
            capture_cooldown = True
        elif not colliding:
            capture_cooldown = False
        if player["image"]:
            resized_image = get_resized_player_image(player["image"], dimensions_perso)
            screen.blit(resized_image, (player["x"], player["y"]))
    if show_inventory and len(inventory) < INVENTORY_SLOTS:
        draw_inventory(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

