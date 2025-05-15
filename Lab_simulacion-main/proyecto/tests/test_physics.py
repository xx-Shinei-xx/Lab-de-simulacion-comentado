import unittest
from processing.physics import Celestialbodies
from processing.objects import Planet
from processing.utils import Vector2D

class TestCelestialbodies(unittest.TestCase): #Se ejecuta antes de cada test

    def setUp(self):
        """ Configuración inicial para cada test """
        self.engine = Celestialbodies()
        self.planet1 = Planet(1000, Vector2D(50, 50), Vector2D(0, 0))
        self.planet2 = Planet(1000, Vector2D(60, 60), Vector2D(0, 0))
        self.engine.add_planet(self.planet1)  
        self.engine.add_planet(self.planet2)  

    def test_gravity_applied(self): #si sigue en 0, la gravedad no está funcionando
        """ Verifica que se aplique gravedad correctamente """
        self.engine.apply_gravity(1)  # Paso de tiempo de 1 segundo
        # Si la gravedad se aplica, las velocidades no deben seguir en 0
        self.assertNotEqual(self.planet1.velocity.x, 0)
        self.assertNotEqual(self.planet2.velocity.x, 0)

    def test_collision_handling(self): 
        """ Verifica que al manejar colisiones, se combine correctamente """
        self.engine.handle_collision(self.planet1, self.planet2)
        # Al combinarse, debería haber solo un planeta en la lista
        self.assertEqual(len(self.engine.planets), 1)
