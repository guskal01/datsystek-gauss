import shutil
import random
from computer import AsmExecutionException

nopline = "nop\t\t#noptimizer\n"
tmp_file = "noptimize_test.s"
best_file = "../noptimize_best.s"
startstring = "### START"
stopstring = "### STOP"

class StartStopMarkersException(Exception):
    pass

def is_code(line):
    line = line.strip()
    if(len(line) == 0 or line[0] == '#'):
        return False
    return True

def modify_code(code):
    starts = 0
    while(code[0] == nopline):
        code.pop(0)
        starts += 1

    no_change = False

    rnd = random.random()
    if(rnd < 0.2):
        # Change number of nops at start
        starts = (starts+random.randint(1, 7))%8  # must change
    elif(rnd < 0.4):
        # Add one random nop
        line = -1
        while(line == -1 or (line != len(code) and not is_code(code[line]))):
            line = random.randint(1, len(code))
        code.insert(line, nopline)
        if(random.random() < 0.2):
            # Move it from start instead
            starts = (starts-1)%8
    elif(rnd < 0.5):
        # Remove one random nop
        if(code.count(nopline) > 0):
            line = -1
            while(line == -1 or code[line] != nopline):
                line = random.randint(0, len(code)-1)
            code.pop(line)
            if(random.random() < 0.2):
                # Move it to start instead
                starts = (starts+1)%8
        else:
            no_change = True
    else:
        # Move a nop
        if(code.count(nopline) > 0):
            line = -1
            while(line == -1 or code[line] != nopline):
                line = random.randint(0, len(code)-1)
            code.pop(line)
            assert line == len(code) or is_code(code[line])
            nline = line
            options_down = []
            while nline < len(code) and len(options_down) < 6:
                nline += 1
                while(nline < len(code) and not is_code(code[nline])):
                    nline += 1
                if(random.random() < 0.5 ** len(options_down)):
                    options_down.append(nline)
            nline = line
            options_up = []
            while nline > 1 and len(options_up) < 6:
                nline -= 1
                while(nline > 1 and not is_code(code[nline])):
                    nline -= 1
                if(is_code(code[nline]) and random.random() < 0.5 ** len(options_up)):
                    options_up.append(nline)
            line = random.choice(options_down + options_up)
            code.insert(line, nopline)
        else:
            no_change = True

    for i in range(starts):
        code.insert(0, nopline)

    if(no_change or random.random() > 0.9):
        # Another change
        modify_code(code)

def noptimize(file, computer):
    with open(file, 'r') as f:
        original = f.readlines()

    stripped = [line.strip() for line in original]
    if(stripped.count(startstring) != 1 or stripped.count(stopstring) != 1):
        raise StartStopMarkersException(f"Need start and stop markers. Add lines \"{startstring}\" and \"{stopstring}\" around eliminate function.")
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
            score, cycles = computer.run(tmp_file, print_wa=False)
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
