import subprocess
from struct import pack, unpack
import solution


class Cache:
	def __init__(self, size, block_size, associativity):
		assert(block_size in [1, 2, 4, 8])
		assert(size in [32, 64, 128])
		assert(associativity in [1, 2, 4])

		self.size = size
		self.block_size = block_size
		self.associativity = associativity
		self.block_count = size//block_size

		assert(associativity <= self.block_count)  # implied by above assertions

	def __str__(self):
		return f"{self.size} words \t{self.block_size} words/block \t{self.block_count} blocks \tassociativity {self.associativity}"

	def get_cost(self):
		if(self.size == 32):
			return 0
		if(self.size == 64):
			return 25
		if(self.size == 128):
			return 50
		raise Exception("Unexpected size")

	def get_max_clock(self):
		s = (self.size, self.associativity)
		if(s == (32, 1)):
			return 500
		if(s == (32, 2)):
			return 475
		if(s == (32, 4)):
			return 450
		if(s == (64, 1)):
			return 475
		if(s == (64, 2)):
			return 450
		if(s == (64, 4)):
			return 425
		if(s == (128, 1)):
			return 450
		if(s == (128, 2)):
			return 425
		if(s == (128, 4)):
			return 400
		raise Exception("Max clock not found")


class Memory:
	def __init__(self, write_buffer, first_access, next_access):
		assert(0 <= write_buffer <= 12)
		assert((first_access, next_access) in [(44, 8), (30, 6)])
		self.write_buffer = write_buffer
		self.first_access = first_access
		self.next_access = next_access

	def __str__(self):
		return f"{self.write_buffer} words buffer \t{self.first_access}/{self.next_access} access times"

	def get_cost(self):
		s = (self.first_access, self.next_access)
		buffer_cost = 3*self.write_buffer
		if(s == (44, 8)):
			return 50 + buffer_cost
		if(s == (30, 6)):
			return 100 + buffer_cost
		raise Exception("Memory cost not found")


class Computer:
	def __init__(self, instruction_cache, data_cache, memory):
		self.instruction_cache = instruction_cache
		self.data_cache = data_cache
		self.memory = memory

	def __str__(self):
		return(
			f"Instruction cache:\t{self.instruction_cache}\n"
			f"Data cache:\t\t{self.data_cache}\n"
			f"Memory:\t\t\t{self.memory}\n"
			f"Clock frequency:\t{self.get_clock()} MHz\n"
			f"Total cost:\t\t{self.get_cost()/100} C$"
		)

	def get_cmd_args(self):
		return(
			f"ibc{self.instruction_cache.block_count} ibs{self.instruction_cache.block_size} isa{self.instruction_cache.associativity} "
			f"dbc{self.data_cache.block_count} dbs{self.data_cache.block_size} dsa{self.data_cache.associativity} "
			f"wbs{self.memory.write_buffer} fwa{self.memory.first_access} nwa{self.memory.next_access}"
		)

	def get_clock(self):
		return min(self.instruction_cache.get_max_clock(), self.data_cache.get_max_clock())

	def get_cost(self):
		return 200 + self.instruction_cache.get_cost() + self.data_cache.get_cost() + self.memory.get_cost()

	def run(self, filename):
		args = self.get_cmd_args()
		result = subprocess.run(f"java -jar Mars.jar {filename} {args} me dump .data HexText out.txt".split(
		), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		returncode = result.returncode
		stdout = result.stdout.decode('utf-8')
		stderr = result.stderr.decode('utf-8')

		if(returncode == 5):
			raise Exception(f"Assembly error\n{stderr}")
		if(returncode == 6):
			raise Exception(f"Runtime error\n{stderr}")
		if('maximum step limit' in stderr):
			raise Exception(f"Inf loop?\n{stderr}")
		if(returncode != 0):
			raise Exception(f"Unexpected return code {returncode}\n{stderr}")

		a = stdout.split()
		L = []
		for s in a:
			f = unpack('f', pack('I', int(s, 16)))[0]  # convert hex string to float
			L.append(f)
		pos = 0
		while(pos+1 < len(L) and (L[pos] != 1.0 or abs(L[pos+1] - 0.47) > 0.01)):
			pos += 1
		L = L[pos:pos+24*24]
		for x, y in zip(L, solution.solution):
			if(abs(x - y) > 0.006):
				raise Exception("Wrong answer")

		cycles = int(a[-1])
		runtime = cycles/self.get_clock()  # μs
		cost = self.get_cost()/100

		return cost*runtime, cycles


def all_caches():
	for size in [32, 64, 128]:
		for blocksize in [1, 2, 4, 8]:
			for associativity in [1, 2, 4]:
				yield Cache(size, blocksize, associativity)


def all_memories():
	for write_buffer in range(13):
		for (fa, sa) in [(44, 8), (30, 6)]:
			yield Memory(write_buffer, fa, sa)


def all_computers():
	for instruction_cache in all_caches():
		for data_cache in all_caches():
			for memory in all_memories():
				yield Computer(instruction_cache, data_cache, memory)
