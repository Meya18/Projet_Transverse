import math

def trajectoire(V0, theta_deg, g=9.81):
    theta = math.radians(theta_deg)  # Convertir l'angle en radians

    # Calcul du temps de vol et de la portée maximale
    t_flight = (2 * V0 * math.sin(theta)) / g
    x_max = V0 * math.cos(theta) * t_flight

    # Génération des points de la trajectoire
    x_values = []
    y_values = []
    step = x_max / 50  # Pas pour un affichage fluide

    x = 0
    while x <= x_max:
        y = x * math.tan(theta) - (g / (2 * V0 ** 2 * math.cos(theta) ** 2)) * x ** 2
        x_values.append(x)
        y_values.append(max(0, y))  # Éviter les valeurs négatives
        x += step

    return x_values, y_values

def print_trajectory(V0, theta_deg):
    x_values, y_values = trajectoire(V0, theta_deg)

    print("\nTrajectoire de la Poké Ball:")
    print(f"Vitesse initiale: {V0} m/s, Angle: {theta_deg}°\n")

    for x, y in zip(x_values, y_values):
        print(f"x = {x:.2f} m, y = {y:.2f} m")

# Demande des paramètres à l'utilisateur
try:
    V0 = float(input("Entrez la vitesse initiale (m/s) : "))
    angle = float(input("Entrez l'angle de lancement (degrés) : "))
    print_trajectory(V0, angle)
except ValueError:
    print("Veuillez entrer des valeurs numériques valides.")
