from helpers import load
import os
import numpy as np

def solve_race(s, t):
    x1 = t/2 - np.sqrt((t**2/4)-s)
    x2 = t/2 + np.sqrt(t**2/4-s)
    res = len(range(int(x1)+1, int(np.ceil(x2))))
    return res

def solve(part):
    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data = load(data_path)
    if part==1:
        times = [int(c) for c in data[0].split(':',1)[1].split()]
        distances = [int(c) for c in data[1].split(':',1)[1].split()]
    if part==2:
        times = [int(data[0].split(":",1)[1].replace(" ",""))]
        distances = [int(data[1].split(":",1)[1].replace(" ",""))]
    res = [solve_race(s,t) for s,t in zip(distances, times)]
    print(np.prod(res))
        
if __name__=="__main__":
    solve(1)
    solve(2)
