from data_generating import generate_graphs
from graph_creator import GraphSynthetic
import json
import yaml

with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)


if __name__ == '__main__':
    print(config)
    g = GraphSynthetic(config)
    fig, ax = g.generate_figure_and_axes(plot_artists_positions=True)
    fig.savefig(f'test.png')
    fig.show()

    # n = 10
    # for i in range(n):
    #     fig, ax, json_data = generate_graphs()
    #     fig.savefig(f'../data/{i}.png')
    #     fig.show()
    #
    #     with open(f'../data/{i}.json', 'w') as f:
    #         json.dump(json_data, f)
