from helpers import load_str
import os
import time
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

connections = {
    "S": [(1, 0), (-1, 0), (0, 1), (0, -1)],  # Starting point
    "|": [(1, 0), (-1, 0)],  # Vertical pipe
    "-": [(0, 1), (0, -1)],  # Horizontal pipe
    "L": [(-1, 0), (0, 1)],  # 90-degree bend (north and east)
    "J": [(-1, 0), (0, -1)],  # 90-degree bend (north and west)
    "7": [(1, 0), (0, -1)],  # 90-degree bend (south and west)
    "F": [(1, 0), (0, 1)],  # 90-degree bend (south and east)
    ".": [],  # Ground; no pipe
}


def load():
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load_str(data_path, delim=None)
    return np.char.array(data)


def addpos(a, b):
    return (a[0] + b[0], a[1] + b[1])


def solve(data, part: int):
    def step(pos: tuple[int, int], current: int):
        queue = deque([(pos, current)])
        while len(queue) > 0:
            pos, current = queue.popleft()

            if (
                connected.get(pos) == -1
                or any([elem < 0 for elem in pos])
                or any([elem >= size for elem, size in zip(pos, list(data.shape))])
            ):
                continue

            elif not any(
                [
                    connected.get(addpos(pos, instruction), -1) >= 0
                    for instruction in connections[data[pos]]
                ]
            ):
                connected[pos] = -1
                continue

            next_tiles = [
                addpos(pos, instruction) for instruction in connections[data[pos]]
            ]

            # Update the connected dictionary with the minimum distance
            if connected.get(pos, np.inf) > current:
                connected[pos] = current + 1

                # Add next tiles to the queue if they haven't been visited or have a greater distance
                queue.extend(
                    (tile, current + 1)
                    for tile in next_tiles
                    if connected.get(tile, -1) < 0
                    or connected.get(tile, 0) > current + 1
                )

    starting_pos = tuple([a[0] for a in np.nonzero(data.find("S") == 0)])
    connected = {starting_pos: 0}

    # Explore the loop starting from the S tile
    for tile in (addpos(starting_pos, instruction) for instruction in connections["S"]):
        step(tile, 0)

        
    res = np.full(data.shape, -10, dtype=int)
    for k, v in connected.items():
        res[k] = v
    plt.imshow(res, aspect="auto")
    plt.savefig('res.pdf')
    plt.colorbar()
    print(f"Furthest distance is {max(connected.values())}.")



if __name__ == "__main__":
    data = load()
    start = time.perf_counter()
    solve(data, 1)
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
