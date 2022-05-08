import concurrent.futures
import itertools
from itertools import repeat

import computer
from computer import Computer


def exhaustive(filename):
    best_score = {
        'score': 1e9,
        'cycles': 1e9,
        'computer': None
    }
    best_cycles = {
        'score': 1e9,
        'cycles': 1e9,
        'computer': None
    }
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
                if score < best_score['score']:
                    best_score = {
                        'score': score,
                        'cycles': cycles,
                        'computer': c
                    }
                    print("\n=== NEW BEST FOR SCORE ===")
                    print(c)
                    print("Cycles:", cycles)
                    print("Score:", round(score, 2), "μsC$\n")
                if cycles < best_cycles['cycles']:
                    best_cycles = {
                        'score': score,
                        'cycles': cycles,
                        'computer': c
                    }
                    print("\n=== NEW BEST FOR CYCLES ===")
                    print(c)
                    print("Cycles:", cycles)
                    print("Score:", round(score, 2), "μsC$\n")
        
        tested_count += len(batch)
        p = int(tested_count / nof_computers * 1000)
        if p != prev_print:
            print(str(p / 10) + "%")
            prev_print = p

    print("\n\n=== BEST COMPUTER FOR SCORE ===")
    print(best_score['computer'])
    print("Cycles:", best_score['cycles'])
    print("Score:", round(best_score['score'], 3), "μsC$\n")

    print("\n\n=== BEST COMPUTER FOR CYCLES ===")
    print(best_cycles['computer'])
    print("Cycles:", best_cycles['cycles'])
    print("Score:", round(best_cycles['score'], 3), "μsC$\n")

    return (best_score['score'], best_score['computer'], best_cycles['cycles'], best_cycles['computer'])
