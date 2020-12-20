import numpy as np
from math import pi, e, log


# main planets, stars and satellites class
class CelestialBody:
    def __init__(self, start_array, time_step, scale):
        self.x = np.array([start_array[0]])
        self.y = np.array([start_array[1]])
        self.z = np.array([start_array[2]])
        self.speed_x = start_array[3]
        self.speed_y = start_array[4]
        self.speed_z = start_array[5]
        self.mass = start_array[6]
        self.size = (4 * pi * (start_array[7] / (scale ** 0.73)) ** 3) / 3
        self.name = start_array[8]
        self.color = start_array[9]
        self.gravity = 6.6743015e-11
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0
        self.time_step = time_step
        if start_array[-1] == 'visible':
            self.visible = True
        else:
            self.visible = False

    def __add__(self, other):
        radius = ((self.x[-1] - other.x[-1]) ** 2 + (self.y[-1] - other.y[-1]) ** 2 +
                  (self.z[-1] - other.z[-1]) ** 2) ** 0.5
        self.a_x -= (self.gravity * other.mass * (self.x[-1] - other.x[-1])) / radius ** 3
        other.a_x -= (self.gravity * self.mass * (other.x[-1] - self.x[-1])) / radius ** 3
        self.a_y -= (self.gravity * other.mass * (self.y[-1] - other.y[-1])) / radius ** 3
        other.a_y -= (self.gravity * self.mass * (other.y[-1] - self.y[-1])) / radius ** 3
        self.a_z -= (self.gravity * other.mass * (self.z[-1] - other.z[-1])) / radius ** 3
        other.a_z -= (self.gravity * self.mass * (other.z[-1] - self.z[-1])) / radius ** 3
        return None

    # solution a differential equation by method Euler
    def move(self):
        self.x = np.append(self.x, self.x[-1] + self.time_step * self.speed_x)
        self.y = np.append(self.y, self.y[-1] + self.time_step * self.speed_y)
        self.z = np.append(self.z, self.z[-1] + self.time_step * self.speed_z)
        self.speed_x += self.time_step * self.a_x
        self.speed_y += self.time_step * self.a_y
        self.speed_z += self.time_step * self.a_z
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0

    def max_coord(self):
        if self.visible:
            return max(self.x.max(initial=0), self.y.max(initial=0), self.z.max(initial=0),
                       2 * (0.75 * self.size / pi) ** (1/3))
        else:
            return 0


class Planet(CelestialBody):
    def draw(self, ax):
        ax.plot(self.x, self.y, self.z, c=self.color, label=self.name)
        ax.scatter(self.x[-1], self.y[-1], self.z[-1], c=self.color, marker="o", s=self.size)

    def draw_ring(self):
        pass


class Star(CelestialBody):
    def __init__(self, start_array, time_step, scale):
        super().__init__(start_array, time_step, scale)
        self.lumino = round(3.86e26 * (1.989e30 / self.mass) ** 4)

    def draw(self, ax):
        ax.plot(self.x, self.y, self.z, c=self.color, label=self.name)
        ax.scatter(self.x[-1], self.y[-1], self.z[-1], c=self.color, marker="o", s=self.size,
                   alpha=0.9)
        for i in range(1, self.lumino // 2):
            factor = log(1.05 * i, e)
            ax.scatter(self.x[-1], self.y[-1], self.z[-1], c=self.color, marker="o", s=self.size * factor,
                       alpha=0.4 / (factor + 1))
            if 0.4 / (factor + 2) < 0.1:
                break


class Satellite(CelestialBody):
    def draw(self, ax):
        ax.plot(self.x, self.y, self.z, c=self.color, label=self.name)
        ax.scatter(self.x[-1], self.y[-1], self.z[-1], c=self.color, marker="o", s=self.size)


class BlackHole(CelestialBody):
    def __init__(self, start_array, time_step, scale):
        super().__init__(start_array, time_step, scale)
        value = (2 * self.gravity * self.mass) / (299792458 ** 2)
        radius = (0.75 * value / pi) ** (1/3)
        self.size = (4 * pi * (radius / (scale ** 0.73)) ** 3) / 3
        self.corruption = round(3.86e26 * (1.989e30 / self.mass) ** 4)

    def draw(self, ax):
        ax.plot(self.x, self.y, self.z, c=self.color, label=self.name)
        for i in range(1, self.corruption // 2):
            factor = log(1.05 * i, e)
            ax.scatter(self.x[-1], self.y[-1], self.z[-1], c=self.color, marker="o", s=self.size * factor,
                       alpha=0.35 / (factor + 0.8))
            if 0.4 / (factor + 2) < 0.1:
                break
        ax.scatter(self.x[-1], self.y[-1], self.z[-1], c='black', marker="o", s=self.size, alpha=1)
