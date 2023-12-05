from helpers import load
import os
import re
import numpy as np

def max_color(line:str, color:str, constraint:int):
    game = int(line[5:line.find(":")])
    matches = [match.start() for match in re.finditer(color, line)]
    matches = [int(line[max(0,match-3) : match-1]) for match in matches]
    res =  max([int(c) for c in matches])
    return game if res<= constraint else 0

def min_color(line:str, color:str):
    matches = [match.start() for match in re.finditer(color, line)]
    matches = [int(line[max(0,match-3) : match-1]) for match in matches]
    return max([int(c) for c in matches])


def solve_1():
    constraint = {
        "red":12,
        "green":13,
        "blue":14,
    }
    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data = load(data_path)
    max_marbles = {color: [max_color(l, color, val)for l in data] for color, val in constraint.items()}
    res = set.intersection(*map(set,max_marbles.values()))
    print(sum(res))    

def solve_2():
    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data = load(data_path)
    min_counts = [[min_color(l, color) for l in data] for color in ['red', 'blue', 'green']]
    counts = np.array(min_counts)
    power = np.prod(counts, axis=0)
    print(power.sum())

if __name__=="__main__":
    # solve_1()
    solve_2()
