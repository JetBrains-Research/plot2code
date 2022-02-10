import matplotlib.patches as patches
import numpy as np


def get_bbox_coordinates(fig, ax):
    p0, p1 = ax.bbox._bbox._points
    x0, y0 = p0
    x1, y1 = p1
    return [[x0, y0], [x0, y1], [x1, y0], [x1, y1]]


def get_title_coordinates(fig, ax, title):
    size = fig.get_size_inches() * fig.dpi
    bbox = title.get_window_extent(renderer=fig.canvas.get_renderer())
    pixels_coordinates = [(bbox.x0, bbox.y0), (bbox.x1, bbox.y1)]

    fig_coordinates = []
    for p in pixels_coordinates:
        x, y = p
        x /= size[0]
        y /= size[1]
        fig_coordinates.append((x, y))

    return fig_coordinates


def get_label_coordinates(fig, ax, label):
    size = fig.get_size_inches() * fig.dpi
    bbox = label.get_window_extent(renderer=fig.canvas.get_renderer())
    pixels_coordinates = [(bbox.x0, bbox.y0), (bbox.x1, bbox.y1)]

    fig_coordinates = []
    for p in pixels_coordinates:
        x, y = p
        x /= size[0]
        y /= size[1]
        fig_coordinates.append((x, y))

    return fig_coordinates


def add_bbox(fig, ax, coordinates, **kwargs):
    size = fig.get_size_inches() * fig.dpi
    p = coordinates
    rect = patches.Rectangle(
        (
            p[0][0],
            p[0][1]
        ),
        (p[1][0] - p[0][0]),
        (p[1][1] - p[0][1]),
        clip_on=False, transform=fig.transFigure, **kwargs)

    ax.add_patch(rect)
    return fig, ax


def get_tick_coordinates(fig, ax, tick):
    size = fig.get_size_inches() * fig.dpi
    text = tick.get_text()
    bbox = tick.get_window_extent(renderer=fig.canvas.get_renderer())
    pixels_coordinates = [(bbox.x0, bbox.y0), (bbox.x1, bbox.y1)]

    tick_coordinates = []
    for p in pixels_coordinates:
        x, y = p
        x /= size[0]
        y /= size[1]
        out = {
            'text': text,
            'coordinates': (x, y)
        }
        tick_coordinates.append(out)

    return tick_coordinates


def get_all_ticks_coordinates(fig, ax, ticks):
    res = []

    for tick in ticks:
        res.append(get_tick_coordinates(fig, ax, tick))

    return res


def get_legend_coordinates(fig, ax, legend):
    size = fig.get_size_inches() * fig.dpi
    bbox = legend.get_window_extent(renderer=fig.canvas.get_renderer())
    pixels_coordinates = [(bbox.x0, bbox.y0), (bbox.x1, bbox.y1)]

    fig_coordinates = []
    for p in pixels_coordinates:
        x, y = p
        x /= size[0]
        y /= size[1]
        fig_coordinates.append((x, y))

    return fig_coordinates


def get_boxes_coordinates(fig, ax, artists):
    title_coordinates = get_title_coordinates(fig, ax, artists['title'])

    xlabel_coordinates = get_label_coordinates(fig, ax, artists['xlabel'])

    ylabel_coordinates = get_label_coordinates(fig, ax, artists['ylabel'])

    ticks = [t for t in ax.get_xticklabels()][1:-1]
    ticks += [t for t in ax.get_yticklabels()][1:-1]
    ticks = get_all_ticks_coordinates(fig, ax, ticks)

    # for tick in ticks:
    #     p = [t['coordinates'] for t in tick]
    #     fig, ax = add_bbox(
    #         fig, ax, p,
    #         linewidth=1, edgecolor='magenta', facecolor='none'
    #     )

    legend_coordinates = get_legend_coordinates(fig, ax, artists['legend'])

    ticks = [
        {
            "text": tick[0]['text'],
            "coordinates": (tick[0]['coordinates'], tick[1]['coordinates'])
        }
        for tick in ticks
    ]
    boxes_coordinates = {
        'title_coordinates': title_coordinates,
        'xlabel_coordinates': xlabel_coordinates,
        'ylabel_coordinates': ylabel_coordinates,
        'ticks': ticks,
        'legend_coordinates': legend_coordinates
    }

    return boxes_coordinates


def get_ticks(fig, ax):
    """
    Get tiks values of x and y axes and
    positions of ticks in figure's coordinate system
    """

    ax_to_figure_transformation = ax.transAxes + ax.figure.transFigure.inverted()

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    xticks_pos = [(tick - x_min) / (x_max - x_min) for tick in ax.get_xticks()]
    yticks_pos = [(tick - y_min) / (y_max - y_min) for tick in ax.get_yticks()]

    crd_x = np.vstack((xticks_pos, np.zeros_like(xticks_pos))).T
    crd_y = np.vstack((np.zeros_like(yticks_pos), yticks_pos)).T

    xticks_pos = ax_to_figure_transformation.transform(crd_x)
    yticks_pos = ax_to_figure_transformation.transform(crd_y)

    coords = []

    width = max(
        ax.yaxis.get_ticklines()[1].get_markeredgewidth(),
        ax.xaxis.get_ticklines()[1].get_markeredgewidth()
    )
    height = max(
        ax.yaxis.get_ticklines()[1].get_markersize(),
        ax.xaxis.get_ticklines()[1].get_markersize()
    )
    bias = ax_to_figure_transformation.transform(
        ax.transAxes.inverted().transform(
            (max(width, height), 0)
        )
    )[0] * 1.5

    xticks_pos = [((p[0] - bias, p[1] - bias), (p[0] + bias, p[1] + bias)) for p in xticks_pos]
    yticks_pos = [((p[0] - bias, p[1] - bias), (p[0] + bias, p[1] + bias)) for p in yticks_pos]

    return ax.get_xticks()[1:-1], ax.get_yticks()[1:-1], xticks_pos[1:-1], yticks_pos[1:-1], coords


def show_artists(fig, ax, artists):

    p = get_title_coordinates(fig, ax, artists['title'])
    fig, ax = add_bbox(fig, ax, p,
                       linewidth=1, edgecolor='b', facecolor='none')

    p = get_label_coordinates(fig, ax, artists['xlabel'])
    fig, ax = add_bbox(fig, ax, p,
                       linewidth=1, edgecolor='g', facecolor='none')

    p = get_label_coordinates(fig, ax, artists['ylabel'])
    fig, ax = add_bbox(fig, ax, p,
                       linewidth=1, edgecolor='g', facecolor='none')

    ticks = [t for t in ax.get_xticklabels()][1:-1]
    ticks += [t for t in ax.get_yticklabels()][1:-1]
    ticks = get_all_ticks_coordinates(fig, ax, ticks)
    ticks = [
        {
            "text": tick[0]['text'],
            "coordinates": (tick[0]['coordinates'], tick[1]['coordinates'])
        }
        for tick in ticks
    ]

    for tick in ticks:
        p = tick['coordinates']
        fig, ax = add_bbox(
            fig, ax, p,
            linewidth=1, edgecolor='magenta', facecolor='none'
        )

    p = get_legend_coordinates(fig, ax, artists['legend'])
    fig, ax = add_bbox(
        fig, ax, p,
        linewidth=2, edgecolor='b', facecolor='none', zorder=10
    )

    return fig, ax