import unittest
from processing.objects import Planet, Moon
from processing.utils import Vector2D

class TestPlanet(unittest.TestCase):

    def test_initialization(self): #verifica que el planeta se inicialice correctamente
        planet = Planet(1000, Vector2D(50, 50), Vector2D(1, 1))
        self.assertEqual(planet.mass, 1000)
        self.assertEqual(planet.position.x, 50)
        self.assertEqual(planet.position.y, 50)

    def test_add_moon(self): #confirma que el método add_moon() funciona y añade correctamente la luna al planeta
        planet = Planet(1000, Vector2D(50, 50), Vector2D(1, 1))
        moon = Moon(10, Vector2D(60, 60), Vector2D(0, 0), planet)
        planet.add_moon(moon)
        self.assertIn(moon, planet.moons)

class TestMoon(unittest.TestCase): #la luna se inicialice con masa, posición, velocidad y referencia al planeta

    def test_initialization(self):
        moon = Moon(10, Vector2D(60, 60), Vector2D(0, 0), None)
        self.assertEqual(moon.mass, 10)
        self.assertEqual(moon.position.x, 60)
        self.assertEqual(moon.position.y, 60)