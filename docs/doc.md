# PReFScript: 
## Partial Recursive Functions for Scripting

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528

Documentation for version: 1.1

Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used much as such.

### Installation

There are two installation options.

#### Installing only the stand-alone interpreter

Make sure you have `pipx`; then, installation proceeds 
in the standard manner: `pipx install prefscript` 
will create a command `prefscript` that you can call 
from the command line. It is suggested that
your very first call is `prefscript --help`.

If you don't have `pipx` yet, installing it globally 
via `pip` should be possible but may require you to 
accept responsibility for mixing up `apt`-installed 
things with `pip`-installed things. The option of 
installing `pipx` in a virtual environment will leave 
the global environment without it; another possibility 
on Ubuntu/Debian is to install `pipx` via `apt`.

This installation form is appropriate if you plan only
to run the interpreter on third-party PReFScript files 
or if you are already familiar with this particular form 
of functional programming. To learn to write scripts of
partial recursive functions and understand well that
formal model of computation, the next installation 
option may be preferable.

<!--- 

On Windows it will be also 
possible to launch a minimal GUI hopefully in the near future.

Then test whether it brought in pytokr and cantorpairs
in an importable form, which I guess it would not, and whether
it is importable, which again I guess it would not be.

---> 

#### Installing the system in an importable form

Use the usual mechanism `pip install prefscript`
(maybe preceded by super-user identification).
This way, besides making the interpreter available
as described in the previous section, you will be 
able to `import prefscript` into your own code.

It is recommended that the installation is made in a
virtual environment. It will install as well the module
`pytokr` unless it is already installed. If you have
`pytokr` already in a virtual environment, consider 
using the same environment to install also `prefscript`.

It may be easier to learn to use PReFScript by installing
it in this way and then importing its main objects as
explained below, rather than from the stand-alone interpreter.

<!--- 

Again, all this to be tested.

##### REWRITE THIS WHEN READY including the pipx thingy
Incomplete as of today, hence not pip-installable yet from PyPI
hosting. Install it instead, within a virtual environment, with:
`pip install --index-url https://test.pypi.org/simple/ --no-deps prefscript`
Then, once within the Python interpreter, `from prefscript import PReFScript, cp`
provides the class for storing the script functions and an access named `cp` 
to `cantorpairs` functions, like `cp.dp(8, 4)`. Working on all that just these days.

(for information about the 
related names `dp`, `pr_l`, `pr_r`, `tup_e`, `tup_i`, `s_tup`, `pr` 
please see the companion repository `https://github.com/balqui/cantorpairs`).
The basic functions include projection variants, and a 
composition-like rule of pair formation is also available.

CHECK OUT THE CAPITAL L AND R IN THE cp FUNCTIONS !!!

---> 

### Elementary notions

In PReFScript, a script is a sequence of functions, each defined 
in terms of the previous ones and of a few basic functions via the 
partial recursion rules of composition and minimization. 

All functions are from the natural numbers into the natural numbers 
and may be undefined for some inputs. In order to handle tuples or 
sequences of natural numbers, a Cantor-like encoding is used. 

#### Cantor-like encoding

Before proceeding to our form of partial recursive functions,
please see first the companion repository 
[cantorpairs](https://github.com/balqui/cantorpairs).
Its README file describes the available functions and their usages.
It is a submodule of `prefscript` and provides the
related names `dp`, `pr_L`, `pr_R`, `tup_e`, `tup_i`, `s_tup`, `pr`
as described there.

#### Basic partial recursive functions

The always available basic functions include: 
`k_1`, the constant 1 function;
`id`, the identity function;
addition and multiplication, `add` and `mul` respectively,
that interpret the single number received as the Cantor encoding
of a pair `<x.y>` and compute the corresponding operation on `x` and 
`y`; modified difference `diff` that receives likewise a Cantor-encoded
pair  `<x.y>` and computes `max(0, x - y)` so that we always stay
within the natural numbers; and two functions related to projections
of Cantor-encoded sequences: the projection function `proj` and
the suffix tuple function `s_tup`.

An extended variant of the system allows for some more basic functions:
see below under Directives.

#### Combining functions into new ones

Two of the traditional ways of constructing partial recursive
functions are composition and mu-minimization (or: linear search,
in more modern terminology). In PReFScript, all functions take
a single natural number as argument and, if they are defined,
return a single natural number. This departs from the original
definition where families of different arities were to be
defined, with unmanageable cases of indexitis. Here, whenever
a function is conceived as taking two arguments (like addition,
for one, `add(x, y) = x + y`) it receives instead a single value
that can be interpreted as the encoding of a pair:
`add(z) = x + y` where `z = <x.y>`.

Thus, composition works in the fully standard way: if `h` is
defined by composition of `f` and `g` (noted here as `comp f g`)
then `h(n) = f(g(n))` if `g(n)` is defined and if `f` is defined
on that value. _Evaluation is eager_. (Fans of lazy evaluation 
may work on Haskell instead.)

The minimization operator takes a test function `f` and creates
a new function `h = mu f` implementing linear search over `f`.
More precisely, `h(x)` is computed by testing, in turn, all the
values `f(<x.0>)`, `f(<x.1>)`, `f(<x.2>)`, and so on, until 
finding a value `k` such that `f(<x.k>)` is nonzero: then `h(x) = k`.

In `mu f` one expects `f` to be a predicate, that is, a total
function that only evaluates to 0 or 1. If one of the intermediate
tests `f(<x.j>)` turns out to be undefined before reaching
the `k` searched for, then `h(x)` is undefined. Nonzero values
of `f` are treated as 1.

A slightly nonstandard addition to the partial recursive function schemes
is necessary to handle everything as single natural numbers, 
namely, given two functions `f` and `g`, computing a single
value pairing up both outputs: it is expressed as `pair f g`
and defines a function `h` such that `h(x) = <f(x).g(x)>`. 

The traditional scheme of primitive recursion is available in
an extended version of `prefscript`; see below under Directives.

### Running the interpreter on a script in a text file

Function definitions in these scripts start with an _arbitrary
natural number_ (that might be useful for human readers to label and
reorder parts of the script) followed by the keyword "define:" 
(with the colon) and then, in sequence, the _name_ of the function
being defined, a human-oriented description in square brackets,
and _how_ it is constructed out of _other previously defined 
functions_ in the script:
"pair" followed by two function names for the function that 
pairs their output up, "comp" followed by two function names 
for the composition function, or "mu" followed by a test function
in order to define a function by minimization (linear search).

Names must be Python identifiers: they consist of letters, numbers,
or underscores and cannot start with a number.

Hence, if the contents of file `myscript.prfs` is, say,

```
10 define: piggyback_1
           [Pairs up input x with 1: <x.1> ]
           pair id k_1

20 define: ant
 [The predecessor or anterior function, maps 0 to 0 and x to x-1 if nonzero]
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

then you can run the command `prefscript myscript`
(note that the `.prfs` extension is omitted upon 
calling the interpreter). It will warn you that
the last function defined `gt` is taken as main 
program and will be expecting numbers that encode
pairs `<x.y>` to answer 0 or 1 according to whether
`x > y`. The option `prefscript --help` is also available.

The well-aligned format exemplified by cases 10 and 50 is not
compulsory, as can be seen in the other cases, but is highly
recommended. The repository includes a few examples of such files.

See below under Directives for how to avoid the annoying message 
about the assumed main function and for additional useful extensions.

### Importing PReFScript objects

Scripts are maintained in objects of the class PReFScript,
that can be imported into your own Python program. 
Thus, you have available two main ways of programming in 
PReFScript: through the stand-alone interpreter as described
or by handling the scripts internals yourself. 

If the installation was made with `pip` instead of `pipx`,
simply import the class:

```
>>> from prefscript import PReFScript
>>> my_fs = PReFScript() # to store my functions for this session
```

You are likely to want to import as well the `cantorpairs` module
so that you have available the auxiliary tuping functions
mentioned earlier; one way to do this is:

```
>>> from prefscript import PReFScript, cantorpairs as cp
```

#### Handling PReFScript objects directly

The `define` method of PReFScript objects allows one to add 
new functions but I recommend the `dialog` method for a more
amiable interface. 
 
Also, definitions contained in `.prfs` files
can be loaded in with the method `load`; there, 
all the previous (and forthcoming) considerations 
given for script files apply.

The `list` method without names specified will list all 
the functions; or the one function matching the name if 
one is provided. Adding `w_code = 1` will give additional 
information.

```
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
Function name? const_pair_1
What is it? The constant <1.1> function
How is it made? [pair or comp or mu] pair
Applied to what? [1 or 2 space-sep names] k_1 k_1
>>>
>>> my_fs.dialog()
Function name? k_2
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
to construct it. Then it has as well a name, a comment, 
and various forms of code, as indicated so far.
If the object initialization is made with

```
>>> my_fs = PReFScript("Store Gödel numbers")
```

then Gödel numbers of the functions will be provided until they
skyrocket to over about 300 decimal digits. Additional info about
the Python-callable codes is provided with `w_code = 2` in method
`list()`.


### Directives

Lines in a `.prfs` script may contain directives.
Starting the line with `.about` indicates that the rest of the line is a 
human-oriented explanation; the directive `.import` followed by a
`filename` requires the interpreter to load in, at that point, 
the contents of `filename.prfs`; and the `.pragma` directives
are explained next. None of these directives is absolutely required.

#### Currently valid pragmas

As of the current version, the following directives are recognized:

`.pragma main:` followed by a name, will run as main program
the function with that name. If omitted, the function declared
last is run, preceded by a message to the effect.

`.pragma input:` followed by one of the keywords `int` (default)
or `intseq` or `none`; specifying, respectively, that the input is
an `int`, or a sequence of `int`, or that no input will be read.
In the second case, the main function will receive a single `int`
encoding the whole sequence as per the `tup_i` encoding function
in `cantorpairs`; the user must mark the end of the sequence in
the usual way (ctrl-D).

`.pragma output:` followed by one of the keywords `int` (default)
or `bool` or `ascii`; in the two latter cases, the integer computed
by the main function will be converted into a Boolean value or a
7-bit ASCII string before being output.

`.pragma extended:` followed by value `False` (default) or `True`.

If `True` then a number of extensions are enabled, namely, the 
capabilities of defining functions as arbitrary ASCII constants, 
as `compair` compositions that merge into a single shot a `pair` 
with a `comp`, or as `primrec` for primitive recursion (faster 
than the dismal delay introduced by `mu`-based primitive recursion).

More precisely, `compair f g h` takes three function names and
forms an intermediate function as `pair g h` composing then `f`
with it; whereas `primrec f g h` defines a new function `s` by
_course-of-values primitive recursion:_ for a given input `x`,
`f` tests `x` for being a base case, `g` is applied to `x` if
it is a base case (that is, when `f(x)` returned nonzero) and, 
in recursive cases, `h` is applied to a pair that has `x` as
left component and, as right component, a tuple containing 
all the values `s(x-1)`, `s(x-2)`, ..., `s(1)`, `s(0)`.



