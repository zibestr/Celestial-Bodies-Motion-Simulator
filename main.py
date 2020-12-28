from matplotlib.pyplot import figure, cm
from mpl_toolkits.mplot3d import Axes3D
from CelBodies import gravity_map, CelestialBody
from numpy import meshgrid, linspace, float64, zeros, arange
from threading import Thread
from time import time

version = 'build v.0.2.4'
start_time = time()


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


def max_distance(list_):
    result = 0
    for row_ in list_:
        if result < max(row_[0], row_[1], row_[2]) and row_[-1] == 'visible':
            result = max(row_[0], row_[1], row_[2])
    return result


def set_dark(fig, ax):
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))


def draw_result(array, fig):
    global version
    lim_max = max([elem.max_coord() for elem in array])
    lim_min = -lim_max

    ax = Axes3D(fig)

    ax.set_title(f'Celestial Bodies Motion Simulator (CBM Simulator)\n{version}', c='lightblue')

    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_zlim(lim_min, lim_max)

    fig.set_size_inches(16, 10)

    set_dark(fig, ax)

    for elem in array:
        if elem.visible:
            elem.draw(ax)
    ax.legend()

    fig.savefig('result.png', bbox_inches='tight', dpi=100)


def draw_gravity_field(array, fig):
    global version
    lim_max = max([elem.max_coord() for elem in array])
    lim_min = -lim_max

    x_potential, y_potential = meshgrid(linspace(lim_min * 1.5, lim_max * 1.5, 3500),
                                        linspace(lim_min * 1.5, lim_max * 1.5, 3500))
    potential = zeros((3500, 3500), dtype=float64)

    ax = Axes3D(fig)
    ax.set_title(f'Celestial Bodies Motion Simulator (CBM Simulator)\n{version}\nGravity Field',
                 c='lightblue')
    fig.set_size_inches(16, 10)
    set_dark(fig, ax)

    for elem in array:
        if elem.visible:
            potential += gravity_map(x_potential, y_potential, elem.x[-1], elem.y[-1], elem.z[-1],
                                     elem.option_relative())

    ax.plot_surface(x_potential, y_potential, potential, cmap=cm.inferno_r)

    fig.savefig('gravity.png', bbox_inches='tight', dpi=100)


def draw_time_graphic(time_array, fig):
    ax = fig.add_subplot()
    ax.plot(time_array[0], time_array[1])

    fig.set_size_inches(16, 10)
    fig.savefig('times.png', bbox_inches='tight', dpi=100)


def start_threads(threads_list):
    for thread in threads_list:
        thread.start()


def wait_stop(threads_list):
    for thread in threads_list:
        thread.join()


def main():
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
    count_steps = int(float(input('Write the count of time steps: ')))
    '''times = zeros((2, count_steps))
    times[0] = arange(1, count_steps + 1, 1)'''
    time_step = 1500
    # init celestial bodies
    celestial_bodies = list()
    for inp in start_input:
        celestial_bodies.append(CelestialBody(time_step, inp[6], coords=(inp[0], inp[1], inp[2]),
                                              speeds=(inp[3], inp[4], inp[5]), visible=inp[9], name=inp[7],
                                              color=inp[8]))

    # mainloop for computing trajectory
    for i in range(0, count_steps):
        # count acceleration for celestial_bodies
        time_start_turn = time()
        threads_matrix = [[]]
        for body1 in celestial_bodies:
            threads_matrix.append([Thread(target=body1.__add__, args=(body2,)) for body2 in
                                   celestial_bodies if body1.name != body2.name])
        for row in threads_matrix:
            start_threads(row)
        for row in threads_matrix:
            wait_stop(row)

        layer_interaction = list()
        for body in celestial_bodies:
            layer_interaction.append(Thread(target=body.move, args=()))
        start_threads(layer_interaction)
        wait_stop(layer_interaction)

        # times[1, i] = (time() - time_start_turn) * 1000
        print(f'Complete {i + 1} step of {count_steps} steps for time: {(time() - time_start_turn) * 1000} ms')
    print(f'Model time: {count_steps * time_step} s')
    print(f'Complete for {time() - start_time} s')

    fig1, fig2 = figure(), figure()

    threads = [Thread(target=draw_result, args=(celestial_bodies, fig1,)),
               Thread(target=draw_gravity_field, args=(celestial_bodies, fig2,))]
    # Thread(target=draw_time_graphic, args=(times, fig3,))]

    start_threads(threads)


if __name__ == '__main__':
    main()
