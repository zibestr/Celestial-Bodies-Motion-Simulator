from math import sqrt, fsum
from random import randint
from numpy import sqrt as array_sqrt
from numpy import append as array_append
from numpy import array, zeros, float64


class CelestialBody:
    def __init__(self, clock, mass, coords=(0.0, 0.0, 0.0), speeds=(0.0, 0.0, 0.0), visible='visible',
                 name='Celestial Body', color=''):
        self.x = array([coords[0]], dtype=float64)
        self.y = array([coords[1]], dtype=float64)
        self.z = array([coords[2]], dtype=float64)
        self.speeds = array([speeds[0], speeds[1], speeds[2]], dtype=float64)
        self.gravity_option = mass * 6.6743015e-11
        self.clock_0, self.clock = clock, clock
        self.accelerations = zeros(3, dtype=float64)
        self.potential = 0
        self.mod_speed = fsum(self.speeds ** 2)
        self.visible = True if visible == 'visible' else False
        self.name = name
        self.color = color if color != '' else '#'+'%06x' % randint(0, 0xFFFFFF)

    def option_relative(self):
        return self.gravity_option / sqrt(1 - self.mod_speed / 89875517873681764)

    def __add__(self, other):
        radius_vector = sqrt(((self.x[-1] - other.x[-1]) ** 2 +
                              (self.y[-1] - other.y[-1]) ** 2 +
                              (self.z[-1] - other.z[-1]) ** 2))
        radius_vector_cube = radius_vector ** 3
        self.accelerations[0] += (other.option_relative() * (other.x[-1] - self.x[-1])) / radius_vector_cube
        self.accelerations[1] += (other.option_relative() * (other.y[-1] - self.y[-1])) / radius_vector_cube
        self.accelerations[2] += (other.option_relative() * (other.z[-1] - self.z[-1])) / radius_vector_cube

        self.potential += - self.option_relative() / radius_vector

        self.clock = self.clock_0 / sqrt(1 - (2 * self.potential) / 89875517873681764)

        return self.potential

    def move(self):
        self.x = array_append(self.x, self.x[-1] + self.speeds[0] * self.clock)
        self.y = array_append(self.y, self.y[-1] + self.speeds[1] * self.clock)
        self.z = array_append(self.z, self.z[-1] + self.speeds[2] * self.clock)
        self.speeds[0] += self.accelerations[0] * self.clock
        self.speeds[1] += self.accelerations[1] * self.clock
        self.speeds[2] += self.accelerations[2] * self.clock
        self.accelerations = zeros(3, dtype=float64)
        self.potential = 0

    def max_coord(self):
        if self.visible:
            return max(self.x.max(initial=0), self.y.max(initial=0), self.z.max(initial=0))
        else:
            return 0

    def draw(self, field):
        field.plot(self.x, self.y, self.z, c=self.color, label=self.name)
        field.scatter(self.x[-1], self.y[-1], self.z[-1], c=self.color, marker="o")


def gravity_map(X, Y, x_mass, y_mass, z_mass, gravity_option):
    return - gravity_option / array_sqrt((x_mass - X) ** 2 + (y_mass - Y) ** 2 + z_mass ** 2)


def generator(count, step=1, time_step=1, mass=1e10):
    list_ = list()
    for i in range(10, count + 10):
        list_.append(CelestialBody(time_step, mass=mass*(i ** 2),
                                   coords=((-1**i)*(i**((step**2)/i)), i**step, 0),
                                   name=f'Body {i-9}'))
    return list_
