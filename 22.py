import os
import time

import numpy as np
from matplotlib import colormaps
from matplotlib.colors import to_rgba

from helpers import load


def populate_element_grid(element_grid: np.array, piece_id: int, line: str):
    """Take information from the variable line which represents 2 three-dimensional coordinates separated by a ~
    and populate the element_grid tensor with all elements spanned by the two coordinates with the value of val.
    """
    p1, p2 = line.split("~")
    p1 = [int(c) for c in p1.split(",")]
    p2 = [int(c) for c in p2.split(",")]

    # fill positions in map between p1 and p2
    for x in range(p1[0], p2[0] + 1):
        for y in range(p1[1], p2[1] + 1):
            for z in range(p1[2], p2[2] + 1):
                if any(
                    dim >= shape for shape, dim in zip(element_grid.shape, [x, y, z])
                ):
                    element_grid = np.pad(
                        element_grid,
                        tuple(
                            (0, max(0, dim - element_grid.shape[idx] + 1))
                            for idx, dim in enumerate([x, y, z])
                        ),
                    )
                element_grid[x, y, z] = piece_id
    return element_grid


def fall(element_grid: np.array):
    """Move down all parts indicated with increasing integer numbers in the element_grid down vertically
    until they either touch another piece below them or the ground at [:,:,0].
    """
    out = np.zeros_like(element_grid)
    out[:, :, 0] = -1
    for piece_id in range(1, element_grid.max() + 1):
        piece = element_grid == piece_id
        while not any(out[piece] != 0):
            piece = np.roll(piece, -1, axis=2)
        piece = np.roll(piece, 1, axis=2)
        out += piece.astype(int) * piece_id
    return out


def is_supporting(element_grid, id) -> dict:
    piece = element_grid == id
    space_above = np.roll(piece, 1, axis=2)
    return tuple(a for a in np.unique(element_grid[space_above]) if a not in [0, id])


def check_values_match(dictionary, key):
    target_values = list(dictionary[key])

    for other_key, other_values in dictionary.items():
        if key != other_key:
            if len(target_values) == 0:
                return True
            # Check if all values of the target key appear in the values of other keys
            remove = []
            for value in target_values:
                if value in other_values:
                    remove.append(value)
            [target_values.remove(i) for i in remove]

    return len(target_values) == 0


def is_safe(supports: dict) -> list[bool]:
    return [check_values_match(supports, i) for i in range(1, max(supports.keys()) + 1)]


def show(element_grid, name: str):
    import matplotlib.pyplot as plt

    cmap = plt.colormaps["viridis"]
    num_colors = element_grid.max() + 1
    colors_list = [cmap(i, alpha=0.6) for i in np.linspace(0, 255, num_colors)]
    colors = np.zeros(list(element_grid.shape) + [4], dtype=float)
    for i in range(element_grid.max() + 1):
        colors[element_grid == i] = colors_list[i]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.voxels(element_grid, facecolors=colors, edgecolors="grey")
    plt.savefig(name)


def solve(part: int):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    element_grid = np.zeros((1, 1, 1), dtype=int)
    for idx, line in enumerate(data):
        element_grid = populate_element_grid(element_grid, idx + 1, line)
    element_grid[:, :, 0] = -1

    # show(element_grid, "hover.png")

    element_grid = fall(element_grid)
    # show(element_grid, "fallen.png")
    supports = {
        i: is_supporting(element_grid, i) for i in range(1, element_grid.max() + 1)
    }
    res = is_safe(supports)
    print(f"Answer to part 1: {sum(res)}")


if __name__ == "__main__":
    start = time.perf_counter()
    solve(1)
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
