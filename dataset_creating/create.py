from data_generating import generate_graphs
from graph_creator import GraphSynthetic
import json
import yaml
from pathlib import Path
from tqdm import tqdm

with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)


def create_dataset(n=10):
    for i in tqdm(range(n)):
        Path(f"../dataset/{i}").mkdir(parents=True, exist_ok=True)
        g = GraphSynthetic(config)
        fig, ax = g.generate_figure_and_axes(plot_artists_positions=False)
        fig.savefig(f'../dataset/{i}/{i}.png')

        with open(f'../dataset/{i}/{i}.json', 'w+') as f:
            json.dump(g.json_params, f)
    fig.show()


if __name__ == '__main__':
    create_dataset()
    # print(config)
    # g = GraphSynthetic(config)
    # fig, ax = g.generate_figure_and_axes(plot_artists_positions=True)
    # fig.savefig(f'test.png')
    # fig.show()

    # n = 10
    # for i in range(n):
    #     fig, ax, json_data = generate_graphs()
    #     fig.savefig(f'../data/{i}.png')
    #     fig.show()
    #
    #     with open(f'../data/{i}.json', 'w') as f:
    #         json.dump(json_data, f)
