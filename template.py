from helpers import load
import os

def solve():
    data_path = f'data_d_{os.path.basename(__file__)[:-2]}csv'
    data = load(data_path)
    print("\n".join(data))

if __name__=="__main__":
    solve()
