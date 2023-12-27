import os
import sys
import time

import numpy as np

from helpers import load

sys.setrecursionlimit(100000)


def show(hiking_map, seen_pos):
    for e in seen_pos:
        hiking_map[e] = "O"
    print("\n".join(["".join(line) for line in hiking_map.tolist()]))


def solve(part: int):
    def dfs(pos: tuple, seen: set):
        terrain = hiking_map[pos]
        if (
            pos in seen
            or terrain == "#"
            or any([p < 0 for p in pos])
            or any([p >= d for p, d in zip(pos, list(hiking_map.shape))])
        ):
            return 0
        elif pos[0] == hiking_map.shape[0] - 1:
            return len(seen)
        else:
            up = (pos[0] - 1, pos[1])
            right = (pos[0], pos[1] + 1)
            left = (pos[0], pos[1] - 1)
            down = (pos[0] + 1, pos[1])
            if terrain == "^":
                steps = [up]
            elif terrain == ">":
                steps = [right]
            elif terrain == "<":
                steps = [left]
            elif terrain == "v":
                steps = [down]
            else:
                steps = [up, right, left, down]

            result = max(dfs(new_pos, seen | set([pos])) for new_pos in steps)
            return result
    def dfs_dp(pos: tuple, seen: set, dp:dict):
        if (
            pos in seen
            or any([p < 0 for p in pos])
            or any([p >= d for p, d in zip(pos, list(hiking_map.shape))])
            or hiking_map[pos] == "#"
        ):
            return 0
        elif pos[0] == hiking_map.shape[0] - 1:
            return 1
        up = (pos[0] - 1, pos[1])
        right = (pos[0], pos[1] + 1)
        left = (pos[0], pos[1] - 1)
        down = (pos[0] + 1, pos[1])
        steps = [up, right, left, down]
        return max(dp[pos], 1+max(dfs_dp(new_pos, seen | set([pos]), dp) for new_pos in steps))

    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    hiking_map = np.char.asarray([list(l) for l in data])
    if part==1:
        current = (0, np.argwhere(hiking_map[0] == ".")[0, 0])
        res = dfs(current, set())
        print(f"Solution for part {part}: {res}")
    if part==2:
        # current = (len(hiking_map)-2, np.argwhere(hiking_map[-1] == ".")[0, 0])
        dp = np.zeros(hiking_map.shape, dtype=int)
        for i in reversed(range(hiking_map.shape[0])):
            for j in reversed(range(hiking_map.shape[1])):
                dp[(i,j)]= dfs_dp((i,j), set(), dp)
        # res = 
        print(f"Solution for part {part}: {res}")



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
