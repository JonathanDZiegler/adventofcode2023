from helpers import load
import os
import numpy as np
from collections import Counter

def find_matches(card:str)->list[int]:
    winning_nums = set([int(c) for c in card[card.index(":")+1:card.index("|")].split()])
    card_nums = [int(c) for c in card[card.index("|")+1:].split()]
    return [num in winning_nums for num in card_nums]

def get_card_points(card:str)->int:
    found_nums = find_matches(card)
    res = np.sum(found_nums)
    return 2**(np.sum(found_nums)-1) if res>0 else 0

def count_cards(data, idx):
    counter[idx]+=1
    num_matches = np.sum(find_matches(data[idx]))
    [count_cards(data, idx+i) for i in np.arange(1,num_matches+1)]

def solve():
    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data = load(data_path)
    # res_part_1 = [get_card_points(line) for line in data]
    # print(f"Part 1 result: {np.sum(res_part_1)}")
    [count_cards(data, idx) for idx in range(len(data))] 
    print(f"Total number of scratchcards: {counter.total()}")


if __name__=="__main__":
    counter = Counter()
    solve()
