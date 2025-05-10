import pygame

# Obstacles fond1
obstacles = [
    pygame.Rect(545, 290, 285, 125),
    pygame.Rect(205, 105, 220, 135),
    pygame.Rect(170, 200, 35, 40),
    pygame.Rect(585, 100, 240, 140),
    pygame.Rect(550, 200, 35, 40),
    pygame.Rect(205, 325, 215, 30),
    pygame.Rect(210, 425, 35, 20),
    pygame.Rect(540, 480, 255, 30),
    pygame.Rect(290, 510, 170, 90),
    pygame.Rect(0, 0, 500, 60),
    pygame.Rect(585, 0, 415, 60),
    pygame.Rect(0, 0, 80, 600),
    pygame.Rect(920, 0, 80, 600),
    pygame.Rect(80, 575, 155, 25),
    pygame.Rect(765, 575, 155, 25)
]

# Obstacles fond2
obstacles_fond2 = [
    pygame.Rect(0, 0, 1000, 60),
    pygame.Rect(710, 60, 290, 155),
    pygame.Rect(940, 215, 60, 85),
    pygame.Rect(890, 215, 50, 30),
    pygame.Rect(365, 60, 225, 60),
    pygame.Rect(40, 60, 30, 30),
    pygame.Rect(0, 190, 10, 410),
    pygame.Rect(10, 425, 55, 175),
    pygame.Rect(65, 545, 175, 55),
    pygame.Rect(480, 545, 520, 55),
    pygame.Rect(715, 485, 285, 60),
    pygame.Rect(830, 425, 170, 60),
    pygame.Rect(945, 360, 55, 65),
    pygame.Rect(305, 205, 110, 190),
    pygame.Rect(415, 175, 65, 190),
    pygame.Rect(480, 235, 60, 190),
    pygame.Rect(540, 300, 50, 125),
    pygame.Rect(160, 390, 55, 65),
    pygame.Rect(220, 420, 50, 65),
    pygame.Rect(710, 275, 30, 30),
    pygame.Rect(10, 200, 60, 15),
    pygame.Rect(130, 200, 175, 15),
    pygame.Rect(544, 120, 20, 150)
]

#obstacles maison 1
obstacles_maison1 = [
    pygame.Rect(0, 0, 175, 600),
    pygame.Rect(825, 0, 175, 600),
    pygame.Rect(175, 0, 650, 90),
    pygame.Rect(175, 555, 95, 45),
    pygame.Rect(270, 580, 75, 20),
    pygame.Rect(345, 555, 480, 45),
    pygame.Rect(175, 230, 45, 90),
    pygame.Rect(175, 370, 45, 90),
    pygame.Rect(780, 230, 45, 90),
    pygame.Rect(780, 370, 45, 90),
    pygame.Rect(440, 290, 165, 75),
    pygame.Rect(475, 250, 90, 40),
    pygame.Rect(220, 90, 80, 50),
    pygame.Rect(390, 90, 85, 50),
    pygame.Rect(570, 90, 80, 50),
    pygame.Rect(700, 90, 125, 50),
]

#obstacles maison 2
obstacles_maison2 = [
    pygame.Rect(0, 0, 1000, 130),
    pygame.Rect(0, 130, 380, 25),
    pygame.Rect(465, 130, 130, 25),
    pygame.Rect(850, 130, 150, 90),
    pygame.Rect(395, 260, 285, 125),
    pygame.Rect(0, 405, 70, 110),
    pygame.Rect(930, 405, 70, 110),
    pygame.Rect(0, 585, 360, 15),
    pygame.Rect(490, 585, 510, 15)
]

#obstacles étage
obstacles_etage = [
    pygame.Rect(0, 0, 1000, 210),
    pygame.Rect(0, 210, 200, 390),
    pygame.Rect(800, 210, 200, 390),
    pygame.Rect(200, 570, 600, 30),
    pygame.Rect(465, 190, 130, 50),
    pygame.Rect(675, 210, 125, 20),
    pygame.Rect(740, 230, 60, 35),
    pygame.Rect(655, 325, 90, 100)
]

#obstacles laboratoire
obstacles_laboratoire = [
    pygame.Rect(0, 0, 25, 600),
    pygame.Rect(25, 0, 1000, 130),
    pygame.Rect(955, 130, 45, 470),
    pygame.Rect(25, 470, 345, 130),
    pygame.Rect(555, 470, 400, 130),
    pygame.Rect(25, 130, 415, 30),
    pygame.Rect(635, 130, 320, 30),
    pygame.Rect(25, 160, 65, 165),
    pygame.Rect(560, 260, 230, 80),
    pygame.Rect(110, 225, 135, 140)
]

#ouverture de l'interface de capture
capture_fond2 = [
    pygame.Rect(160, 460, 5, 5),
    pygame.Rect(190, 520, 5, 5),
    pygame.Rect(280, 575, 5, 5),
    pygame.Rect(100, 310, 5, 5),
    pygame.Rect(220, 215, 5, 5),
    pygame.Rect(15, 370, 5, 5),
    pygame.Rect(425, 370, 5, 5),
    pygame.Rect(365, 430, 5, 5),
    pygame.Rect(450, 460, 5, 5),
    pygame.Rect(680, 65, 5, 5),
    pygame.Rect(680, 155, 5, 5),
    pygame.Rect(595, 95, 5, 5),
    pygame.Rect(280, 70, 5, 5)
]

# Rectangle passage de scène
passage_rect = [
    pygame.Rect(500, 0, 90, 30), #fond2
    pygame.Rect(260,240,20,5), #maison 1
    pygame.Rect(635,240,20,5), #maison 2
    pygame.Rect(675,420,20,2), #laboratoire
    pygame.Rect(270,575,70,2), #maison1 -> jeu
    pygame.Rect(360,595,125,2), #maison2 -> jeu
    pygame.Rect(260,210,80,2), #etage -> maison2
    pygame.Rect(360,595,120,2), #fond2 -> jeu
    pygame.Rect(845,120,5,90), #maison2 -> etage
    pygame.Rect(370, 595, 190, 5)  #laboratoire -> jeu
]
