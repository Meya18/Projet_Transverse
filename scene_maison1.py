import pygame
from obstacles import obstacles_maison1, passage_rect
from joueur import deplacer_joueur

def afficher_scene_maison1(screen, fond, player, dimensions_perso):
    screen.blit(fond, (0, 0))

    deplacer_joueur(obstacles_maison1, player, dimensions_perso)

    if player["image"]:
        screen.blit(player["image"], (player["x"], player["y"]))

    if passage_rect[4].colliderect(pygame.Rect(player["x"], player["y"], dimensions_perso, dimensions_perso)):
        player["x"], player["y"] = 260, 245
        return "jeu"

    return "maison1"
