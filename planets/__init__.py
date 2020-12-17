import numpy as np


# main planets, stars and satellites class
class Planet:
    def __init__(self, start_array, time_step):
        self.x = np.array([start_array[0]])
        self.y = np.array([start_array[1]])
        self.z = np.array([start_array[2]])
        self.speed_x = start_array[3]
        self.speed_y = start_array[4]
        self.speed_z = start_array[5]
        self.mass = start_array[6]
        self.name = start_array[7]
        self.color = start_array[8]
        self.gravity = 6.6743015e-11
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0
        self.time_step = time_step
        if start_array[9] == 'visible':
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
        return 'error'

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
            return max(self.x.max(initial=0), self.y.max(initial=0), self.z.max(initial=0))
        else:
            return 0

    def min_coord(self):
        if self.visible:
            return min(self.x.min(initial=0), self.y.min(initial=0), self.z.min(initial=0))
        else:
            return 0
