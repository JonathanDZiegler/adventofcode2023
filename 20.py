import math
import os
import time
from itertools import count
from typing import Union

from helpers import load

ModuleOutput = list[tuple[str, str, bool]]


class Flipflop(object):
    def __init__(self, name: str, outputs: list[str]) -> None:
        self.name = name
        self.state: bool = False
        self.outputs = outputs

    def __call__(self, source: str, signal: bool) -> Union[tuple, ModuleOutput]:
        if not signal:
            self.state = not self.state
            return [(self.name, k, self.state) for k in self.outputs]
        return tuple()

    def __repr__(self) -> str:
        return self.name + ": Flip-flop module"


class Conjunction(object):
    def __init__(self, name: str, inputs: list[str], outputs: list[str]) -> None:
        self.name = name
        self.inputs: dict = {elem: False for elem in inputs}
        self.outputs = outputs

    def add_input(self, input: str) -> None:
        self.inputs[input] = False

    def __call__(self, source: str, signal: bool) -> ModuleOutput:
        self.inputs[source] = signal
        return [(self.name, k, not all(self.inputs.values())) for k in self.outputs]

    def __repr__(self) -> str:
        return self.name + ": Conjunction module"


class Broadcaster(object):
    def __init__(self, name: str, outputs: list[str]) -> None:
        self.name = name
        self.outputs = outputs

    def __call__(self, source: str, signal: bool) -> ModuleOutput:
        return [(self.name, k, signal) for k in self.outputs]

    def __repr__(self) -> str:
        return self.name + ": Broadcaster module"


def solve(part: int):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    components: dict = dict()
    conjunctions: set = set()
    for line in data:
        source, dest = line.split(" -> ")
        dl = dest.split(", ")
        if source[0] == "%":
            components[source[1:]] = Flipflop(name=source[1:], outputs=dl)
        elif source[0] == "&":
            if source[1:] not in components:
                components[source[1:]] = Conjunction(
                    name=source[1:], inputs=[], outputs=dl
                )
                conjunctions.update(components)
        else:
            components[source] = Broadcaster(name=source, outputs=dl)
    for line in data:
        source, dest = line.split(" -> ")
        dl = dest.split(", ")
        for d in dl:
            if d == "rx" and d not in conjunctions:
                components[d] = Conjunction(
                    name=d,
                    inputs=[source.replace("%", "").replace("&", "")],
                    outputs=[],
                )
                conjunctions.update(d)
            if d not in components and d != "rx":
                components[d] = Broadcaster(name=d, outputs=[])
            if d in conjunctions and isinstance(components[d], Conjunction):
                components[d].add_input(source.replace("%", "").replace("&", ""))
    low = 0
    high = 0

    # Assumption for part 2: all conjunctions feeding into the last conjunction fire High in regular intervals.
    # Finding the lowest common multiplier is an efficient way of finding the solution
    final_layer = components[list(components["rx"].inputs.keys())[0]]
    cycles = []
    semi_final_layer = set(k for k in final_layer.inputs.keys())

    for presses in range(1000) if part == 1 else count(1):
        queue = [(None, "broadcaster", False)]
        low += 1
        while queue:
            source, dest, signal = queue.pop(0)
            res = components[dest](source, signal)
            low += sum([not a[2] for a in res])
            high += sum([a[2] for a in res])
            queue.extend(res)
            if (
                part == 2
                and source in semi_final_layer
                and dest == final_layer.name
                and signal
            ):
                cycles.append(presses)
                semi_final_layer.remove(source)
        if not semi_final_layer and part == 2:
            break
    if part == 1:
        print(f"Part 1: {low*high}")
    else:
        print(f"Part 2: {math.lcm(*cycles)}")


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
