import pygame
from joueur import deplacer_joueur
from obstacles import obstacles_maison2, passage_rect

def afficher_scene_maison2(screen, scenes, player):
    screen.blit(scenes["maison2"]["fond"], (0, 0))

    deplacer_joueur(obstacles_maison2, player)

    if passage_rect[8].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
        player["x"], player["y"] = 280, 230
        return "etage"

    if passage_rect[5].colliderect(pygame.Rect(player["x"], player["y"], 30, 30)):
        player["x"], player["y"] = 635, 245
        return "jeu"

    if player["image"]:
        screen.blit(player["image"], (player["x"], player["y"]))

    return "maison2"
