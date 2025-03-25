import pygame

pygame.init()

# Définition de la fenêtre
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Jeu Team Rocket")

# Chargement des images
background = pygame.image.load("images/fond1.png")
background = pygame.transform.scale(background, (1000, 600))
debut_image = pygame.image.load("images/debut.jpeg")
debut_image = pygame.transform.scale(debut_image, (1000, 600))
bouton_debut = pygame.image.load("images/bouton_debut.webp")

# Bouton du début
bouton_largeur, bouton_hauteur = 300, 150
bouton_debut = pygame.transform.scale(bouton_debut, (bouton_largeur, bouton_hauteur))
button_rect = bouton_debut.get_rect(center=(500, 500))
bouton_scale = 1.0
hovering = False

# Définition du joueur
player = {"x": 487, "y": 560, "speed": 5, "image": pygame.Surface((25, 25))}
player["image"].fill((255, 0, 0))

# Liste des obstacles
obstacles = [
    pygame.Rect(530, 285, 305, 140),  # Maison en bas à droite
    pygame.Rect(170, 105, 250, 135),  # Maison en haut à gauche
    pygame.Rect(525, 100, 300, 140),  # Maison en haut à droite
    pygame.Rect(205, 325, 215, 125),  # Jardin en bas à gauche
    pygame.Rect(540, 480, 255, 30),  # Barrière en bas à droite
    pygame.Rect(290, 510, 170, 90),  # Lac en bas au milieu
    pygame.Rect(0, 0, 500, 60),  # Forêt en haut à gauche
    pygame.Rect(585, 0, 415, 60),  # Forêt en haut à droite
    pygame.Rect(0, 0, 80, 600),  # Forêt à gauche
    pygame.Rect(920, 0, 80, 600),  # Forêt à droite
    pygame.Rect(80, 575, 155, 25),  # Forêt en bas à gauche
    pygame.Rect(765, 575, 155, 25)  # Forêt en bas à droite
]

scenes = {
    "debut": {"fond": debut_image, "bouton": bouton_debut},
    "jeu": {"fond": background, "joueur": player, "obstacles": obstacles}
}

current_scene = "debut"

# Boucle du jeu
running = True
clock = pygame.time.Clock()

while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and current_scene == "debut":
            if button_rect.collidepoint(event.pos):
                current_scene = "jeu"

    screen.fill((0, 0, 0))

    if current_scene == "debut":
        screen.blit(scenes["debut"]["fond"], (0, 0))

        # Gestion de l'effet sur le bouton
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

    elif current_scene == "jeu":
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -player["speed"]
        if keys[pygame.K_RIGHT]:
            dx = player["speed"]
        if keys[pygame.K_UP]:
            dy = -player["speed"]
        if keys[pygame.K_DOWN]:
            dy = player["speed"]

        # Vérification des collisions avec les bords et obstacles
        new_x = player["x"] + dx
        new_y = player["y"] + dy
        new_rect = pygame.Rect(new_x, new_y, 25, 25)
        if 0 <= new_x <= 975 and 0 <= new_y <= 575 and not any(new_rect.colliderect(obs) for obs in obstacles):
            player["x"], player["y"] = new_x, new_y

        screen.blit(scenes["jeu"]["fond"], (0, 0))
        screen.blit(player["image"], (player["x"], player["y"]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
