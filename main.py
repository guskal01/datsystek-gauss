import sys

import optimizers
from noptimizer import noptimize, StartStopMarkersException
from computer import *

if __name__ == "__main__":
    if sys.argv[1:]:
        filename = sys.argv[1]
    else:
        filename = input("Enter filename: ")
    filename = "../" + filename
    
    #score, score_computer, cycles, cycles_computer = optimizers.exhaustive(filename)

    start_computer = None  # Computer(Cache(64, 8, 1), Cache(32, 8, 1), Memory(8, 30, 6))
    value, best_computer = optimizers.hill_climb(filename, 40, start_computer, 'score')


    print("\n######### NOPTIMIZING #########")
    print("Noptimeraren är inte alls lika consistent som hårdvarutestaren. Ibland kan den fastna "
          "i ett par minuter innan den hittar en till förbättring. Ibland fastnar den helt i ett "
          "lokalt minimum så det kan vara värt att köra den ett par gånger för att se om den hittar "
          "nåt bättre. Det kan också hända att andra hårdvarukonfigurationer ger bättre resultat "
          "efter noptimering.")
    print("Bästa koden sparas i noptimizer_best.s.\n")

    #computer = Computer(Cache(64, 8, 1), Cache(32, 8, 1), Memory(8, 30, 6))
    computer = best_computer

    if input("Noptimera? (y/n): ") == "y":
        print("Using", repr(computer))
        print()

        try:
            noptimize(filename, computer)
        except StartStopMarkersException as e:
            print(str(e))
