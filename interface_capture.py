import pygame
import math
from music import *
import random
from load_image import *

# Constantes
WIDTH, HEIGHT = 1000, 600
BALL_RADIUS = 10
TARGET_RADIUS = 55
GRAVITY = 25
POWER_MAX = 20
SPEED_FACTOR = 5  # Vitesse d'affichage de la trajectoire
# inventaire des cibles capturées
inventory = []
INVENTORY_PANEL_HEIGHT = 150
INVENTORY_SLOTS = 6
SLOT_SIZE = 20
SLOT_MARGIN = 50
music_manager = MusicManager()
panel_img = None
panel_w = panel_h = 0
panel_pos = (0, 0)
def trajectoire(V0, theta_deg, x0=0, y0=0, g=GRAVITY):
    theta = math.radians(theta_deg)
    # tenir compte de la hauteur initiale h0 = (écran bas) – y0
    h0 = HEIGHT - y0
    # résolution de -½gt² + V0·sinθ·t + h0 = 0
    D = (V0 * math.sin(theta)) ** 2 + 2 * g * h0
    t_flight = (V0 * math.sin(theta) + math.sqrt(D)) / g
    num_points = int(t_flight * 60)
    if num_points < 2:
        num_points = 2

    x_values = []
    y_values = []

    for i in range(num_points):
        t = i * t_flight / (num_points - 1)
        x = V0 * math.cos(theta) * t
        # calcul de la hauteur h par rapport au bas
        h = h0 + V0 * math.sin(theta) * t - 0.5 * g * t ** 2
        x_values.append(x0 + x)
        y_values.append(HEIGHT - h)

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
        self.img = self.scale_image_keep_ratio(image_surface, 110)
        # placer la cible au sol, et ne bouger qu’horizontalement
        self.rect = self.img.get_rect(center=(center_pos[0], HEIGHT - TARGET_RADIUS))
        self.speed = 2
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])
        self.hit = False
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            # bouger horizontalement et verticalement
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
        # déplacement horizontal et vertical
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        # rebondir entre la moitié droite et le bord droit
        if self.rect.left < WIDTH // 2:
            self.rect.left = WIDTH // 2
            self.dx *= -1
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.dx *= -1
        if self.rect.top < HEIGHT // 2:
            self.rect.top = HEIGHT // 2
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

    def scale_image_keep_ratio(self, image, target_size):
        rect = image.get_rect()
        width, height = rect.width, rect.height

        if width > height:
            new_width = target_size
            new_height = int(height * target_size / width)
        else:
            new_height = target_size
            new_width = int(width * target_size / height)

        return pygame.transform.smoothscale(image, (new_width, new_height))


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
def draw_inventory(surface, final):
    global panel_img, panel_w, panel_h, panel_pos
    if panel_img is None:
        raw = pygame.image.load("images/inventaire.png").convert_alpha()
        rw, rh = raw.get_size()
        panel_w = WIDTH - 2 * SLOT_MARGIN
        panel_h = int(rh * panel_w / rw)
        panel_img = pygame.transform.scale(raw, (panel_w, panel_h))
        y_offset = 0
        if final:
            y_offset = 150
        panel_pos = (SLOT_MARGIN, HEIGHT - panel_h + 200 + y_offset)
    surface.blit(panel_img, panel_pos)
    border = 10
    slot_w = (panel_w - border * (INVENTORY_SLOTS + 1)) / INVENTORY_SLOTS - 12
    slot_h = panel_h - 2 * border
    max_icon_size = int(min(slot_w, slot_h) * 0.9)

    for i, slot in enumerate(inventory):
        img_rect = slot.get_rect()
        w, h = img_rect.size
        if w > h:
            new_w = max_icon_size
            new_h = int(h * new_w / w)
        else:
            new_h = max_icon_size
            new_w = int(w * new_h / h)

        scaled_img = pygame.transform.smoothscale(slot, (new_w, new_h))
        x = panel_pos[0] + border + i * (slot_w + border) + (slot_w - new_w) // 2 + 35-i
        y = panel_pos[1] + border + (slot_h - new_h) // 2 - 35-i
        surface.blit(scaled_img, (x, y))

def draw_inventory_final(surface, final):
    global panel_img, panel_w, panel_h, panel_pos
    if panel_img is None:
        raw = pygame.image.load("images/inventaire.png").convert_alpha()
        rw, rh = raw.get_size()
        panel_w = WIDTH - 2 * SLOT_MARGIN
        panel_h = int(rh * panel_w / rw)
        panel_img = pygame.transform.scale(raw, (panel_w, panel_h))
        y_offset = 0
        if final:
            y_offset = 150
        panel_pos = (SLOT_MARGIN, HEIGHT - panel_h + 200 + 150)
    surface.blit(panel_img, panel_pos)
    border = 10
    slot_w = (panel_w - border * (INVENTORY_SLOTS + 1)) / INVENTORY_SLOTS - 12
    slot_h = panel_h - 2 * border
    max_icon_size = int(min(slot_w, slot_h) * 0.9)

    for i, slot in enumerate(inventory):
        img_rect = slot.get_rect()
        w, h = img_rect.size
        if w > h:
            new_w = max_icon_size
            new_h = int(h * new_w / w)
        else:
            new_h = max_icon_size
            new_w = int(w * new_h / h)

        scaled_img = pygame.transform.smoothscale(slot, (new_w, new_h))
        x = panel_pos[0] + border + i * (slot_w + border) + (slot_w - new_w) // 2 + 35-i
        y = panel_pos[1] + border + (slot_h - new_h) // 2 - 35-i
        surface.blit(scaled_img, (x, y))
def interface_capture(surface,player_image):
    start_pos = (100, HEIGHT - 100)
    balle = Balle("images/pokeball.png", start_pos)
    ball_icon = pygame.transform.scale(pygame.image.load("images/pokeball.png").convert_alpha(),(20, 20))
    font_counter = pygame.font.SysFont("Arial", 24)
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
    fond = fond_capture
    # préparer l’image du joueur passée en paramètre
    player_img = pygame.transform.scale(player_image, (60, 60))
    player_pos = (balle.start_pos[0] - 70, balle.start_pos[1])
    clock = pygame.time.Clock()
    inventory_visible = False
    attempt_count = 0
    running = True

    while running:
        music_manager.set_etat("combat")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory_visible = not inventory_visible
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # quitter le mini-jeu

            elif event.type == pygame.MOUSEBUTTONDOWN and not balle.fired:
                chargeur.charging = True
                chargeur.power = 0

            elif event.type == pygame.MOUSEBUTTONUP and chargeur.charging:
                attempt_count += 1
                balle.set_velocity(chargeur.power, pygame.mouse.get_pos())
                chargeur.reset()
                cible.hit = False

        surface.blit(fond, (0, 0))
        essais_restants = max(0, 5 - attempt_count)
        surface.blit(ball_icon, (10, 10))
        counter_surf = font_counter.render(f"x {essais_restants}", True, (0, 0, 0))
        surface.blit(counter_surf, (35, 12))
        if inventory_visible:
            draw_inventory(surface,False)
        if not balle.fired and chargeur.charging:
            start = balle.start_pos
            end = pygame.mouse.get_pos()
            pygame.draw.line(surface, (255, 0, 0), start, end, 2)
            # calcul de la tête de flèche
            theta = math.atan2(end[1] - start[1], end[0] - start[0])
            arrow_len = 15
            back = (end[0] - arrow_len * math.cos(theta), end[1] - arrow_len * math.sin(theta))
            head_size = 8
            left = (back[0] + head_size * math.sin(theta), back[1] - head_size * math.cos(theta))
            right = (back[0] - head_size * math.sin(theta), back[1] + head_size * math.cos(theta))
            pygame.draw.polygon(surface, (255, 0, 0), [end, left, right])
        chargeur.update()
        chargeur.draw(surface)
        cible.update()
        cible.draw(surface)
        surface.blit(
            player_img,
            player_img.get_rect(center=player_pos)
        )
        balle.update()
        balle.draw(surface)

        if balle.fired and cible.check_collision(balle.pos):
            cible.hit = True
            # stocker l'image de la cible si place dispo
            if len(inventory) < INVENTORY_SLOTS:
                inventory.append(pokemons[random_key])
            balle.reset(start_pos)
            music_manager.set_etat("jeu")
            return  # quitte le mini-jeu et revient à la scène précédente
        if not balle.fired and attempt_count >= 5 and not cible.hit:
            music_manager.set_etat("jeu")
            return
        pygame.display.flip()
        clock.tick(60)

