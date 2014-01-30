import random

def fuzz(n=4):
	return 'fuzz'.join(random.choice('barney') for i in range(n))