from numpy import array
from numpy import append as append_array
import matplotlib.pyplot as plt


# main planets, stars and satellites class
class Planet:
    def __init__(self, start_array):
        self.x = array([start_array[0]])
        self.y = array([start_array[1]])
        self.z = array([start_array[2]])
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

    # solution a differential equation by method Euler
    def move(self):
        global time_step
        self.x = append_array(self.x, self.x[-1] + time_step * self.speed_x)
        self.y = append_array(self.y, self.y[-1] + time_step * self.speed_y)
        self.z = append_array(self.z, self.z[-1] + time_step * self.speed_z)
        self.speed_x += time_step * self.a_x
        self.speed_y += time_step * self.a_y
        self.speed_z += time_step * self.a_z
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0

    def max_coord(self):
        return max(self.x.max(initial=0), self.y.max(initial=0), self.z.max(initial=0))

    def min_coord(self):
        return min(self.x.min(initial=0), self.y.min(initial=0), self.z.min(initial=0))


def open_csv(file_name):
    result = list()
    file = open(file_name, 'r', encoding='utf-8')
    for line in file:
        result.append([*[float(value) for value in line.split(', ')[:7]],
                       *[value for value in line.split(', ')[7:]]])
        if result[-1][-1][-1:] == '\n':
            result[-1][-1] = result[-1][-1][:-1]
    file.close()
    return result


start_input = open_csv('input.csv')
max_time = float(input())
if max_time * 5e-5 <= 100:
    time_step = max_time * 5e-5
else:
    time_step = 100
print(time_step)
# init planets
planets = array([Planet(inp) for inp in start_input])


for i in range(1, int(max_time // time_step) + 1):
    ignored_names = set()
    # count acceleration for planets
    for planet1 in planets:
        for planet2 in planets:
            if planet1.name != planet2.name and planet1.name not in ignored_names and planet2 not in ignored_names:
                planet1 + planet2
        ignored_names.add(planet1.name)

    for planet in planets:
        planet.move()

lim_max = max([planet.max_coord() for planet in planets if planet.visible])
lim_min = min([planet.min_coord() for planet in planets if planet.visible])

fig_3D = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('X', c='r')
ax.set_ylabel('Y', c='r')
ax.set_zlabel('Z', c='r')
ax.set_title('Celestial Bodies Motion Simulator (CBM Simulator)\nbuild v0.1.1', c='purple')
ax.set_xlim(lim_min, lim_max)
ax.set_ylim(lim_min, lim_max)
ax.set_zlim(lim_min, lim_max)

for planet in planets:
    if planet.visible:
        ax.plot(planet.x, planet.y, planet.z, c=planet.color, label=planet.name)
        ax.scatter(planet.x[-1], planet.y[-1], planet.z[-1], c=planet.color, marker="o")
ax.legend()

fig_3D.set_size_inches(16, 13)
fig_3D.savefig('result.png', bbox_inches='tight', dpi=100)
