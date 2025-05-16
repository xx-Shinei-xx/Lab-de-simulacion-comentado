import pygame
from .utils import Vector2D, random_color, random_shape
import random
from multiprocessing import Pool  # Importación para usar multiprocesos

class PhysicalProperties:  # Encapsulamiento, se define una clase que encapsula las propiedades físicas de un objeto
    def __init__(self, mass: float, position: Vector2D, velocity: Vector2D):
        # Encapsulamiento, esto restringe el acceso directo
        self._mass = mass
        self._position = position
        self._velocity = velocity

    @property
    def mass(self):
        return self._mass

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity


class GraphicalProperties:  # Propiedades gráficas, color, forma y tamaño
    def __init__(self, color: tuple, size: int, shape: str):
        self.color = color
        self.size = size
        self.shape = shape

    def draw(self, surface):  # Aquí se aplica polimorfismo, el comportamiento cambia según el valor del atributo "shape"
        pos_tuple = (int(self.position.x), int(self.position.y))
        if self.shape == "circle":
            pygame.draw.circle(surface, self.color, pos_tuple, self.size)
        elif self.shape == "square":
            pygame.draw.rect(surface, self.color, (pos_tuple[0], pos_tuple[1], self.size * 2, self.size * 2))
        elif self.shape == "triangle":
            points = [
                (pos_tuple[0], pos_tuple[1] - self.size),
                (pos_tuple[0] - self.size, pos_tuple[1] + self.size),
                (pos_tuple[0] + self.size, pos_tuple[1] + self.size)
            ]
            pygame.draw.polygon(surface, self.color, points)


class Planet(PhysicalProperties, GraphicalProperties):  #se define una clase con herencia múltiple y agregación, se heredan atributos y métodos de ambas clases
    def __init__(self, mass, position, velocity): #constructor, se necesita los datos de la masa, posicion y velocidad
        color = random_color()
        size = int(mass ** (1/3) * 1)
        shape = random_shape()

        PhysicalProperties.__init__(self, mass, position, velocity) #por la herencia, se tienen que llamar los constructores de ambas clases para usar sus atributos
        GraphicalProperties.__init__(self, color, size, shape)
        self.moons = [] # agregacion, un planeta puede contener otras instancias de tipo moon (lunas)

    @classmethod #permite crear planetas a partir de un diccionario de configuración, cls es para planets y config es para el diccionario que contiene las distribuciones estadísticas para masa, posición y velocidad
    def from_config(cls, config):
        dist_cfg = config["planet"] #Se accede a la subclave "planet"

        mass_cfg = dist_cfg["mass"] #la masa se genere según una distribución normal
        if mass_cfg["type"] == "normal":
            mass = random.gauss(mass_cfg["mean"], mass_cfg["stddev"]) # media y desviación estándar
            mass = max(min(mass, mass_cfg["max"]), mass_cfg["min"]) 
        else:
            raise ValueError("Tipo de distribución de masa no soportado")

        pos_cfg = dist_cfg["position"] # posición aleatoria uniformemente distribuida dentro de un rectangulo definido por los valores mínimos y máximos en x, y
        if pos_cfg["type"] == "uniform":
            x = random.uniform(pos_cfg["x_min"], pos_cfg["x_max"])
            y = random.uniform(pos_cfg["y_min"], pos_cfg["y_max"])
        else:
            raise ValueError("Tipo de distribución de posición no soportado")
        position = Vector2D(x, y) #Se construyen objetos Vector2D para representar la posición

        vel_cfg = dist_cfg["velocity"] #Se genera un vector velocidad con componentes x,y también aleatorios 
        if vel_cfg["type"] == "uniform":
            vx = random.uniform(vel_cfg["vx_min"], vel_cfg["vx_max"])
            vy = random.uniform(vel_cfg["vy_min"], vel_cfg["vy_max"])
        else:
            raise ValueError("Tipo de distribución de velocidad no soportado")
        velocity = Vector2D(vx, vy) #Se construyen objetos Vector2D para representar la velocidad

        return cls(mass, position, velocity) 

    def add_moon(self, moon):  #Agregación, los planetas pueden contener lunas, que son objetos independientes referenciados por composicion
        self.moons.append(moon)

    def __str__(self): #aqui se aplica sobrecarga de metodos para personalizar la impresión de objetos 
        return f"Planeta - Masa: {self.mass}, Posición: {self.position}, Velocidad: {self.velocity}"

    def update(self, bodies, gravity, dt, screen_width=1200, screen_height=800): #colisiones contra los bordes de la pantalla, implementa la lógica de movimiento de los planetas y la interacción con sus lunas
        for moon in self.moons:
            dx = moon.position.x - self.position.x
            dy = moon.position.y - self.position.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            force = gravity * self.mass * moon.mass / (distance ** 2)
            fx = force * (dx / distance)
            fy = force * (dy / distance)
            moon._velocity = moon._velocity + Vector2D(fx / moon.mass, fy / moon.mass)

        self._position = self._position + self._velocity * dt

        if self._position.x - self.size < 0 or self._position.x + self.size > screen_width:
            self._velocity.x *= -1
            self._position.x = max(self.size, min(self._position.x, screen_width - self.size))

        if self._position.y - self.size < 0 or self._position.y + self.size > screen_height:
            self._velocity.y *= -1
            self._position.y = max(self.size, min(self._position.y, screen_height - self.size))


class Moon(PhysicalProperties, GraphicalProperties): #hereda las propiedades fisicas y graficas
    def __init__(self, mass, position, velocity, orbit_center: Planet): #constructor
        color = random_color()
        size = int(mass ** (1/3) * 1) #El tamaño es proporcional a la raíz cúbica de la masa m=ρV -> r^1/3	\propto m
        shape = random_shape()

        super().__init__(mass, position, velocity) #llama al constructor de la primera clase base, se usa super para respetar el orden en herencia múltiple
        GraphicalProperties.__init__(self, color, size, shape) #para llamar
        self.orbit_center = orbit_center

    def update(self, dt, gravity, bodies, screen_width=1200, screen_height=800): # actualiza la posición y velocidad de la luna
        dx = self.orbit_center.position.x - self.position.x
        dy = self.orbit_center.position.y - self.position.y
        distance = (dx ** 2 + dy ** 2) ** 0.5 #Se calcula la distancia entre la luna y su planeta.
        # se calcula la descomposición vectorial de la fuerza en x,y
        force = gravity * self.mass * self.orbit_center.mass / (distance ** 2)
        fx = force * (dx / distance)
        fy = force * (dy / distance)
        self._velocity = self._velocity + Vector2D(fx / self.mass, fy / self.mass) #2da ley de newton
        self._position = self._position + self._velocity * dt

        if self._position.x - self.size < 0 or self._position.x + self.size > screen_width: #Si la luna choca contra un borde lateral, rebota
            self._velocity.x *= -1
            self._position.x = max(self.size, min(self._position.x, screen_width - self.size))

        if self._position.y - self.size < 0 or self._position.y + self.size > screen_height:
            self._velocity.y *= -1
            self._position.y = max(self.size, min(self._position.y, screen_height - self.size))


# Función  para usar en multiproceso
def update_planet_data(args): # actualiza simultáneamente un planeta y todas sus lunas
    planet, bodies, gravity, dt, width, height = args
    planet.update(bodies, gravity, dt, width, height)
    for moon in planet.moons: #Itera sobre todas las lunas del planeta y las actualiza
        moon.update(dt, gravity, bodies, width, height)
    return planet #Devuelve el planeta con su nuevo estado, es para procesos en paralelo
