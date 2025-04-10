import pygame

pygame.init()

# Définition de la fenêtre
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Jeu Team Rocket")

# Chargement des images de fond
background = pygame.image.load("images/fond1.png")
background = pygame.transform.scale(background, (1000, 600))
debut_image = pygame.image.load("images/debut.jpeg")
debut_image = pygame.transform.scale(debut_image, (1000, 600))
choix_perso_image = pygame.image.load("images/choix_perso.jpg")
choix_perso_image = pygame.transform.scale(choix_perso_image, (1000, 600))

# Chargement des personnages pour la sélection
persos = {
    "james": pygame.image.load("images/james_p.png"),
    "jessie": pygame.image.load("images/jessie_p.png"),
    "chouette": pygame.image.load("images/chouette_p.png")
}

# Images pour le personnage sélectionné (utilisé dans la scène de jeu)
joueur_images = {
    "james": pygame.image.load("images/james_f.png"),
    "jessie": pygame.image.load("images/jessie_f.png"),
    "chouette": pygame.image.load("images/chouette_f.png")
}

# Taille par défaut des personnages
perso_sizes = {
    "james": {"width": 200, "height": 200},
    "jessie": {"width": 200, "height": 200},
    "chouette": {"width": 200, "height": 200}
}

# Redimensionnement des personnages
for key in persos:
    persos[key] = pygame.transform.scale(persos[key], (perso_sizes[key]["width"], perso_sizes[key]["height"]))
for key in joueur_images:
    joueur_images[key] = pygame.transform.scale(joueur_images[key], (30, 30))

# Positions des personnages
perso_positions = {
    "james": (225, 400),
    "jessie": (775, 400),
    "chouette": (500, 400)
}

# Police pour les textes (garde la police par défaut)
font_titre = pygame.font.SysFont("Arial", 40, bold=True)
font_nom = pygame.font.SysFont("Arial", 30)

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Bouton du début
bouton_largeur, bouton_hauteur = 300, 150
bouton_debut = pygame.image.load("images/bouton_debut.png")
bouton_debut = pygame.transform.scale(bouton_debut, (bouton_largeur, bouton_hauteur))
button_rect = bouton_debut.get_rect(center=(500, 500))
bouton_scale = 1.0

# Variables pour l'animation des personnages
perso_scale = {"james": 1.0, "jessie": 1.0, "chouette": 1.0}
player_image = None

# Liste des obstacles
obstacles = [
    pygame.Rect(530, 285, 305, 140),
    pygame.Rect(170, 105, 250, 135),
    pygame.Rect(525, 100, 300, 140),
    pygame.Rect(205, 325, 215, 125),
    pygame.Rect(540, 480, 255, 30),
    pygame.Rect(290, 510, 170, 90),
    pygame.Rect(0, 0, 500, 60),
    pygame.Rect(585, 0, 415, 60),
    pygame.Rect(0, 0, 80, 600),
    pygame.Rect(920, 0, 80, 600),
    pygame.Rect(80, 575, 155, 25),
    pygame.Rect(765, 575, 155, 25)
]

scenes = {
    "debut": {"fond": debut_image, "bouton": bouton_debut},
    "choix_perso": {"fond": choix_perso_image, "persos": persos},
    "jeu": {"fond": background, "joueur": None, "obstacles": obstacles}
}

current_scene = "debut"
player = {"x": 487, "y": 560, "speed": 5, "image": None}

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
                        current_scene = "jeu"

    screen.fill(noir)

    if current_scene == "debut":
        screen.blit(scenes["debut"]["fond"], (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_x, mouse_y):
            if bouton_scale > 0.9:
                bouton_scale -= 0.01
        else:
            if bouton_scale < 1.0:
                bouton_scale += 0.01
        scaled_bouton = pygame.transform.scale(bouton_debut,
                                               (int(bouton_largeur * bouton_scale), int(bouton_hauteur * bouton_scale)))
        scaled_rect = scaled_bouton.get_rect(center=button_rect.center)
        screen.blit(scaled_bouton, scaled_rect.topleft)

    elif current_scene == "choix_perso":
        screen.blit(scenes["choix_perso"]["fond"], (0, 0))
        # Titre en noir
        titre = font_titre.render("Choisissez votre personnage", True, noir)
        screen.blit(titre, (500 - titre.get_width() // 2, 30))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for perso, pos in perso_positions.items():
            rect = pygame.Rect(pos[0] - 50, pos[1] - 50, 100, 100)
            if rect.collidepoint(mouse_x, mouse_y):
                if perso_scale[perso] > 0.9:
                    perso_scale[perso] -= 0.01
            else:
                if perso_scale[perso] < 1.0:
                    perso_scale[perso] += 0.01

            scaled_perso = pygame.transform.scale(persos[perso],
                                                  (int(perso_sizes[perso]["width"] * perso_scale[perso]),
                                                   int(perso_sizes[perso]["height"] * perso_scale[perso])))
            scaled_rect = scaled_perso.get_rect(center=pos)
            screen.blit(scaled_perso, scaled_rect.topleft)

            # Affichage du nom sous chaque personnage en blanc
            nom = {"jessie": "Jessie", "james": "James", "chouette": "Effraie"}[perso]
            texte_nom = font_nom.render(nom, True, blanc)
            screen.blit(texte_nom, (pos[0] - texte_nom.get_width() // 2, pos[1] + perso_sizes[perso]["height"] // 2))

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

        new_x = player["x"] + dx
        new_y = player["y"] + dy
        new_rect = pygame.Rect(new_x, new_y, 30, 30)
        if 0 <= new_x <= 970 and 0 <= new_y <= 570 and not any(new_rect.colliderect(obs) for obs in obstacles):
            player["x"], player["y"] = new_x, new_y

        screen.blit(scenes["jeu"]["fond"], (0, 0))
        if player["image"]:
            screen.blit(player["image"], (player["x"], player["y"]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()