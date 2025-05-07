import pygame
from obstacles import obstacles_laboratoire, passage_rect
from interface_capture import interface_capture
from music import MusicManager
from joueur import *

def afficher_scene_laboratoire(screen, scenes, player, dimensions_perso):
    screen.blit(scenes["laboratoire"]["fond"], (0, 0))

    deplacer_joueur(obstacles_laboratoire, player, dimensions_perso)

    if passage_rect[9].colliderect(pygame.Rect(player["x"], player["y"], dimensions_perso, dimensions_perso)):
        player["x"], player["y"] = 670, 430
        return "jeu"

    if player["image"]:
        screen.blit(player["image"], (player["x"], player["y"]))

    return "laboratoire"
