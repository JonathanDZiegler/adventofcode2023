import os
import time
from itertools import combinations

import numpy as np

from helpers import load


def extract_line(line: str, dims: int = 2) -> np.array:
    x, dx = line.split("@")
    x = np.array(tuple(int(c) for c in x.split(",")), dtype=float)[:dims]
    dx = np.array(tuple(int(c) for c in dx.split(",")), dtype=float)[:dims]
    return x, dx


def intersect(f: tuple[np.array], g: tuple[np.array], area: tuple[int], dims: int = 2):
    a = [[p, -q] for p, q in zip(f[1], g[1])]
    b = [q - p for p, q in zip(f[0], g[0])]
    try:
        x = np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        return False

    area = np.tile(np.array(area), (dims, 1)).T
    return (
        all(x > 0)
        and np.all(area[0] <= f[0] + x[0] * f[1])
        and np.all(f[0] + x[0] * f[1] <= area[1])
    )


def solve(part: int):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    points = [extract_line(line) for line in data]
    res = [
        intersect(*points, area=(200000000000000, 400000000000000), dims=2)
        for points in combinations(points, 2)
    ]
    print(f"Result part 1: {sum(res)}")


if __name__ == "__main__":
    start = time.perf_counter()
    solve(1)
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
    # solve(2)
    stop = time.perf_counter()
    print(f"Computation time for part 2: {1000*(stop-intermediate):0.3f} milliseconds.")
