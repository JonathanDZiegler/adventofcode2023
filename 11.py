from helpers import load_str
import os
import time
import numpy as np
import sys
from scipy.spatial.distance import cdist




def preprocess(data_path:os.PathLike)->np.array:
    data = load_str(data_path)
    data = np.char.asarray(data)
    data = np.asarray(data.replace(".", "0").replace('#',"1"), dtype=bool)
    return data

def print_map(data):
    np.set_printoptions(threshold=sys.maxsize)
    print(np.char.asarray(data, unicode=True).replace('False','.').replace('True',"#"))


def expand(data:np.array):
    c=0
    for col in data.T:
        if not any(col):
            data = np.insert(data, c, values=False,axis=1)
            c+=1
        c+=1
    r=0
    for row in data:
        if not any(row):
            data = np.insert(data, r, values=False,axis=0)
            r+=1
        r+=1
    return data

def calc_distances(data:np.array):
    points = np.argwhere(data)
    distances = []
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            distances.append(int(np.linalg.norm(points[j]-points[i],ord=1)))
    return distances


def solve(part:int):
    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data=preprocess(data_path)
    data=expand(data)
    distances = calc_distances(data)
    print(f"Sum of all distances is: {np.sum(distances)}.")

if __name__=="__main__":
    start = time.perf_counter()
    solve(1)
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
    # solve(2)
    stop = time.perf_counter()
    print(f"Computation time for part 2: {1000*(stop-intermediate):0.3f} milliseconds.")
