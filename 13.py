from helpers import load
import os
import time
import numpy as np


def load_and_preprocess():
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    res = []
    tmp = []
    for l in data:
        if l != "":
            tmp.append(list(l))
        else:
            res.append(np.char.asarray(tmp))
            tmp = []
    res.append(np.char.asarray(tmp))
    return res


def check_symmetry(a: np.chararray):
    pass


def solve(data: np.chararray, part: int):
    res = []
    if part == 1:
        for map in data:
            score = 0
            # column symmetry
            width = map.shape[1]
            for idx in range(1, int(np.ceil(width / 2))):
                if np.all(map[:, :idx] == np.flip(map[:, idx : 2 * idx], axis=1)):
                    score += idx
                    break
                elif np.all(map[:, -idx:] == np.flip(map[:, -2 * idx : -idx], axis=1)):
                    score += width - idx
                    break

            # row symmetry
            height = map.shape[0]
            for idx in range(1, int(np.ceil(height / 2))):
                if np.all(map[:idx, :] == np.flip(map[idx : 2 * idx, :], axis=0)):
                    score += 100 * idx
                    break
                elif np.all(map[-idx:, :] == np.flip(map[-2 * idx : -idx, :], axis=0)):
                    score += 100 * (height - idx)
                    break
            res.append(score)
    elif part == 2:
        for map in data:
            score = 0
            # column symmetry
            width = map.shape[1]
            for idx in range(1, int(np.ceil(width / 2))):
                if np.sum(map[:, :idx] != np.flip(map[:, idx : 2 * idx], axis=1)) == 1:
                    score += idx
                    break
                elif (
                    np.sum(map[:, -idx:] != np.flip(map[:, -2 * idx : -idx], axis=1))
                    == 1
                ):
                    score += width - idx
                    break

            # row symmetry
            height = map.shape[0]
            for idx in range(1, int(np.ceil(height / 2))):
                if np.sum(map[:idx, :] != np.flip(map[idx : 2 * idx, :], axis=0)) == 1:
                    score += 100 * idx
                    break
                elif (
                    np.sum(map[-idx:, :] != np.flip(map[-2 * idx : -idx, :], axis=0))
                    == 1
                ):
                    score += 100 * (height - idx)
                    break
            res.append(score)
    print(np.sum(res))


if __name__ == "__main__":
    start = time.perf_counter()
    data = load_and_preprocess()
    solve(data, 1)
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
    solve(data, 2)
    stop = time.perf_counter()
    print(f"Computation time for part 2: {1000*(stop-intermediate):0.3f} milliseconds.")
