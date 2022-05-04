import shutil
import random
from computer import AsmExecutionException

noprow = "nop\t\t#noptimizer\n"
tmp_file = "noptimize_test.s"
best_file = "../noptimize_best.s"
startstring = "### START"
stopstring = "### STOP"

class StartStopMarkersException(Exception):
    pass

def is_code(row):
    row = row.strip()
    if(len(row) == 0 or row[0] == '#'):
        return False
    return True

def modify_code(code):
    starts = 0
    while(code[0] == noprow):
        code.pop(0)
        starts += 1

    no_change = False

    rnd = random.random()
    if(rnd < 0.2):
        # Change number of nops at start
        starts = (starts+random.randint(1, 7))%8  # must change
    elif(rnd < 0.4):
        # Add one random nop
        row = -1
        while(row == -1 or (row != len(code) and not is_code(code[row]))):
            row = random.randint(1, len(code))
        code.insert(row, noprow)
        if(random.random() < 0.2):
            # Move it from start instead
            starts = (starts-1)%8
    elif(rnd < 0.5):
        # Remove one random nop
        if(code.count(noprow) > 0):
            row = -1
            while(row == -1 or code[row] != noprow):
                row = random.randint(0, len(code)-1)
            code.pop(row)
            if(random.random() < 0.2):
                # Move it to start instead
                starts = (starts+1)%8
        else:
            no_change = True
    else:
        # Move a nop
        if(code.count(noprow) > 0):
            row = -1
            while(row == -1 or code[row] != noprow):
                row = random.randint(0, len(code)-1)
            code.pop(row)
            assert row == len(code) or is_code(code[row])
            nrow = row
            options_down = []
            while nrow < len(code) and len(options_down) < 6:
                nrow += 1
                while(nrow < len(code) and not is_code(code[nrow])):
                    nrow += 1
                if(random.random() < 0.5 ** len(options_down)):
                    options_down.append(nrow)
            nrow = row
            options_up = []
            while nrow > 1 and len(options_up) < 6:
                nrow -= 1
                while(nrow > 1 and not is_code(code[nrow])):
                    nrow -= 1
                if(random.random() < 0.5 ** len(options_up)):
                    options_up.append(nrow)
            row = random.choice(options_down + options_up)
            code.insert(row, noprow)
        else:
            no_change = True

    for i in range(starts):
        code.insert(0, noprow)

    if(no_change or random.random() > 0.9):
        # Another change
        modify_code(code)

def noptimize(file, computer):
    with open(file, 'r') as f:
        original = f.readlines()

    stripped = [line.strip() for line in original]
    if(stripped.count(startstring) != 1 or stripped.count(stopstring) != 1):
        raise StartStopMarkersException(f"Need start and stop markers. Add rows \"{startstring}\" and \"{stopstring}\" around eliminate function.")
    start = stripped.index(startstring)
    stop = stripped.index(stopstring)
    if(start >= stop):
        raise StartStopMarkersException("Start must be before stop.")
    precode = original[:start+1]
    postcode = original[stop:]
    original = original[start+1:stop]
    
    best_score, best_cycles = computer.run(file)
    print(f"Starting point: {best_cycles}\t({best_score:.2f})")
    shutil.copyfile(file, best_file)
    best_code = [*original]

    while True:
        test = [*best_code]
        modify_code(test)
        with open(tmp_file, 'w+') as f:
            f.writelines(precode)
            f.writelines(test)
            f.writelines(postcode)
        try:
            score, cycles = computer.run(tmp_file)
        except AsmExecutionException as e:
            score = float('inf')
            cycles = float('inf')
        if(cycles < best_cycles):
            print(f"NEW BEST: {cycles}\t({score:.2f})")
            shutil.copyfile(tmp_file, best_file)
            best_cycles = cycles
            best_score = score
            best_code = test
        elif(cycles == best_cycles):
            best_code = test
