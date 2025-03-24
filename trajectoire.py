import math


def trajectoire(V0, theta_deg, g=9.81):
    theta = math.radians(theta_deg)  # Convertir l'angle en radians

    # Calcul de la portée maximale
    t_flight = 2 * V0 * math.sin(theta) / g  # Temps de vol total
    x_max = V0 * math.cos(theta) * t_flight  # Portée maximale

    # Génération des points de la trajectoire
    x_values = []
    y_values = []
    step = x_max / 50  # Nombre de points
    x = 0
    while x <= x_max:
        y = x * math.tan(theta) - (g / (2 * V0 ** 2 * math.cos(theta) ** 2)) * x ** 2
        if y < 0:
            break
        x_values.append(x)
        y_values.append(y)
        x += step

    return x_values, y_values


def print_trajectory(V0, theta_deg):
    x_values, y_values = trajectoire(V0, theta_deg)

    print("Trajectoire de la Poké Ball:")
    for x, y in zip(x_values, y_values):
        print(f"x = {x:.2f} m, y = {y:.2f} m")


# Paramètres d'entrée
V0 = 15  # Vitesse initiale en m/s
angle = 45  # Angle de lancement en degrés
print_trajectory(V0, angle)