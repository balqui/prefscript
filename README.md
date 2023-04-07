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

Intended usage as of April 6, 2023 (for the names dp, pr_l, pr_r,
tup_e, tup_i, s_tup, pr see the companion repository 
`https://github.com/balqui/cantorpairs`):


```
>>> from prefscript import PReFScript
>>> my_fs = PReFScript() # to store my functions for this session
>>> my_fs.list()

id
 The identity function
 1 = <0.0>
 lambda x: x

constant_1 
 The constant 1 function
 2 = <0.1>
 lambda x: 1

add
 Addition of both components of input pair, lambda <x.y>: x + y
 4 = <0.2>
 lambda z: pr_l(z) + pr_r(x) 

[...] shows the basic functions that are available from the beginning

>>> my_fs.define("pair", ("constant_1", "constant_1"), "const_pair_1",
                 "The constant <1.1> function")
>>> my_fs.define("comp", ("add", "const_pair_1"), "constant_2",
                 "The constant 2 function")
>>> my_fs.list()

[...] as before but now includes the two newly defined functions

>>> my_fs.list("constant_2")

[...] lists only the constant_2 function

>>> f = my_fs.to_python("constant_2")
>>> f(8)
2
>>> 
```
