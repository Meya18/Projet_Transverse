import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("miouss.jpg")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.velocity = [0, 0]

    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def draw(self, screen):
        screen.blit(self.image, self.rect)