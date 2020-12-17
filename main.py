from numpy import array
import matplotlib.pyplot as plt
import planets


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


if __name__ == '__main__':
    # open .csv file with start value
    answer = input('Usage the ready data sets?(y or n) ')
    if answer == 'y':
        num_set = input('Write the number of data set: ')
        try:
            start_input = open_csv(f'data/set_{num_set}.csv')
        except FileNotFoundError:
            raise FileNotFoundError('no such data set, please try another file')
    else:
        start_input = open_csv('input.csv')
    # init time step
    max_time = float(input('Write the time of motion: '))
    if max_time * 5e-5 <= 100:
        time_step = max_time * 5e-5
    else:
        time_step = 100
    print(f'Time step: {time_step}')
    # init planets
    planets = array([planets.Planet(inp, time_step) for inp in start_input])

    for i in range(1, int(max_time // time_step) + 1):
        ignored_names = set()
        # count acceleration for planets
        for planet1 in planets:
            for planet2 in planets:
                if planet1.name != planet2.name and planet1.name not in ignored_names and planet2 not in ignored_names:
                    err = planet1 + planet2
            ignored_names.add(planet1.name)

        for planet in planets:
            planet.move()

    lim_max = max([planet.max_coord() for planet in planets])
    lim_min = min([planet.min_coord() for planet in planets])

    fig_3D = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('X', c='r')
    ax.set_ylabel('Y', c='r')
    ax.set_zlabel('Z', c='r')
    ax.set_title('Celestial Bodies Motion Simulator (CBM Simulator)\nbuild v0.0.2', c='purple')
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
