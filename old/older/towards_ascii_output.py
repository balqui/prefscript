'''
Exploring arbitrary constants and ascii output...
'''

# ~ import cantorpairs as cp

# ~ def pr_LR(x):
	# ~ return cp.pr_L(cp.pr_R(x))

TWO_pow_7 = 1 << 7

def str2int(s):
	r = 0
	for c in s:
		r = r * TWO_pow_7 + ord(c)
	return r

def int2str(n):
	r = list()
	while n > 0:
		r.append(chr(n % TWO_pow_7))
		n //= TWO_pow_7
	return ''.join(reversed(r))

def int2pr_str(n):
	r = list()
	while n > 0:
		c = n % TWO_pow_7
		# ~ print(n, c, chr(c))
		if 31 < c:
			r.append(chr(c))
		else:
			r.append('_')
		n //= TWO_pow_7
	return ''.join(reversed(r))

print(TWO_pow_7)
for s in ['', 'a', 'aa', 'abcde']:
	n =  str2int(s)
	print(s, n, int2str(n))
print(hw := str2int("Hello, World!"))
print(int2pr_str(hw))
print(int2str(hw))
# ~ for i in range(10000): print(int2pr_str(i*23), end = ' ')
