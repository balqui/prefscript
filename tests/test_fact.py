from time import process_time
from prefscript import PReFScript
import scaff.cantorpairs as cp

ff = PReFScript()
ff.load("fact_00.prfs")
f = ff.to_python("fact")

def t(n):
	try:
		start = process_time()
		r = f(n)
		tm = process_time() - start
	except:
		print(f"Stopped; time: {1000*(process_time() - start):3.6f} ms")
	print(f"Outcome: {r}; time: {1000*(tm):3.6f} ms")

t(int(input("n: ")))


