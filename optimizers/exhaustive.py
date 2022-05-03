import concurrent.futures
import itertools
from itertools import repeat

import computer
from computer import Computer


def exhaustive(filename):
    best_score = 1e9
    best_computer = None
    best_cycles = 1e9
    iter_computers = computer.all_computers()
    batch_size = 4
    nof_computers = 33696  # nof allowed computer configurations
    tested_count = 0
    prev_print = 0
    while 1:
        batch = list(itertools.islice(iter_computers, batch_size))
        if len(batch) == 0:
            break
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(Computer.run, batch, repeat(filename))

            for (score, cycles), c in zip(results, batch):
                if score < best_score:
                    best_score = score
                    best_cycles = cycles
                    best_computer = c
                    print("\n=== NEW BEST ===")
                    print(c)
                    print("Cycles:", cycles)
                    print("Score:", round(score, 2), "μsC$\n")
        tested_count += len(batch)
        p = int(tested_count / nof_computers * 1000)
        if p != prev_print:
            print(str(p / 10) + "%")
            prev_print = p

    print("\n\n=== BEST COMPUTER ===")
    print(best_computer)
    print("Cycles:", best_cycles)
    print("Score:", round(best_score, 3), "μsC$\n")

    return (best_score, best_computer)
