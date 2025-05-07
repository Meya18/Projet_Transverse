import pygame

def afficher_scene_debut(screen, scenes, button_rect, bouton_debut, bouton_scale):
    screen.blit(scenes["debut"]["fond"], (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_x, mouse_y):
        if bouton_scale > 0.9:
            bouton_scale -= 0.01
    else:
        if bouton_scale < 1.0:
            bouton_scale += 0.01
    scaled_bouton = pygame.transform.scale(bouton_debut, (int(300 * bouton_scale), int(150 * bouton_scale)))
    scaled_rect = scaled_bouton.get_rect(center=button_rect.center)
    screen.blit(scaled_bouton, scaled_rect.topleft)
    return bouton_scale
