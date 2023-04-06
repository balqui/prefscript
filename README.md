# PReFScript: 
## A Partial Recursive Functions Lab

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used as such.

Each function in a script has associated Gödel number, internal
name (string with the Gödel number), nickname, comments, and code.
The Gödel number is stored together with the last operation used 
to construct it.

Intended usage as of April 6, 2023:

```
>>> from prefscript import PReFScript
>>> my_fs = PReFScript() # to store my functions for this session
>>> my_fs.list()

id
 The identity function
 1 = <0.0>, prf_1
 lambda x: x

constant_1 
 The constant 1 function
 2 = <0.1>, prf_2
 lambda x: 1

add
 Addition of both components of input pair
 4 = <0.2>, 

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
