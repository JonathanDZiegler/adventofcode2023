import os
import time
from itertools import combinations

import networkx as nx
import numpy as np
from tqdm import tqdm

from helpers import load


# works but is prohibitively slow. Upper bound of 32h for my example
def brute_force(g: nx.Graph) -> int:
    for i in tqdm(list(combinations(list(g.edges()), 2))):
        tmp_graph = g.copy()
        tmp_graph.remove_edges_from(list(i))
        if nx.has_bridges(tmp_graph):
            tmp_graph.remove_edges_from(nx.bridges(tmp_graph))
            # if len(list(nx.connected_components(tmp_graph))) == 2:
            break
    return np.prod([len(i) for i in nx.connected_components(tmp_graph)])


def solve():
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    g = nx.Graph()
    for line in data:
        start_node, end_nodes = line.split(": ")
        for end_node in end_nodes.split(" "):
            g.add_edges_from([(start_node, end_node)])

    res = nx.algorithms.connectivity.stoerwagner.stoer_wagner(g)[1]
    res = np.prod([len(i) for i in res])

    print(f"Result part 1: {res}")


if __name__ == "__main__":
    start = time.perf_counter()
    solve()
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
