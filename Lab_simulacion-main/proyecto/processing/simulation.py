import pygame
import yaml
import random
from processing.objects import Planet
import os #accede a funciones del sistema operativo para poder interactuar con el entorno de archivos

#La clase Simulation es el controlador del sistema, se lee la configuración desde YAML, crea y maneja los cuerpos celestes, sus interacciones y luego lo simula con pygame
class Simulation:
    def __init__(self):
#Se usa yaml para cargar la configuración al iniciar Simulation.py
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f) 

        self.width = self.config["simulation"]["screen_width"]
        self.height = self.config["simulation"]["screen_height"]
        self.num_bodies = self.config["simulation"]["num_bodies"]
        self.gravity_constant = self.config["simulation"]["gravity_constant"]
        self.time_step = self.config["simulation"]["time_step"]
        self.enable_merging = self.config["collisions"]["enable_merging"]

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulación Gravitacional")
        #self.bodies contiene una lista de instancias, aqui se aplica agregacion
        self.bodies = self.create_bodies()

    def create_bodies(self):
        return [Planet.from_config(self.config) for _ in range(self.num_bodies)]
#Se usa Vector2D en merge_bodies para conservar masa y momento
    def merge_bodies(self, body1, body2):
        total_mass = body1.mass + body2.mass
    
    # Centro de masa usando Vector2D, 
        new_position = (body1.position * body1.mass + body2.position * body2.mass) * (1/total_mass)
    
    # Conservación de momento usando Vector2D
        new_velocity = (body1.velocity * body1.mass + body2.velocity * body2.mass) * (1/total_mass)
    
        new_color = [(c1 + c2) // 2 for c1, c2 in zip(body1.color, body2.color)]
        new_size = int(max(body1.size, body2.size) * 1.1)
    
        return Planet(total_mass, new_position, new_velocity)

    def handle_collisions(self):
        new_bodies = []
        skip = set()

        for i, body1 in enumerate(self.bodies):
            if i in skip:
                continue
            merged = False
            for j, body2 in enumerate(self.bodies):
                if i == j or j in skip:
                    continue
                # Usar las propiedades position.x y position.y directamente
                dx = body1.position.x - body2.position.x
                dy = body1.position.y - body2.position.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < (body1.size + body2.size):  # Colisión
                    if self.enable_merging:
                        new_body = self.merge_bodies(body1, body2)
                        new_bodies.append(new_body)
                        skip.update([i, j])
                        merged = True
                        break
            if not merged:
                new_bodies.append(body1)

        self.bodies = new_bodies

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for body in self.bodies:
                body.update(self.bodies, self.gravity_constant, self.time_step)
                body.draw(self.screen)

            if self.enable_merging:
                self.handle_collisions()

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

