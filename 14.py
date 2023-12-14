from helpers import load_str
import os
import time
import numpy as np
from typing import Literal
from dataclasses import dataclass
from tqdm import tqdm
from itertools import cycle
from collections import OrderedDict


@dataclass
class Point:
    y: int
    x: int

    def __str__(self):
        return "({0},{1})".format(self.y, self.x)

    def __add__(self, other):
        y = self.y + other.y
        x = self.x + other.x
        return Point(y, x)

    def check_bounds(self, top: tuple[int, int]):
        return self.x < 0 or self.y < 0 or self.y >= top[0] or self.x >= top[1]

    def pos(self):
        return (self.y, self.x)


def scootch(map: np.chararray, pos: Point, direction: Point) -> np.chararray:
    new_pos = pos + direction
    if (new_pos).check_bounds(map.shape):
        return map, map.shape[0] - pos.y
    if map[new_pos.pos()] == ".":
        map[new_pos.pos()] = "O"
        map[pos.pos()] = "."
        return scootch(map, new_pos, direction)
    else:
        return map, map.shape[0] - pos.y


def tilt(
    map: np.chararray, direction: Literal["N", "W", "S", "E"]
) -> tuple[np.chararray, int]:
    move_dict = {
        "N": Point(-1, 0),
        "W": Point(0, -1),
        "S": Point(1, 0),
        "E": Point(0, 1),
    }
    score = 0
    all_o = (
        zip(*np.where(map == "O"))
        if direction in ["N", "W"]
        else zip(reversed(np.where(map == "O")[0]), reversed(np.where(map == "O")[1]))
    )
    for pos in all_o:
        map, single_score = scootch(map, Point(*pos), move_dict[direction])
        score += single_score
    return map, score


def solve(part: int):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = np.char.asarray(load_str(data_path))
    if part == 1:
        map, score = tilt(data, "N")
    elif part == 2:
        map = data
        directions = cycle(["N", "W", "S", "E"])
        cached_maps = OrderedDict()
        num_runs = 1000000000
        run_id = 0
        while run_id < num_runs:
            for _ in range(4):
                direction = next(directions)
                map, score = tilt(map, direction)
            maphash = "".join(map.flatten())
            if maphash in cached_maps:
                cached_run, _ = cached_maps[maphash]
                score = list(cached_maps.values())[
                    (num_runs - cached_run) % (run_id - cached_run) + cached_run - 1
                ][1]
                break

            else:
                cached_maps[maphash] = (run_id, score)
                run_id += 1

    print(f"The solution for part {part} is: {score}")


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
