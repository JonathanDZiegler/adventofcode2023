from helpers import load
import os
from itertools import cycle
import sys
import time

sys.setrecursionlimit(100000)


def preprocess(data: list[str]) -> tuple[cycle, dict[dict]]:
    instructions = cycle(list(data[0]))
    nodes = {
        line[:3]: {"value": line[:3], "L": line[7:10], "R": line[12:15]}
        for line in data[2:]
    }
    return instructions, nodes


def step(instructions: cycle, node: dict, nodes: dict, count: int) -> int:
    if node["value"] == "ZZZ":
        return count
    else:
        count += 1
        dir = next(instructions)
        return step(instructions, nodes[node[dir]], nodes, count)


def step_2(instructions: cycle, node_list: list[dict], nodes: dict):
    done = False
    params = (instructions, node_list, nodes)
    count = 0
    while not done:
        if count%1000000==0:
            print(f"We've hit {count} counts!")
        count += 1
        done, params = step_list(*params)
    return count - 1


def step_list(instructions: cycle, node_list: list[dict], nodes: dict):
    if all([node["value"][-1] == "Z" for node in node_list]):
        return True, None
    else:
        dir = next(instructions)
        return False, (instructions, [nodes[node[dir]] for node in node_list], nodes)


def solve(part: int):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    instructions, nodes = preprocess(data)
    if part == 1:
        steps = step(instructions, nodes["AAA"], nodes, 0)
        print(f"We reach ZZZ after {steps} steps.")
    elif part == 2:
        steps = step_2(
            instructions,
            [node for node in nodes.values() if node["value"][-1] == "A"],
            nodes,
        )
        print(f"All nodes end in Z after {steps} steps.")


if __name__ == "__main__":
    start = time.perf_counter()
    solve(1)
    intermediate = time.perf_counter()
    print(f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds.")
    solve(2)
    stop = time.perf_counter()
    print(f"Computation time for part 2: {1000*(stop-intermediate):0.3f} milliseconds.")
