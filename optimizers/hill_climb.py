from computer import Computer, Cache, Memory
import random

choices = \
[
	[32, 64, 128], # instruction cache size
	[1, 2, 4, 8], # instruction cache block size
	[1, 2, 4], # instruction cache associativity

	[32, 64, 128], # data cache size
	[1, 2, 4, 8], # data cache block size
	[1, 2, 4], # data cache associativity

	[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], # write buffer size
	[(44,8), (30,6)] # memory access times
]

def get_choices(parameters):
	r = []
	for i in range(len(parameters)):
		r.append(choices[i][parameters[i]])
	return r

def build_computer(parameters):
	c = get_choices(parameters)
	return Computer(Cache(c[0], c[1], c[2]), Cache(c[3], c[4], c[5]), Memory(c[6], c[7][0], c[7][1]))

def evaluate(parameters, filename):
	return build_computer(parameters).run(filename)

def random_change(parameters, p=0.5):
	while 1:
		ind = random.randrange(len(parameters))
		parameters[ind] += random.choice([-1, 1])
		parameters[ind] = max(0, min(len(choices[ind])-1, parameters[ind]))
		if(random.random() < p): return

def distance(a, b):
	return sum(abs(x[0]-x[1]) for x in zip(a, b))

def hill_climb(filename, iterations=200):
	parameters = [len(c)//2 for c in choices]
	best_score, best_cycles = evaluate(parameters, filename)
	best_parameters = [*parameters]
	curr_score = best_score
	prev_print=0
	for i in range(iterations):
		new_parameters = [*parameters]
		random_change(new_parameters)
		dist = distance(parameters, new_parameters)
		if(dist == 0): continue
		score, cycles = evaluate(new_parameters, filename)
		if(score < curr_score or score/curr_score<1.02 and dist>=2):
			parameters = new_parameters
			curr_score = score
			if(score < best_score):
				best_score = score
				best_parameters = [*parameters]
				print("\n=== NEW BEST ===")
				print(build_computer(parameters))
				print("Cycles:", cycles)
				print("Score:", round(score, 2), "μsC$\n")
		p = int((i+1)/iterations*50)
		if(p != prev_print):
			print(str(p*2) + "%")
			prev_print = p

	best_computer = build_computer(best_parameters)
	print("\n\n=== BEST COMPUTER ===")
	print(best_computer)
	print("Cycles:", best_cycles)
	print("Score:", round(best_score, 3), "μsC$\n")

	return (best_score, best_computer)
