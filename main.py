
from computer import *

import optimizers

filename = '../gauss.s'

#computer, score = optimizers.exhaustive(filename)
computer, score = optimizers.hill_climb(filename, 100)

