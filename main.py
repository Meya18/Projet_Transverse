import pygame

pygame.init()

# Définition de la fenêtre
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Jeu Team Rocket")

# Chargement des images
background = pygame.image.load("images/fond1.png")
background = pygame.transform.scale(background, (1000, 600))

# Définition du joueur
player = {"x": 487, "y": 560, "speed": 5, "image": pygame.Surface((25, 25))}
player["image"].fill((255, 0, 0))

# Liste des obstacles
obstacles = [
    pygame.Rect(530, 285, 305, 140),  # Maison en bas à droite
    pygame.Rect(170, 105, 250, 135),  # Maison en haut à gauche
    pygame.Rect(525, 100, 300, 140),  # Maison en haut à droite
    pygame.Rect(205, 325, 215, 125),  # Jardin en bas à gauche
    pygame.Rect(540, 480, 255, 30),   # Barrière en bas à droite
    pygame.Rect(290, 510, 170, 90),   # Lac en bas au milieu
    pygame.Rect(0, 0, 500, 60),   # Forêt en haut à gauche
    pygame.Rect(585, 0, 415, 60),   # Forêt en haut à droite
    pygame.Rect(0, 0, 80, 600),   # Forêt à gauche
    pygame.Rect(920, 0, 80, 600),   # Forêt à droite
    pygame.Rect(80, 575, 155, 25),  # Forêt en bas à gauche
    pygame.Rect(765, 575, 155, 25)  # Forêt en bas à droite
]

# Scène sous forme de tableau 2D
scenes = [
    ["Fond", background],
    ["Joueur", player],
    ["Obstacles", obstacles]
]

# Boucle du jeu
running = True
clock = pygame.time.Clock()

while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement du joueur
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

    # Vérification des collisions avec les bords et les obstacles
    new_x = player["x"] + dx
    new_y = player["y"] + dy
    new_rect = pygame.Rect(new_x, new_y, 25, 25)

    if 0 <= new_x <= 975 and 0 <= new_y <= 575 and not any(new_rect.colliderect(obs) for obs in obstacles):
        player["x"], player["y"] = new_x, new_y

    # Affichage
    screen.blit(scenes[0][1], (0, 0))  # Fond
    screen.blit(player["image"], (player["x"], player["y"]))  # Joueur

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
