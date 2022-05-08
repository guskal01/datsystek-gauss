import random
import concurrent.futures
from itertools import repeat

from computer import Cache, Computer, Memory

choices = [
    [32, 64, 128],  # instruction cache size
    [1, 2, 4, 8],  # instruction cache block size
    [1, 2, 4],  # instruction cache associativity
    [32, 64, 128],  # data cache size
    [1, 2, 4, 8],  # data cache block size
    [1, 2, 4],  # data cache associativity
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # write buffer size
    [(44, 8), (30, 6)],  # memory access times
]


def get_choices(parameters):
    r = []
    for i in range(len(parameters)):
        r.append(choices[i][parameters[i]])
    return r

def get_parameters(computer):
    r = []
    for i,param in enumerate([computer.instruction_cache.size, computer.instruction_cache.block_size, computer.instruction_cache.associativity,
                              computer.data_cache.size, computer.data_cache.block_size, computer.data_cache.associativity,
                              computer.memory.write_buffer, (computer.memory.first_access, computer.memory.next_access)]):
        r.append(choices[i].index(param))
    return r

def build_computer(parameters):
    c = get_choices(parameters)
    return Computer(
        Cache(c[0], c[1], c[2]), Cache(c[3], c[4], c[5]), Memory(c[6], c[7][0], c[7][1])
    )


def evaluate(parameters, filename):
    return build_computer(parameters).run(filename)


def random_change(parameters, p=0.5):
    while 1:
        ind = random.randrange(len(parameters))
        parameters[ind] += random.choice([-1, 1])
        parameters[ind] = max(0, min(len(choices[ind]) - 1, parameters[ind]))
        if random.random() < p:
            return


def hill_climb(filename, iterations = 200, start_computer = None, mode = 'score'):
    threads = 3  # not faster to use more
    mode = mode.upper()
    assert(mode in ['SCORE', 'CYCLES'])
    
    if(start_computer == None):
        parameters = [len(c) // 2 for c in choices]
    else:
        parameters = get_parameters(start_computer)
    best_score, best_cycles = evaluate(parameters, filename)
    print("\n=== STARTING COMPUTER ===")
    print(build_computer(parameters))
    print("Cycles:", best_cycles)
    print("Score:", round(best_score, 2), "μsC$\n")
    best_parameters = [*parameters]
    seen = {tuple(parameters)}
    prev_print = 0
    for i in range(iterations):
        batch = []
        for j in range(threads):
            new_parameters = None
            while(new_parameters == None or tuple(new_parameters) in seen):
                new_parameters = [*parameters]
                random_change(new_parameters)
            seen.add(tuple(new_parameters))
            batch.append(new_parameters)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(evaluate, batch, repeat(filename))

        for (score, cycles), new_parameters in zip(results, batch):
            if (mode == 'SCORE' and score < best_score) or mode == 'CYCLES' and cycles < best_cycles:
                parameters = new_parameters
                best_score = score
                best_cycles = cycles
                print(f'\n=== NEW BEST FOR {mode} ===')
                print(build_computer(parameters))
                print("Cycles:", cycles)
                print("Score:", round(score, 2), "μsC$\n")
            
        p = int((i + 1) / iterations * 20)
        if p != prev_print:
            print(str(p * 5) + "%")
            prev_print = p

    best_computer = build_computer(parameters)
    print(f'\n\n=== BEST COMPUTER FOR {mode} ===')
    print("File:", filename)
    print(best_computer)
    print("Cycles:", best_cycles)
    print("Score:", round(best_score, 3), "μsC$\n")
    best_value = best_score if mode == 'SCORE' else best_cycles

    return (best_value, best_computer)
