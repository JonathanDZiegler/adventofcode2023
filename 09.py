from helpers import load_int
import os
import time
import numpy as np

sequence = list[int]


def derivative(seq: sequence) -> sequence:
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


def build_head(head: sequence) -> int:
    res = [0]
    for elem in head[::-1]:
        res.append(elem - res[-1])
    return res[-1]


def find_next_element(seq: sequence) -> tuple[int, int]:
    head = []
    tail = []
    while True:
        if not any([bool(e) for e in seq]):
            break
        tail.append(seq[-1])
        head.append(seq[0])
        seq = derivative(seq)
    return sum(tail), build_head(head)


def solve() -> None:
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load_int(data_path)
    res = [find_next_element(l) for l in data]
    part_1, part_2 = zip(*res)
    print(f"The result for part one is {sum(part_1)}.")
    print(f"The result for part two is {sum(part_2)}.")


if __name__ == "__main__":
    start = time.perf_counter()
    solve()
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1 and 2 combined: {1000*(intermediate-start):0.3f} milliseconds."
    )
