from helpers import load
import os
import time
import numpy as np
from typing import Literal
import sys

sys.setrecursionlimit(100000)

Direction = Literal["U", "D", "L", "R"]
Coordinate = tuple[int, int]


def addpos(pos: tuple, dir: tuple):
    return (pos[0] + dir[0], pos[1] + dir[1])


def solve(part: int):
    dirmap = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

    def check_map(digmap: np.array, pos: Coordinate) -> Coordinate:
        """Expand map if position is out of bounds, modify pos variable to still be poitning to the same field.

        Args:
            pos: Tuple of row and column coordinates of the current position.
        Returns:
            None - map is modified inplace
        """
        if pos[0] < 0 or pos[1] < 0:
            digmap = np.pad(
                digmap,
                (abs(min(0, pos[0])), abs(min(0, pos[1]))),
                constant_values=".",
            )
            pos = (pos[0] + abs(min(0, pos[0])), pos[1] + abs(min(0, pos[1])))
        elif pos[0] >= digmap.shape[0] or pos[1] >= digmap.shape[1]:
            digmap = np.pad(
                digmap,
                (
                    (0, max(0, pos[0] - digmap.shape[0] + 1)),
                    (0, max(0, pos[1] - digmap.shape[1] + 1)),
                ),
                constant_values=".",
            )
        return digmap, pos

    def dig(digmap: np.array, pos: Coordinate, instructions: str) -> Coordinate:
        direction, steps, color = instructions.split()
        for _ in range(int(steps)):
            pos = addpos(pos, dirmap[direction])
            digmap, pos = check_map(digmap, pos)
            digmap[pos] = color[1:-1]
        return digmap, pos

    def fill(
        pos: Coordinate = (1, 1), val: str = "0", empty_val: str = "."
    ) -> np.array:
        """Flood fill algoithm to change all points within the perimeter to a constant value ("0").

        Returns:
            The map with values filled in
        """
        if (
            any([p < 0 for p in pos])
            or pos[0] >= bool_digmap.shape[0]
            or pos[1] >= bool_digmap.shape[1]
            or bool_digmap[pos] != empty_val
        ):
            return
        else:
            bool_digmap[pos] = val
            fill(addpos(pos, (0, 1)), val, empty_val)
            fill(addpos(pos, (1, 0)), val, empty_val)
            fill(addpos(pos, (0, -1)), val, empty_val)
            fill(addpos(pos, (-1, 0)), val, empty_val)

    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    starting_sz = int(data[0].split()[1])
    digmap = np.full((starting_sz, starting_sz), ".", dtype="U7")
    pos = (0, 0)
    digmap[pos] = data[0].split()[2][1:-1]
    for l in data:
        digmap, pos = dig(digmap, pos, l)

    row, col = np.where(digmap != ".")
    row = max(np.where(digmap != ".")[0]) - min(np.where(digmap != ".")[0]) // 2
    row = max(np.where(digmap != ".")[0]) - min(np.where(digmap != ".")[0]) // 2
    row, col = np.where(digmap != ".")
    bool_digmap = digmap != "."
    fill((min(row) + 1, min(col) + 1), True, False)
    print(f"Result for part 1: {digmap.sum()}")


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
