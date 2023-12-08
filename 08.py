from helpers import load
import os
from itertools import cycle
import time
import math


def preprocess(data: list[str]) -> tuple[cycle, dict[dict]]:
    instructions = list(data[0])
    nodes = {
        line[:3]: {"value": line[:3], "L": line[7:10], "R": line[12:15]}
        for line in data[2:]
    }
    return instructions, nodes


def step(instructions: cycle, node: dict, nodes: dict) -> int:
    count = 0
    while node["value"] != "ZZZ":
        count += 1
        dir = next(instructions)
        node = nodes[node[dir]]
    return count


def step_2(instructions: cycle, node: dict, nodes: dict) -> int:
    count = 0
    while node["value"][-1] != "Z":
        count += 1
        dir = next(instructions)
        node = nodes[node[dir]]
    return count


def solve(part: int):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    instructions, nodes = preprocess(data)
    if part == 1:
        steps = step(cycle(instructions), nodes["AAA"], nodes)
        print(f"We reach ZZZ after {steps} steps.")
    elif part == 2:
        steps = []
        for node in nodes.values():
            if node["value"][-1] == "A":
                steps.append(step_2(cycle(instructions), node, nodes))
        print(f"All nodes end in Z after {math.lcm(*steps)} steps.")


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
