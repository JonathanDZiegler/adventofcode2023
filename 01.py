from helpers import load_str, load_int
import os

def solve():
    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data = load_int(data_path)
    print(data)

if __name__=="__main__":
    solve()
