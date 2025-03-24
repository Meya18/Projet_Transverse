import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Afficher une image avec des personnages")

image_fond = pygame.image.load(r"C:\Users\HP\Downloads\bourg-palette.png")
image_fond = pygame.transform.scale(image_fond, (1000, 600))

personnage1 = pygame.image.load("C:\Users\HP\Downloads\Jessie.jpg")
personnage1 = pygame.transform.scale(personnage1, (100, 150))

personnage2 = pygame.image.load(r"C:\Users\HP\Downloads\personnage2.jpg")
personnage2 = pygame.transform.scale(personnage2, (100, 150))

personnage3 = pygame.image.load(r"C:\Users\HP\Downloads\personnage3.jpg")
personnage3 = pygame.transform.scale(personnage3, (100, 150))

personnage1_rect = personnage1.get_rect()
personnage1_rect.topleft = (400, 300)

personnage2_rect = personnage2.get_rect()
personnage2_rect.topleft = (600, 300)

personnage3_rect = personnage3.get_rect()
personnage3_rect.topleft = (200, 300)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((250, 250, 250))
    screen.blit(image_fond, (0, 0))

    screen.blit(personnage1, personnage1_rect)
    screen.blit(personnage2, personnage2_rect)
    screen.blit(personnage3, personnage3_rect)

    pygame.display.update()

pygame.quit()
