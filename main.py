import sys

import optimizers
from noptimizer import *
from computer import *

if __name__ == "__main__":
    if sys.argv[1:]:
        filename = sys.argv[1]
    else:
        filename = input("Enter filename: ")
    filename = "../" + filename
    # score, computer = optimizers.exhaustive(filename)
    score, computer = optimizers.hill_climb(filename, 35)


    print("\n######### NOPTIMIZING #########")
    print("Noptimeraren är inte alls lika consistent som hårdvarutestaren. Ibland kan den fastna "
          "i ett par minuter innan den hittar en till förbättring. Ibland fastnar den helt i ett "
          "lokalt minimum så det kan vara värt att köra den ett par gånger för att se om den hittar "
          "nåt bättre. Det kan också hända att andra hårdvarukonfigurationer ger bättre resultat "
          "efter noptimering.")
    print("Bästa koden sparas i noptimizer_best.s.\n")

    #computer = Computer(Cache(64, 8, 1), Cache(32, 8, 1), Memory(8, 30, 6))

    print("Using", repr(computer))
    print()

    try:
        noptimize(filename, computer)
    except StartStopMarkersException as e:
        print(str(e))
