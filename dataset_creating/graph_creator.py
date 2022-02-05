import numpy as np
import matplotlib.pyplot as plt
import json
import random
from extracting_data import show_artists, get_boxes_coordinates, get_bbox_coordinates
from dataclasses import dataclass


@dataclass
class ScatterPlotParameters:
    pass


@dataclass
class LinePlotParameters:
    pass


@dataclass
class GraphParameters:
    figsize: tuple
    xlabel_length: int
    ylabel_length: int
    title_length: int
    xlabel_location: int
    ylabel_location: int
    title_location: int
    xlabel_fontsize: int
    ylabel_fontsize: int
    title_fontsize: int
    types_of_graphs: list
    x_factor_min: float
    x_factor_max: float
    y_factor_min: float
    y_factor_max: float
    points_min: int
    points_max: int
    deg_min: int
    deg_max: int
    scatter_plot_threshold: float
    scattering_points_min: int
    scattering_points_max: int


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class GraphSynthetic:
    x_locations = ['left', 'center', 'right']
    y_locations = ['bottom', 'center', 'top']
    title_locations = x_locations

    def __init__(self, config):
        self.parameters = self.generate_random_parameters(config)
        self.label_generator = self.create_random_name
        self.fig, self.ax = None, None

    @staticmethod
    def generate_random_parameters(config):
        figsize_min, figsize_max = config['figsize_boundaries']
        text_length_min, text_length_max = config['text_length_boundaries']
        fontsize_min, fontsize_max = config['fontsize_boundaries']
        number_of_graphs = config['number_of_graphs']
        scatter_plot_threshold = config['scatter_plot_threshold']
        x_factor_min, x_factor_max = config['x_factor_boundaries']
        y_factor_min, y_factor_max = config['y_factor_boundaries']
        points_min, points_max = config['points_boundaries']
        scattering_points_min, scattering_points_max = config['scattering_points_boundaries']
        deg_min, deg_max = config['deg_boundaries']

        figsize = tuple(np.random.randint(figsize_min, figsize_max, 2))
        xlabel_length, ylabel_length, title_length = np.random.randint(text_length_min, text_length_max, 3)
        xlabel_location, ylabel_location, title_location = np.random.randint(0, 2, 3)
        xlabel_fontsize, ylabel_fontsize, title_fontsize = np.random.randint(fontsize_min, fontsize_max, 3)
        types_of_graphs = np.random.random(number_of_graphs)

        parameters = GraphParameters(
            figsize,
            xlabel_length, ylabel_length, title_length,
            xlabel_location, ylabel_location, title_location,
            xlabel_fontsize, ylabel_fontsize, title_fontsize,
            types_of_graphs,
            x_factor_min, x_factor_max,
            y_factor_min, y_factor_max,
            points_min, points_max,
            deg_min, deg_max,
            scatter_plot_threshold, scattering_points_min, scattering_points_max,
        )

        return parameters

    @staticmethod
    def random_in_range(a, b, n=1):
        return (b - a) * np.random.random(n) + a

    @staticmethod
    def create_random_name(length):
        alphabet = "abcdefghijklmnopqrstuvwxyz123456789"
        return ''.join(random.sample(alphabet, length))

    @staticmethod
    def poly_generator(c, x):
        c = c[::-1]
        return sum(np.array([c[i] * x ** i for i in range(len(c))]))

    def generate_figure_and_axes(self, plot_artists_positions=False):
        fig, ax = plt.subplots(figsize=self.parameters.figsize)

        xlabel = self.label_generator(self.parameters.xlabel_length)
        xla = ax.set_xlabel(
            xlabel,
            fontsize=self.parameters.xlabel_fontsize,
            loc=self.x_locations[self.parameters.xlabel_location]
        )

        ylabel = self.label_generator(self.parameters.ylabel_length)
        yla = ax.set_ylabel(
            ylabel,
            fontsize=self.parameters.ylabel_fontsize,
            loc=self.y_locations[self.parameters.ylabel_location]
        )

        ttl = self.label_generator(self.parameters.title_length)
        title = ax.set_title(
            ttl,
            fontsize=self.parameters.title_fontsize,
            loc=self.title_locations[self.parameters.title_location]
        )

        x_factor = self.random_in_range(self.parameters.x_factor_min, self.parameters.x_factor_max)

        for i, graph_type in enumerate(self.parameters.types_of_graphs):
            n = np.random.randint(self.parameters.points_min, self.parameters.points_max)
            deg = np.random.randint(self.parameters.deg_min, self.parameters.deg_max)
            x = np.random.rand(n)
            y = np.random.rand(n)

            coefs = np.polyfit(x, y, deg=deg)
            y_factor = self.random_in_range(self.parameters.y_factor_min, self.parameters.y_factor_max)

            if graph_type >= self.parameters.scatter_plot_threshold:
                number_of_points = np.random.randint(
                    self.parameters.scattering_points_min, self.parameters.scattering_points_max
                )
                size = np.random.randint(10, 50)

                x = np.linspace(0, 1, number_of_points)
                ax.scatter(x * x_factor, self.poly_generator(coefs, x) * y_factor,
                           s=size, label=f'scatter {i}')

            else:
                width = np.random.rand() * 4 + 1

                x = np.linspace(0, 1, 100)
                ax.plot(x * x_factor, self.poly_generator(coefs, x) * y_factor,
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

        self.fig, self.ax = fig, ax
        return fig, ax
