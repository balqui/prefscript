'''
Exploring primitive recursion...
'''

import cantorpairs as cp

def pr_LR(x):
	return cp.pr_L(cp.pr_R(x))

for i in range(5, 500):
	if pr_LR(i) != cp.pr(i, 1):
		print(pr_LR(i), cp.pr(i, 1))

def prim_rec_py(base_lim, base, recurse):
	"primitive recursion more efficient than by minimization"

	def c_of_v(x):
		"create the full course of values"
		sq = 0
		for y in range(x + 1):
			new = base(y) if y <= base_lim else recurse(cp.dp(y, sq))
			sq = cp.dp(new, sq)
		return sq

	return lambda x: cp.pr_L(c_of_v(x))

frec = lambda t: cp.pr_L(t) * pr_LR(t)
k_1 = lambda t: 1

f = prim_rec_py(1, k_1, frec)

run = 1
for i in range(10):
	print(i, f(i), run)
	run *= i + 1
print(run)

