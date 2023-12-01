from helpers import load
import os


def extract_ints(line: str, problem: int = 1):
    def scan(line, rev: bool = False):
        ints = ""
        for idx in range(len(line)):
            if ints != "":
                return ints
            if problem == 2:
                line = (
                    line[:idx]
                    + convert_string_to_int(line[idx : idx + 5], rev=rev)
                    + line[idx + 5 :]
                )
            try:
                ints = int(line[idx])
            except:
                pass
        return ints

    tens = scan(line)
    ones = scan(line[::-1], rev=True)
    return 10 * tens + ones


def convert_string_to_int(line, rev: bool = False):
    if rev:
        vocab = {
            "eno": "1",
            "owt": "2",
            "eerht": "3",
            "ruof": "4",
            "evif": "5",
            "xis": "6",
            "neves": "7",
            "thgie": "8",
            "enin": "9",
        }
    else:
        vocab = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }
    for key, value in vocab.items():
        idx = line.find(key)
        if idx > -1:
            line = line[:idx] + value + line[idx + len(key) :]
    return line


def solve(problem: int):
    data_path = f"data_d_{os.path.basename(__file__)[:-2]}csv"
    data = load(data_path)
    res = [extract_ints(line, problem) for line in data]
    print(sum(res))


if __name__ == "__main__":
    solve(1)
    solve(2)
