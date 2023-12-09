from helpers import load
import os
import time

def solve(part:int):
    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data = load(data_path)
    print("\n".join(data))

if __name__=="__main__":
    start = time.perf_counter()
    # solve(1)
    intermediate = time.perf_counter()
    print(
        f"Computation time for part 1: {1000*(intermediate-start):0.3f} milliseconds."
    )
    # solve(2)
    stop = time.perf_counter()
    print(f"Computation time for part 2: {1000*(stop-intermediate):0.3f} milliseconds.")
