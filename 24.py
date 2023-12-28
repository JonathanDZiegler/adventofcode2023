import os
import time
from itertools import combinations

import numpy as np
from sympy import solve, symbols

from helpers import load


def extract_line(line: str, dims: int = 2) -> np.array:
    x, dx = line.split("@")
    x = np.array(tuple(int(c) for c in x.split(",")), dtype=float)[:dims]
    dx = np.array(tuple(int(c) for c in dx.split(",")), dtype=float)[:dims]
    return x, dx


def intersect(
    f: tuple[np.array], g: tuple[np.array], area: tuple[int], dims: int = 2
) -> bool:
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


def sym_3(c: str):
    return symbols(" ".join(f"{c}{i}" for i in range(3)))


def throw(trajectories: tuple[tuple[np.array]]) -> np.array:
    a = [elem[1] for elem in trajectories[:4]]
    b = [elem[0] for elem in trajectories[:4]]
    c, d = [sym_3(c) for c in ["c", "d"]]
    eqs = []
    t = symbols(" ".join(f"t{i}" for i in range(len(a))))
    for i in range(len(a)):
        eqs.extend(
            [a * t[i] + b - c * t[i] - d for a, b, c, d in zip(a[i], b[i], c, d)]
        )

    res = solve(
        eqs,
        list(c) + list(d) + list(t),
        dict=True,
    )[0]

    nums = list(res.values())
    c = np.array(nums[:3], dtype=int)
    d = np.array(nums[3:6], dtype=int)
    t = np.array(nums[6:], dtype=int)

    return d.sum()


def solve_1(points):
    res = [
        intersect(*points, area=(200000000000000, 400000000000000), dims=2)
        for points in combinations(points, 2)
    ]
    print(f"Result part 1: {sum(res)}")


def solve_2(points):
    res = throw(points)
    print(f"Result part 2: {res}")


if __name__ == "__main__":
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    start = time.perf_counter()
    solve_1([extract_line(line, dims=2) for line in data])
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
    solve_2([extract_line(line, dims=3) for line in data])
    stop = time.perf_counter()
    print(f"Computation time for part 2: {1000*(stop-intermediate):0.3f} milliseconds.")
