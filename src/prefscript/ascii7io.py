'''
Project started mid Germinal 2023:
PReFScript: A Partial Recursive Functions Lab

Ancillary module, early Thermidor 2024:
Single-integer encoding and decoding of (printable) 7-bit ASCII strings
Currently employed for versions up to 1.2, this docstring expanded 
by mid Messidor 2026 with no change to code.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

TWO_pow_7 = 1 << 7

def str2int(s):
	'integer from any string, even with nonprintable chars'
	r = 0
	for c in s:
		r = r * TWO_pow_7 + ord(c)
	return r

def int2raw_str(n):
	'string from any integer, even with nonprintable chars'
	r = list()
	while n > 0:
		r.append(chr(n % TWO_pow_7))
		n //= TWO_pow_7
	return ''.join(reversed(r))

def int2str(n):
	'string from any integer, nonprintable chars replaced by underscores'
	r = list()
	while n > 0:
		c = n % TWO_pow_7
		if 31 < c:
			r.append(chr(c))
		else:
			r.append('_')
		n //= TWO_pow_7
	return ''.join(reversed(r))

if __name__ == "__main__":
	print(TWO_pow_7)
	for s in ['', 'a', 'aa', 'abcde']:
		n =  str2int(s)
		print(s, n, int2str(n))
	print(hw := str2int("Hello, World!"))
	print(int2raw_str(hw))
	print(int2str(hw))
	for i in range(10000, 100000): print(int2str(i*103), end = ' ')
	
