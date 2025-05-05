import pygame
import math
import random
from load_image import *

# Constantes
WIDTH, HEIGHT = 1000, 600
BALL_RADIUS = 10
TARGET_RADIUS = 30
GRAVITY = 25
POWER_MAX = 20
SPEED_FACTOR = 5  # Vitesse d'affichage de la trajectoire


def trajectoire(V0, theta_deg, x0=0, y0=0, g=GRAVITY):
    theta = math.radians(theta_deg)
    t_flight = (2 * V0 * math.sin(theta)) / g
    num_points = int(t_flight * 60)
    if num_points < 2:
        num_points = 2

    x_values = []
    y_values = []

    for i in range(num_points):
        t = i * t_flight / (num_points - 1)
        x = V0 * math.cos(theta) * t
        y = V0 * math.sin(theta) * t - 0.5 * g * t**2
        x_values.append(x0 + x)
        y_values.append(y0 - y)  # car l'axe Y descend en Pygame

    return x_values, y_values, t_flight


class Balle:
    def __init__(self, image_path, start_pos):
        raw = pygame.image.load(image_path).convert_alpha()
        self.base_img = pygame.transform.scale(raw, (20, 20))
        self.pos = list(start_pos)
        self.angle = 0
        self.fired = False
        self.rect = self.base_img.get_rect(center=self.pos)
        self.start_pos = list(start_pos)
        self.time = 0
        self.trajectory_x = []
        self.trajectory_y = []
        self.time_to_fly = 0

    def update(self):
        if self.fired and self.time_to_fly > 0:
            self.time += 1 / 60
            index = int(self.time * 60 * SPEED_FACTOR)

            if index < len(self.trajectory_x):
                x = self.trajectory_x[index]
                y = self.trajectory_y[index]
            else:
                self.reset(self.start_pos)
                return

            self.pos = [x, y]
            self.rect = self.base_img.get_rect(center=self.pos)
            self.angle += 5

            if y >= HEIGHT:
                self.reset(self.start_pos)

    def draw(self, win):
        if self.fired:
            rotated = pygame.transform.rotate(self.base_img, self.angle)
            rect = rotated.get_rect(center=self.rect.center)
            win.blit(rotated, rect)
        else:
            win.blit(self.base_img, self.rect)

    def reset(self, start_pos):
        self.pos = list(start_pos)
        self.angle = 0
        self.fired = False
        self.time = 0
        self.rect = self.base_img.get_rect(center=self.pos)
        self.trajectory_x = []
        self.trajectory_y = []
        self.time_to_fly = 0

    def set_velocity(self, power, mouse_pos):
        dx, dy = mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        angle_deg = math.degrees(math.atan2(-dy, dx))  # -dy car Y descend
        velocity_multiplier = 10
        V0 = power * velocity_multiplier
        self.trajectory_x, self.trajectory_y, t_flight = trajectoire(V0, angle_deg, x0=self.pos[0], y0=self.pos[1])
        self.time_to_fly = t_flight / SPEED_FACTOR
        self.fired = True


class Cible:
    def __init__(self, image_surface, center_pos):
        self.img = pygame.transform.scale(image_surface, (60, 60))
        self.rect = self.img.get_rect(center=center_pos)
        self.hit = False
        self.speed = 2
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        if self.rect.left < WIDTH // 2:
            self.rect.left = WIDTH // 2
            self.dx *= -1
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.dx *= -1

        if self.rect.top < 0:
            self.rect.top = 0
            self.dy *= -1
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.dy *= -1

    def check_collision(self, ball_pos):
        dist = math.hypot(ball_pos[0] - self.rect.centerx, ball_pos[1] - self.rect.centery)
        return dist <= BALL_RADIUS + TARGET_RADIUS

    def draw(self, win):
        win.blit(self.img, self.rect)
        if self.hit:
            pygame.draw.circle(win, (0, 255, 0), self.rect.center, TARGET_RADIUS, 3)


class Chargeur:
    def __init__(self):
        self.charging = False
        self.power = 0

    def update(self):
        if self.charging:
            self.power = min(self.power + 0.3, POWER_MAX)

    def draw(self, win):
        if self.charging:
            pygame.draw.rect(win, (0, 0, 0), (50, 50, self.power * 10, 10))

    def reset(self):
        self.charging = False
        self.power = 0


def interface_capture(surface):
    balle = Balle("images/pokeball.png", (100, HEIGHT - 100))
    pokemons = {
        "carapuce": carapuce,
        "darkrai" : darkrai,
        "dracaufeu": dracaufeu,
        "dracolosse": dracolosse,
        "evoli": evoli,
        "herbizarre": herbizarre,
        "lucario": lucario,
        "metalosse": metalosse,
        "mew": mew,
        "nymphali": nymphali,
        "pikachu": pikachu,
        "carabaffe": carabaffe
    }

    random_key = random.choice(list(pokemons.keys()))
    cible = Cible(pokemons[random_key], (800, 400))
    chargeur = Chargeur()
    fond = pygame.transform.scale(pygame.image.load("images/fond_combat.jpg").convert(), (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # quitter le mini-jeu

            elif event.type == pygame.MOUSEBUTTONDOWN and not balle.fired:
                chargeur.charging = True
                chargeur.power = 0

            elif event.type == pygame.MOUSEBUTTONUP and chargeur.charging:
                balle.set_velocity(chargeur.power, pygame.mouse.get_pos())
                chargeur.reset()
                cible.hit = False

        surface.blit(fond, (0, 0))
        chargeur.update()
        chargeur.draw(surface)
        cible.update()
        cible.draw(surface)
        balle.update()
        balle.draw(surface)

        if balle.fired and cible.check_collision(balle.pos):
            cible.hit = True
            balle.reset((100, HEIGHT - 100))

        pygame.display.flip()
        clock.tick(60)
