from helpers import load
import os
from collections import Counter, ChainMap
import numpy as np
from itertools import groupby


def preprocess(line: str) -> tuple[str, int]:
    hand, bid = line.split()
    bid = int(bid)
    return (hand, bid)


def score_hand_1(line: tuple) -> dict:
    hand, _ = line
    counts = Counter(hand)
    commons = counts.most_common()
    if commons[0][1] == 5:
        return {line: 7}
    elif commons[0][1] == 4:
        return {line: 6}
    elif commons[0][1] == 3 and commons[1][1] == 2:
        return {line: 5}
    elif commons[0][1] == 3:
        return {line: 4}
    elif commons[0][1] == 2 and commons[1][1] == 2:
        return {line: 3}
    elif commons[0][1] == 2:
        return {line: 2}
    else:
        return {line: 1}


def score_hand_2(line: tuple) -> dict:
    hand, _ = line
    counts = Counter(hand)
    js = counts["J"]
    counts["J"] = 0
    commons = counts.most_common()
    if (commons[0][1] + js) == 5:
        return {line: 7}
    elif (commons[0][1] + js) == 4:
        return {line: 6}
    elif ((commons[0][1] + js == 3) and commons[1][1] == 2) or (
        commons[0][1] == 3 and (commons[1][1] + js == 2)
    ):
        return {line: 5}
    elif commons[0][1] + js == 3:
        return {line: 4}
    elif commons[0][1] == 2 and (commons[1][1] + js) == 2:
        return {line: 3}
    elif (commons[0][1] + js) == 2:
        return {line: 2}
    else:
        return {line: 1}


def rank_hands(scored_hands: dict, part: int) -> int:
    sorted_hands = sorted(scored_hands.items(), key=lambda x: x[1])
    grouped_hands = {
        rank: list([e[0] for e in group])
        for rank, group in groupby(sorted_hands, key=lambda x: x[1])
    }
    if part == 1:
        card_order = {
            "2": 0,
            "3": 1,
            "4": 2,
            "5": 3,
            "6": 4,
            "7": 5,
            "8": 6,
            "9": 7,
            "T": 8,
            "J": 9,
            "Q": 10,
            "K": 11,
            "A": 12,
        }
    elif part == 2:
        card_order = {
            "J": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
            "9": 8,
            "T": 9,
            "Q": 10,
            "K": 11,
            "A": 12,
        }
    else:
        raise ValueError(f"Unknow part id {part}.")

    res = []
    for rank, hands in grouped_hands.items():
        hands.sort(key=lambda x: [card_order[c] for c in x[0]])
        res.extend([hand[1] for hand in hands])

    return np.sum([(i + 1) * res[i] for i in range(len(res))])


def solve(part: int) -> None:
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    processed = [preprocess(l) for l in data]
    if part == 1:
        scored = dict(ChainMap(*[score_hand_1(l) for l in processed]))
    elif part == 2:
        scored = dict(ChainMap(*[score_hand_2(l) for l in processed]))
    res = rank_hands(scored, part=part)
    print(res)


if __name__ == "__main__":
    # solve(1)
    solve(2)
