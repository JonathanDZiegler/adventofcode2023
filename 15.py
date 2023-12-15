from helpers import load
import os
import time
import numpy as np
from collections import OrderedDict


def solve():
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)[0].split(",")

    print(f"Solution for part 1: {np.sum([score(elem) for elem in data])}")

    boxes = {i: OrderedDict() for i in range(256)}
    for elem in data:
        label, val = elem.split("=") if "=" in elem else (elem[:-1], False)
        box = score(label)
        if val:
            boxes[box][label] = int(val)
        elif not val and boxes[box].get(label, False):
            boxes[box].pop(label)
    fp = np.sum([focusing_power(box_idx, lenses) for box_idx, lenses in boxes.items()])
    print(f"Solution for part 2: {fp}")


def focusing_power(box_number, lenses):
    return int(
        (box_number + 1) * np.sum([(i + 1) * v for i, v in enumerate(lenses.values())])
    )


def score(chars: str):
    current = 0
    for c in chars:
        current = ((current + ord(c)) * 17) % 256
    return current


if __name__ == "__main__":
    start = time.perf_counter()
    solve()
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1 and 2 combined: {1000*(intermediate-start):0.3f} milliseconds."
    )
