import os
import sys
import time

import numpy as np

from helpers import load_str


def preprocess(data_path: os.PathLike) -> np.array:
    data = load_str(data_path)
    data = np.char.asarray(data)
    data = np.asarray(data.replace(".", "0").replace("#", "1"), dtype=bool)
    return data


def print_map(data):
    np.set_printoptions(threshold=sys.maxsize)
    print(
        np.char.asarray(data, unicode=True).replace("False", ".").replace("True", "#")
    )


def warp_space(starmap, warp_factor):
    spacemap = np.ones_like(starmap, dtype=int)
    for i in range(starmap.shape[0]):
        if not any(starmap[i, :]):
            spacemap[i, :] = warp_factor
    for i in range(starmap.shape[1]):
        if not any(starmap[:, i]):
            spacemap[:, i] = warp_factor
    return spacemap


def traverse_warped_space(points, spacemap):
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            y_dist = np.sum(
                spacemap[
                    min(points[i][0], points[j][0]) : max(points[i][0], points[j][0]),
                    points[i][1],
                ]
            )
            x_dist = np.sum(
                spacemap[
                    points[i][0],
                    min(points[i][1], points[j][1]) : max(points[i][1], points[j][1]),
                ]
            )
            distances.append(x_dist + y_dist)
    return distances


def solve(part: int):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = preprocess(data_path)
    points = np.argwhere(data)
    if part == 1:
        spacemap = warp_space(data, 2)
    elif part == 2:
        spacemap = warp_space(data, 1e6)

    distances = traverse_warped_space(points, spacemap)
    print(f"Sum of all distances is: {np.sum(distances)}.")


if __name__ == "__main__":
    start = time.perf_counter()
    solve(1)
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
    solve(2)
    stop = time.perf_counter()
    print(f"Computation time for part 2: {1000*(stop-intermediate):0.3f} milliseconds.")
