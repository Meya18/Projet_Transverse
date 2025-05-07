import pygame
from load_image import *

def afficher_scene_choix_perso(screen, scenes, persos, perso_positions, perso_sizes, perso_scale, font_nom):
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

        scaled_perso = pygame.transform.scale(
            persos[perso],
            (int(perso_sizes[perso]["width"] * perso_scale[perso]), int(perso_sizes[perso]["height"] * perso_scale[perso]))
        )
        scaled_rect = scaled_perso.get_rect(center=pos)
        screen.blit(scaled_perso, scaled_rect.topleft)

        nom = {"jessie": "Jessie", "james": "James", "chouette": "Effraie"}[perso]
        texte_nom = font_nom.render(nom, True, (255, 255, 255))
        screen.blit(texte_nom, (pos[0] - texte_nom.get_width() // 2, pos[1] + perso_sizes[perso]["height"] // 2))
