import sys

import optimizers
from computer import *

if __name__ == "__main__":
    if sys.argv[1:]:
        filename = sys.argv[1]
    else:
        filename = input("Enter filename: ")
    filename = "../" + filename
    # computer, score = optimizers.exhaustive(filename)
    computer, score = optimizers.hill_climb(filename, 100)
