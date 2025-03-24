import pygame
from joueur import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.player = Player(0, 0)
        self.background = pygame.image.load("images/fond1.png")  # Charge l'image de fond
        self.background = pygame.transform.scale(self.background, (1000, 600))  # Ajuste la taille

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        self.player.velocity = [0, 0]

        if keys[pygame.K_LEFT]:
            self.player.velocity[0] = -1
        if keys[pygame.K_RIGHT]:
            self.player.velocity[0] = 1
        if keys[pygame.K_UP]:
            self.player.velocity[1] = -1
        if keys[pygame.K_DOWN]:
            self.player.velocity[1] = 1

    def update(self):
        self.player.move()

    def display(self):
        self.screen.blit(self.background, (0, 0))  # Affiche l'image de fond
        self.player.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.display()
            self.clock.tick(60)

pygame.init()
screen = pygame.display.set_mode((1000, 600))
game = Game(screen)
game.run()
pygame.quit()