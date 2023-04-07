# PReFScript: 
## A Partial Recursive Functions Lab

Rather: Towards a Partial Recursive Functions lab.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used as such.

Each function in a script has associated Gödel number, nickname, 
comments, and code; also, the last operation used to construct it.

Intended usage as of April 7, 2023 (for the names dp, pr_l, pr_r,
tup_e, tup_i, s_tup, pr see the companion repository 
`https://github.com/balqui/cantorpairs`):


```
>>> from prefscript import PReFScript
>>> my_fs = PReFScript() # to store my functions for this session
>>> my_fs.list()

k_1 
 The constant 1 function
 lambda x: 1
 Gödel number: 1 = <0.0>

id
 The identity function
 lambda x: x
 Gödel number: 2 = <0.1>

[...]

add
 Addition x+y of the two components of input <x.y>
 lambda z: cp.pr_l(z) + cp.pr_r(x) 
 Gödel number: 11 = <0.4>

[...] shows the basic functions that are always available from the beginning

>>> my_fs.define("pair", ("k_1", "k_1"), "const_pair_1", "The constant <1.1> function")
>>> my_fs.define("comp", ("add", "const_pair_1"), "k_2", "The constant 2 function")
>>> my_fs.list()

[...] as before but now includes the two newly defined functions

const_pair_1
 The constant <1.1> function
 lambda x: cp.dp(k_1(x), k_1(x))
 Gödel number: 31 = <2.5>

k_2
 The constant 2 function
 lambda x: add(const_pair_1(x))
 Gödel number: 419988 = <1.915>

>>> my_fs.list("k_2")

[...] lists only the constant 2 function (unsupported in the current version!)

>>> f = my_fs.to_python("k_2")
>>> f(8)
2
>>> 
```
