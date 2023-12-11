def read_input_from_file(file_path) -> str:
    with open(file_path) as file:
        return file.read()


def input_lines(puzzle_input: str):
    return puzzle_input.split("\n")

def load(path:str):
    return input_lines(read_input_from_file(path))

def load_str(path:str, delim:str=None):
    lines = input_lines(read_input_from_file(path))
    if delim is None or len(delim)==0:
        return [list(l) for l in lines]
    else:
        return [l.split(delim) for l in lines]
    # return lines

def load_int(path:str, delim:str=" "):
    lines = input_lines(read_input_from_file(path))
    chars = [l.split(delim) for l in lines]
    return [[int(c) for c in l] for l in chars]
    # return lines