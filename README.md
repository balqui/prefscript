# PReFScript: 
## A Partial Recursive Functions Scripts Lab

Rather: Towards a Partial Recursive Functions lab.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528

Project started: mid Germinal 2003.

Current version: 0.5, mid Thermidor 2024.

Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used as such.

##### REWRITE THIS WHEN READY including the pipx thingy
Incomplete as of today, hence not pip-installable yet from PyPI
hosting. Install it instead, within a virtual environment, with:
`pip install --index-url https://test.pypi.org/simple/ --no-deps prefscript`
Alternatively, download the source file `prefscript.py` from the `src` folder.
Then, once within the Python interpreter, `from prefscript import PReFScript, cp`
provides the class for storing the script functions and an access named `cp` 
to `cantorpairs` functions, like `cp.dp(8, 4)`. Working on all that just these days.

A prefscript is a sequence of functions defined in terms of each
other and a few basic functions via the partial recursion rules 
of composition and minimization. All functions are from the
natural numbers into the natural numbers and may be undefined
for some inputs. In order to handle tuples or sequences of natural
numbers, a Cantor-like encoding is used (for information about the 
related names dp, pr_l, pr_r, tup_e, tup_i, s_tup, pr please see 
the companion repository `https://github.com/balqui/cantorpairs`).
The basic functions include projection variants, and a 
composition-like rule of pair formation is also available.

Scripts are maintained in objects of the class PReFScript,
that can be imported into your own Python program. 
A stand-alone interpreter is also provided. Thus, you
have available two main ways of programming in prefscript.

### Running the interpreter on a script in a text file

##### REWRITE THIS WHEN READY

INSTALLATION DEPENDING, run the command `prefscript --help`
as a first attempt or call directly `prefscript myscript`
after making sure that the working folder contains a text 
file `myscript.prfs` (omit the extension upon calling the
interpreter).

Function definitions in these scripts start with an arbitrary
integer (that might be useful for human readers to label and
reorder parts of the script) followed by the keyword "define:" 
(with the colon) and then, in sequence, the name of the function
being defined, a human-oriented description in square brackets,
and how it is constructed out of other functions in the script:
"pair" followed by two function names for the function that 
pairs their output up, "comp" followed by two function names 
for the composition function, and "mu" followed by a function
for defining a function by minimization.

```
10 define: piggyback_1
           [Pairs up input x with 1: <x.1> ]
           pair id k_1

20 define: ant
 [The predecessor or anterior function]
 comp diff piggyback_1

30 define: piggyback_ant
        [Pairs up x with its predecessor]
        pair id ant

   40      define:      sign
 [ Sign: 0 for 0, 1 for the rest ]     comp diff piggyback_ant

50 define: gt
           [whether x > y in input <x.y>]
           comp sign diff
```

The well-aligned format exemplified by cases 10 and 50 is not
compulsory, as can be seen in the other cases, but is highly
recommended. The repository includes a few examples of such files.

Alternatively, each line in the script may contain a directive.
Starting with `.about` indicates that the rest of the line is a 
human-oriented explanation; the directive `.import` followed by a
`filename` requires the interpreter to load in, at that point, 
the contents of `filename.prfs`; also the `.pragma` directives
are explained below. None of these directives is absolutely required.

#### Currently valid pragmas

As of the current version, the following directives are recognized:

`.pragma main:` followed by a name, will run as main program
the function with that name. If omitted, the function declared
last is run, preceded by a message to the effect.

`.pragma input:` followed by one of the keywords `int` (default),
`intseq` or `none`; specifying, respectively, that the input is
an `int` or a sequence of `int` or that no input will be read.
In the second case, the main function will receive a single `int`
encoding the whole sequence as per the `tup_i` encoding function
in `cantorpairs`.

`.pragma output:` followed by one of the keywords `int` (default)
or `bool` or `ascii`; in the two latter cases, the integer computed
by the main function will be converted into a Boolean value or a
7-bit ASCII string before being output.

`.pragma extended:` followed by value `False` (default) or `True`.

If `True` then a number of extensions are enabled, namely, the 
capabilities of defining functions as arbitrary ASCII constants, 
as `compair` compositions that merge into a shot a `pair` with a 
`comp` or as `primrec` for primitive recursion (faster than the 
dismal delay introduced by `mu`-based primitive recursion).

More precisely, `compair f g h` takes three function names and
forms an intermediate function as `pair g h` composing then `f`
with it; whereas `primrec f g h` defines a new function `s` by
course-of-values primitive recursion: for a given input `x`,
`f` tests `x` for being a base case, `g` is applied to `x` if
it is a base case (that is, when `f(x)` returned nonzero) and, 
in recursive cases, `h` is applied to a pair that has `x` as
left component and, as right component, a tuple containing 
all the values `s(x-1)`, `s(x-2)`, ..., `s(1)`, `s(0)`.






### Handling PReFScript objects directly

INSTALLATION PROCEDURE

The `define` method of PReFScript objects allows one to add 
new functions but I recommend the `dialog` method for a more
 amiable interface. Further examples of 
`define` are shown in file `uses_prefscript.py`.

Also, definitions contained in `.prfs` files
can be loaded in with the method `load`.

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

Each function in a PReFScript may have a Gödel number associated
(until it becomes too big) and also the last operation used 
to construct it. Then it has as well a nickname, a comment, 
and various forms of code, as indicated so far.
If the object initialization is made with

```
>>> my_fs = PReFScript("Store Gödel numbers")
```

then Gödel numbers of the functions will be provided until they
skyrocket to over about 300 decimal digits. Additional info about
the Python-callable codes is provided with `w_code = 2` in method
`list()`.


