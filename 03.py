from helpers import load_str, load
import os
from typing import List
import numpy as np

def is_symbol(char:str)->bool:
    return (not char.isalnum()) and char!="."


def solve():
    seen = set()

    def search(data:List[str], row:int, col:int, buffer:list=[])->List[int]:
        if (row, col) in seen:
            return ""
        if row < 0 or row>=len(data) or col<0 or col>=len(data[0]):
            return ""
        char = data[row][col]
        if char.isnumeric():
            seen.add((row,col))
            char = search(data, row, col-1) + char + search(data, row, col+1)
            return char
        return ""

    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data = load(data_path)
    chars = [[is_symbol(c) for c in row] for row in data]
    res_part_1 = 0
    res_part_2 = 0
    for row, column in zip(*np.where(chars)):
        current_nums = []
        seen.add((row, column))
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                res = search(data,row+y,column+x)
                if len(res) > 0:
                    res_part_1+= int(res)
                    current_nums.append(res)
            
        if len(current_nums) == 2:
            res_part_2 += np.prod([int(num) for num in current_nums])
        

    # disp_chars = ["".join([str(int(is_symbol(c))) for c in row]) for row in data]
    # print("\n".join(data))
    # print("\n".join(chars))
    return res_part_1, res_part_2 

if __name__=="__main__":
    print(solve())
