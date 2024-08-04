# PReFScript: 
## A Partial Recursive Functions Scripts Lab

Rather: Towards a Partial Recursive Functions lab.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528

Project started: mid Germinal 2003.

Current version: 0.4, mid Thermidor 2024.

Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used as such.

Incomplete as of today, hence not pip-installable yet from PyPI
hosting. Install it instead, within a virtual environment, with:
`pip install --index-url https://test.pypi.org/simple/ --no-deps prefscript`
Alternatively, download the source file `prefscript.py` from the `src` folder.
Then, once within the Python interpreter, `from prefscript import PReFScript, cp`
provides the class for storing the script functions and an access named `cp` 
to `cantorpairs` functions, like `cp.dp(8, 4)`. Working on all that just these days.

### Defining Partial Recursive Functions directly

Each function in a PReFScript has associated a Gödel number
(until it becomes too big) and also the last operation used 
to construct it. Then it has as well a nickname, a comment, 
and various forms of code.

The `define` method allows one to add new functions but 
I recommend the `dialog` method for a more amiable interface
(for information about the names dp, pr_l, pr_r, tup_e, 
tup_i, s_tup, pr please see the companion repository 
`https://github.com/balqui/cantorpairs`). Further examples of 
`define` are shown in file `uses_prefscript.py`.

The `list` method without nicknames specified will list all 
the functions; or the one function matching the nickname if 
one is provided. Adding `w_code = 1` will give additional 
information.


```
>>> from prefscript import PReFScript
>>> my_fs = PReFScript() # to store my functions for this session
>>> my_fs.list()

k_1 
 The constant 1 function

id
 The identity function

[...]

add
 Addition x+y of the two components of input <x.y>

[...] shows the basic functions that are always available from the beginning

>>> my_fs.dialog()
Function nickname? const_pair_1
What is it? The constant <1.1> function
How is it made? [pair or comp or mu] pair
Applied to what? [1 or 2 space-sep names] k_1 k_1
>>>
>>> my_fs.dialog()
Function nickname? k_2
What is it? The constant 2 function
How is it made? [pair or comp or mu] comp
Applied to what? [1 or 2 space-sep names] add const_pair_1
>>>
>>> my_fs.list("const_pair_1")

const_pair_1
 The constant <1.1> function
>>> my_fs.list("const_pair_1", w_code = 1)

const_pair_1
 The constant <1.1> function
 pair: k_1 k_1
>>> 
>>> my_fs.list(w_code = 1)

[...] as before but now includes the two newly defined functions

const_pair_1
 The constant <1.1> function
 pair: k_1 k_1

k_2
 The constant 2 function
 comp: add const_pair_1

>>>
>>> f = my_fs.to_python("k_2") # gets a callable, working implementation
>>> f(8)
2
>>> 
```

If the object initialization is made with

```
>>> my_fs = PReFScript("Store Gödel numbers")
```

then Gödel numbers of the functions will be provided until they
skyrocket to over about 300 decimal digits. Additional info about
the Python-callable codes is provided with `w_code = 2`.


### Scripts containing definitions of Partial Recursive Functions

It is possible to load in a series of function definitions 
from a separate script file; I use these files with
extension .prfs (standing for "partial recursive functions script").
The repo includes some script files.

Function definitions in these scripts follow a format very similar 
to the one used in listing them. The main differences are the keyword
"define:" (with the colon) preceded by an optional integer, not having
a colon with the "pair" / "comp" / "mu" indication, and the square 
brackets encompassing the comment:

```
10 define: piggyback_1
           [Pairs up x with 1: <x.1> ]
           pair id k_1

20 define: ant
 [The ant function]
 comp diff piggyback_1

define: piggyback_ant
        [Pairs up x with its predecessor]
        pair id ant

   40 define: sign
 [ Sign: 0 for 0, 1 for the rest ]
     comp diff piggyback_ant

50 define: gt
           [x > y in <x.y>]
           comp sign diff
```

The well-aligned format exemplified by cases 10 and 50 is not
compulsory, as can be seen in the other cases, but is highly
recommended. Such files can be loaded in with the method `load`.
The repository includes a few examples of such files.
