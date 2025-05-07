import pygame

def deplacer_joueur(obstacles, player, dimensions_perso):
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
    new_rect = pygame.Rect(new_x, new_y, dimensions_perso, dimensions_perso)

    if 0 <= new_x <= 970 and 0 <= new_y <= 570 and not any(new_rect.colliderect(obs) for obs in obstacles):
        player["x"], player["y"] = new_x, new_y