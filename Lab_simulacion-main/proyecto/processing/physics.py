import math
from .objects import Planet, Moon
from .utils import Vector2D

G = 6.67430e-11  # Constante gravitacional

class Celestialbodies: #Maneja la lista de todos los planetas y lunas
    def __init__(self):
        self.planets = []
        self.moons = []

    def add_planet(self, planet: Planet):
        self.planets.append(planet)

    def add_moon(self, moon: Moon):
        self.moons.append(moon)

    def apply_gravity(self, dt): #Aplica la fuerza gravitacional entre todos los pares de planetas y gestiona colisiones, cuando 2 planetas chocan, se fucionan
        """Aplica la fuerza gravitacional entre los planetas."""
        for i, planet1 in enumerate(self.planets):
            for planet2 in self.planets[i + 1:]:
                r_vec = planet2.position - planet1.position
                distance = math.sqrt(r_vec.x ** 2 + r_vec.y ** 2)

                if distance > 0:
                    force = (G * planet1.mass * planet2.mass) / (distance ** 2)
                    direction = Vector2D(r_vec.x / distance, r_vec.y / distance)

                    planet1._velocity += direction * (force / planet1.mass) * dt
                    planet2._velocity -= direction * (force / planet2.mass) * dt

                # Detectar colisión
                if distance <= planet1.size + planet2.size:
                    self.handle_collision(planet1, planet2)

    def handle_collision(self, planet1: Planet, planet2: Planet): #Implementa una fusión conservando el momento lineal, cuando se fusionan, se crea un nuevo planeta con propiedades promediadas o sumadas
        """Fusiona dos planetas si colisionan."""
        new_mass = planet1.mass + planet2.mass
        new_velocity = (planet1.velocity * planet1.mass + planet2.velocity * planet2.mass) / new_mass
        new_position = (planet1.position + planet2.position) * 0.5

        # Crear un nuevo planeta y eliminar los anteriores
        new_planet = Planet(new_mass, new_position, new_velocity)
        self.planets.remove(planet1)
        self.planets.remove(planet2)
        self.add_planet(new_planet)

    def update(self, dt, gravity, bodies):
        """Actualiza todos los objetos en cada frame."""
        self.apply_gravity(dt)
        for planet in self.planets:
            planet.update(dt)
        for moon in self.moons:
            moon.update(dt)