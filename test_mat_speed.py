import numpy as np
from timeit import default_timer as timer

if __name__ == '__main__':
	arr = np.random.rand(320,240,3)
	start_t = timer()
	for i in range(10):
		arr += i
	end_t = timer()
	print("iterating numpy array 10 times takes {0}s".format(end_t-start_t))
