import random
#aqui nada mas se usa para manejar los vectores 

#se tiene un vector 2D con coordenadas x e y, mas que todo es para realizar operaciones entre vectores 
class Vector2D:
    ##aqui se crea un constructor el cual crea un vector con coordenadas (x,y), que se convierten en flotantes
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
#permite sumar vectores
    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return NotImplemented
#permite multiplicar por un escalar
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)
#texto
    def __str__(self):
        return f"({self.x}, {self.y})"
#interpreta el vector como si fuera una tupla, x,y=v
    def __iter__(self):
        yield self.x
        yield self.y

    def as_tuple(self):
        return (self.x, self.y)
#nos da una tupla RGB aleatoria
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def random_shape():
    return random.choice(["circle", "square", "triangle"])
