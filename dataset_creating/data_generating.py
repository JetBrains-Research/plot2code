import numpy as np
import matplotlib.pyplot as plt
import random
import json
from extracting_data import show_artists, get_boxes_coordinates, get_bbox_coordinates


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def labels_generator(length):
    alphabet = "abcdefghijklmnopqrstuvwxyz123456789"
    return ''.join(random.sample(alphabet, length))


def poly_generator(c, x):
    c = c[::-1]
    return sum(np.array([c[i] * x ** i for i in range(len(c))]))


def create_json_of_graph(fig, ax, input_data, artists):
    print(input_data)
    return json.dumps(
        {**input_data, **get_boxes_coordinates(fig, ax, artists)},
        cls=NpEncoder
    )


def generate_graphs(
        number_of_graphs=5,
        scatter_threshold=0.8,
        plot_artists_positions=False
):
    figsize = np.random.randint(4, 8, 2)
    x_locations = ['left', 'center', 'right']
    y_locations = ['bottom', 'center', 'top']

    fig, ax = plt.subplots(figsize=figsize)
    length_min, length_max = 4, 12
    fontsize_min, fontsize_max = 10, 20

    label_length = np.random.randint(length_min, length_max, 3)
    label_fontsize = np.random.randint(fontsize_min, fontsize_max, 3)
    xlabel_location = np.random.randint(0, 2, 2)
    ylabel_location = np.random.randint(0, 2)

    xlabel = labels_generator(label_length[0])
    xla = ax.set_xlabel(xlabel,
                        fontsize=label_fontsize[0], loc=x_locations[xlabel_location[0]])
    ylabel = labels_generator(label_length[1])
    yla = ax.set_ylabel(ylabel,
                        fontsize=label_fontsize[1], loc=y_locations[ylabel_location])
    ttl = labels_generator(label_length[2])
    title = ax.set_title(ttl,
                         fontsize=label_fontsize[2], loc=x_locations[xlabel_location[1]])

    tp = np.random.random(number_of_graphs)
    max_x, max_y = 100, 100
    min_points, max_points = 10, 100
    scattering_min_points, scattering_max_points = (5, 40)
    min_size, max_size = 5, 30
    min_deg, max_deg = 1, 4

    x_factor = np.random.randint(1, max_x)

    for i in range(number_of_graphs):
        n = np.random.randint(min_points, max_points)
        deg = np.random.randint(min_deg, max_deg)
        x = np.random.rand(n)
        y = np.random.rand(n)

        coefs = np.polyfit(x, y, deg=deg)
        y_factor = np.random.rand() * max_y

        if tp[i] >= scatter_threshold:
            number_of_points = np.random.randint(scattering_min_points, scattering_max_points)
            size = np.random.randint(min_size, max_size)

            x = np.linspace(0, 1, number_of_points)
            ax.scatter(x * x_factor, poly_generator(coefs, x) * y_factor,
                       s=size, label=f'scatter {i}')

        else:
            width = np.random.rand() * 4 + 1

            x = np.linspace(0, 1, 100)
            ax.plot(x * x_factor, poly_generator(coefs, x) * y_factor,
                    linewidth=width, label=f'line {i}')

    legend_location = np.random.randint(1, 10)
    lgd = ax.legend(loc=legend_location)
    artists = {
        'xlabel': xla,
        'ylabel': yla,
        'title': title,
        'legend': lgd
    }
    bbox_points = get_bbox_coordinates(fig, ax)
    fig.canvas.draw()

    if plot_artists_positions:
        fig, ax = show_artists(fig, ax, artists)
        for point in bbox_points:
            ax.scatter(
                *point, color='b', s=100, alpha=0.5,
                transform=fig.transFigure, clip_on=False
            )

    input_data = {
        'number_of_graphs': number_of_graphs,
        'figsize': figsize,
        'xlabel': (xlabel, label_fontsize[0]),
        'ylabel': (ylabel, label_fontsize[1]),
        'title': (ttl, label_fontsize[2]),
        'bbox_coordinates': bbox_points
    }

    json_data = create_json_of_graph(fig, ax, input_data, artists)

    return fig, ax, json_data
