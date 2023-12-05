from helpers import load
import os
import numpy as np
from functools import partial
from joblib import Parallel, delayed
from tqdm import tqdm


def preprocess(data: list):
    seeds = [int(c) for c in (data[0].split(":", 1)[1]).split()]
    curr_lines = []
    map_lines = {}
    names = []
    for l in data[2:]:
        if len(l) == 0:
            map_lines[name] = curr_lines
            curr_lines = []
        elif l[0].isalpha():
            name = l.split()[0]
            names.append(name)
        else:
            curr_lines.append([int(c) for c in l.split()])
    map_lines[name] = curr_lines
    return seeds, map_lines, names


def step(ids, single_map):
    for i, id in enumerate(ids):
        appended = False
        for map in single_map:
            if map[1] <= id <= map[1] + map[2]:
                offset = id - map[1]
                ids[i] = map[0] + offset
                appended = True
                break
        if not appended:
            ids[i] = id
    return ids


def vector_step(idx:int, single_map)->int:
    for map in single_map:
        if map[1] <= idx <= map[1] + map[2]:
            offset = idx - map[1]
            idx = map[0] + offset
            break
    return idx


def solve(part: int = 1):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    seeds, seed_map, map_order = preprocess(data)
    if part == 2:
        seeds = np.hstack(
            [
                np.arange(start, start + length)
                for start, length in zip(seeds[::2], seeds[1::2])
            ]
        )
    curr_ids = seeds
    for name in tqdm(map_order):
        # transform = np.vectorize(vector_step, excluded=["single_map"])
        transform= partial(vector_step, single_map=seed_map[name])
        curr_ids = transform(curr_ids)
    print(min(curr_ids))


if __name__ == "__main__":
    # solve(1)
    solve(2)
