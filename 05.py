import os
import time

from helpers import load


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


def calc_overlap(a: range, b: range):
    return range(max(a[0], b[0]), min(a[-1], b[-1]) + 1)


def range_step(range_list: list[range], map_list) -> list[list[range]]:
    results = []
    while range_list:
        elem = range_list.pop(0)
        for single_map in map_list:
            target, source, length = single_map
            map_range = range(source, source + length)
            overlap = calc_overlap(elem, map_range)
            # map overlap of ranges to target values and add to list of output ranges
            if len(overlap) > 0:
                results.append(
                    range(
                        target + overlap.start - source, target + overlap.stop - source
                    )
                )
                # check for underflow of range
                if elem.start < overlap.start:
                    range_list.append(range(elem.start, min(elem.stop, overlap.start)))
                # check for overflow of range
                elif overlap.stop < elem.stop:
                    range_list.append(range(max(overlap.stop, elem.start), elem.stop))
                break
        else:
            results.append(elem)

    return results


def solve(part: int = 1):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    seeds, seed_map, map_order = preprocess(data)
    if part == 2:
        curr_ranges = [
            range(start, start + length)
            for start, length in zip(seeds[::2], seeds[1::2])
        ]
        for name in map_order:
            curr_ranges = range_step(curr_ranges, seed_map[name])

        print(min([e.start for e in curr_ranges]))
    else:
        curr_ids = seeds
        for name in map_order:
            curr_ids = step(curr_ids, seed_map[name])
        print(min(curr_ids))


if __name__ == "__main__":
    start = time.perf_counter()
    solve(1)
    intermediate = time.perf_counter()
    solve(2)
    stop = time.perf_counter()
    print(f"Part 1 compute time: {1000*(intermediate-start):0.2f} milliseconds")
    print(f"Part 2 compute time: {1000*(stop-intermediate):0.2f} milliseconds")
