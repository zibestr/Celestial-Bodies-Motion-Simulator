import matplotlib.pyplot as plt
import planets


def open_csv(file_name):
    result = list()
    file = open(file_name, 'r', encoding='utf-8')
    for line in file:
        result.append([*[float(value) for value in line.split(', ')[:8]],
                       *[value for value in line.split(', ')[8:]]])
        if result[-1][-1][-1:] == '\n':
            result[-1][-1] = result[-1][-1][:-1]
    file.close()
    return result


def max_num(list_):
    result = 1
    for row in list_:
        if result < max([abs(elem) for elem in row[:3]]) and row[-1] == 'visible':
            result = max([abs(elem) for elem in row[:3]])
    return result


def set_dark():
    fig_3D.set_facecolor('black')
    ax.set_facecolor('black')
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))


if __name__ == '__main__':
    # open .csv file with start value
    answer = input('Usage the ready data sets?(y or n) ').lower()
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
    # init celestial bodies
    celestial_bodies = list()
    scale = max_num(start_input)
    for inp in start_input:
        if inp[-2] == 'star':
            celestial_bodies.append(planets.Star(inp, time_step, scale))
        elif inp[-2] == 'blackhole':
            celestial_bodies.append(planets.BlackHole(inp, time_step, scale))
        elif inp[-2] == 'satellite':
            celestial_bodies.append(planets.Satellite(inp, time_step, scale))
        elif inp[-2] == 'planet':
            celestial_bodies.append(planets.Planet(inp, time_step, scale))

    for i in range(1, int(max_time // time_step) + 1):
        ignored_names = set()
        # count acceleration for celestial_bodies
        for body1 in celestial_bodies:
            for body2 in celestial_bodies:
                if body1.name != body2.name and body1.name not in ignored_names and body2 not in ignored_names:
                    body1.__add__(body2)
            ignored_names.add(body1.name)

        for body in celestial_bodies:
            body.move()

    lim_max = max([body.max_coord() for body in celestial_bodies])
    lim_min = -lim_max

    fig_3D = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title('Celestial Bodies Motion Simulator (CBM Simulator)\nbuild v0.0.5', c='lightblue')
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_zlim(lim_min, lim_max)

    fig_3D.set_size_inches(16, 10)
    fig_3D.tight_layout()
    set_dark()

    for body in celestial_bodies:
        if body.visible:
            body.draw(ax)
    ax.legend()

    fig_3D.savefig('result.png', bbox_inches='tight', dpi=100)
