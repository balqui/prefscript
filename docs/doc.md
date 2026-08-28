# PReFScript: 
## Partial Recursive Functions for Scripting

Author: José Luis Balcázar, ORCID 0000-0003-4248-4528

Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with 
partial recursive functions; naturally doubles as a (stateless, 
purely functional) programming language, although it is not 
intended to be used much as such.

Documentation for version: 2.0, **not** backwards-compatible.

Deprecated documentation for previous versions can be found in
[doc_v1.md](https://github.com/balqui/prefscript/blob/main/docs/doc_v1.md).


### Installation

The usual options should work: pipx (less fussy), pip (which might 
complain about breaking system packages), or uv. Version 2.0 offers
only functionality compatible with pipx, a feature in which it differs
from V1.*.

The install command will create a command `prefscript` that you can 
call from the command line. It is suggested that your very first call 
is `prefscript --help`.


<!--- 

Make sure some example scripts become available.

On Windows it will be also 
possible to launch a minimal GUI hopefully in the near future.

Test whether it brought in pytokr and cantorpairs
in an importable form, also if pytokr wasn't there
and maybe now is, stand-alone.

Think how to avoid the no-main pragma complaint upon importing.

Mention somewhere that repeated consistent definitions are ignored.

TEST: `pip install --index-url https://test.pypi.org/simple/ --no-deps prefscript`

FROM V1 DOCS:

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

 = = =
 
An extended variant of the system allows for some more basic functions:
see below under Directives.

 = = =
 
The traditional scheme of primitive recursion is available in
an extended version of `prefscript`; see below under Directives.


---> 



### Elementary notions

In PReFScript, a script is a sequence of functions, each defined 
in terms of others and of a few basic functions via the 
partial recursion rules of composition and minimization. 

All functions are from the natural numbers into the natural numbers 
and may be undefined for some inputs. In order to handle tuples or 
sequences of natural numbers, a Cantor-like encoding is used. 

#### Cantor-like encoding

Before proceeding to our form of partial recursive functions,
please see first the companion repository 
[`cantorpairs`](https://github.com/balqui/cantorpairs).
Its README file describes the available functions and their usages.
It is a submodule of `prefscript` and provides the
related names `dp`, `pr_L`, `pr_R`, `tup_e`, `tup_i`, `s_tup`, `pr`, `seq`
as described there.

#### Basic partial recursive functions

The always available basic functions include: 

- `k_1`, the constant 1 function;

- `id`, the identity function;

- addition and multiplication, `add` and `mul` respectively,
that interpret the single number received as the Cantor encoding
of a pair `<x.y>` and compute the corresponding operation on `x` and 
`y`; 

- modified difference `diff` that receives likewise a Cantor-encoded
pair  `<x.y>` and computes `max(0, x - y)` so that we always stay
within the natural numbers; and 

- two functions related to projections
of Cantor-encoded sequences: the projection function `proj` and
the suffix tuple function `s_tup`.

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
on that value. 
The minimization operator takes a test function `f` and creates
a new function `h = mu f` implementing linear search over `f`.
More precisely, `h(x)` is computed by testing, in turn, all the
values `f(<x.0>)`, `f(<x.1>)`, `f(<x.2>)`, and so on, until 
finding a value `k` such that `f(<x.k>)` is nonzero: then `h(x) = k`.
In `mu f` one expects `f` to be a predicate, that is, a total
function that only evaluates to 0 or 1. However, nonzero values
of `f` are treated as 1.

A slightly nonstandard addition to the partial recursive function schemes
is necessary to handle everything as single natural numbers, 
namely, given two functions `f` and `g`, computing a single
value pairing up both outputs: it is expressed as `pair f g`
and defines a function `h` such that `h(x) = <f(x).g(x)>`. 

_Evaluation is eager_: an undefined value at any intermediate step
leads to the finally desired value remaining undefined. 
That is, if `h(n) = f(g(n))` and `g(n)` is undefined then
`h(n)` is undefined, and if one of the intermediate
tests `f(<x.j>)` of a minimization turns out to be undefined 
before reaching the `k` searched for, then `h(x)` is undefined. 

A form of the so-called _primitive recursion_ is also available. Whereas it can
be proved that it is redundant in the presence of the given 
schemes, its lack leads to some computations being inadmissibly
slow. We postpone briefly the discussion of this point.

### Running the interpreter on a script in a text file

Scripts contain mainly function definitions.

They may contain as well comments and docstrings, starting 
at either the mark `#` or the mark `\\` and spanning until 
the end of the line. They may contain also `#pragma` instructions, 
handled by an ad-hoc preprocessor and explained below, and the 
word `import` followed by a filename in double quotes: it will 
search for a script of that name, adding the ".prfs" extension 
if necessary, and will read and have subsequently available all 
the function definitions there. It is expected that many uses
will be `import "std"` which will bring in all the function
definitions in the file `std.prfs` provided at installation
time in a folder under the name `stdprfs`.

Scripts intended to be run must include a function definition
under the name `main`. In scripts that become imported into
other scripts, that name is silently ignored. Running a script
amounts to calling that `main` function, feeding it a value 
read from standard input.

Function definitions in these scripts are syntactically very simple:
a name for the function followed by a colon, followed by zero or
more docstrings in double quotes, finally followed by a specification
of how the function is defined. Specifications can be other function
names (thus creating aliases, that is, different names of the same 
function) or the keywords `comp`, `pair`, `mu`, or `rec` (this last 
one to be clarified below) followed by the adequate number of function 
specifications: two for `comp` and `pair`, one for `mu` (the test 
function), and three for `rec`.

Parentheses surrounding any function specification are always allowed
but never compulsory; users can employ them at will to clarify their code.
Parentheses surrounding anything that does not conform syntactically
to a function specification are disallowed.

From a CLI (command line interface) simply call the `prefscript`
interpreter followed by the name of the file containing the script.
The file extension is assumed to be `.prfs` if nonexistent. 
CLI flags are available for 
fine-tuning: `-R`, `--read` changes the criterion by which input 
is read; `-W`, `--write` changes the criterion by which output 
is written. Allowed values can be inspected by calling 
`prefscript --help`. Also `-I`, `--import_folder` allows one 
to specify where additional, necessary function definitions can be found. These
three flags can be also handled from pragmas within the source
code (see below).

Additional flags are `-P`, `--show_parsing` that shows the 
abstract syntax tree of the script and `-G`, `--Goedel_nums`
that will provide Gödel numbers of the functions until they
skyrocket to over about 300 decimal digits (1000 bits actually). 
In both cases, the task is done without running the script. 

### Recursion

The `rec f g h` construction implements so-called _parameterized 
course-of-values primitive recursion_. Let's switch to better names:
the function defined by `rec recurse base is_base` receives an
integer `z`, tests it to distinguish recursion basis from recursion
step, and proceeds accordingly.

For the test and basis, `z` is interpreted as a pair `<param.input>`, 
where the input part is the actual inductive value and the 
parameter provides extra information. Then, `is_base` is
likely to need to test only `pr_R`, leaving the `param` out
(an example follows momentarily).

If the outcome of `is_base` is true (that is, nonzero), `z` is 
considered to be a basis case and the result is computed 
as `base(z)`; otherwise, the function `recurse` is applied to 
a pair consisting of `z` and the whole
sequence of values of the function itself that is being defined 
for all pairs `<param.val>` for `val` between 0 and `input-1`, 
leaving `param` always invariant. Using these values, `recurse`
must obtain the value of the function for `z = <param.input>`.

As an example (somewhat incomplete in that some simple 
but not basic functions are still missing, such as the 
constant 0 function `k_0`, the `gt` comparison or the 
left and right projections) we see how to define the 
addition via recursion on top of the "add one"
function `succ`. The main function is `add_recurs`, the 
recursive version of addition, which gets `<x.y>` and must
find `x+y` via a recursive construction. Arbitrarily we
assign roles: `x` remains as parameter, `y` is taken as 
inductive variable. To check the base case, `is_zero_R` 
checks that the right-hand side of the input number is
`y == 0`, and then the sum to be computed is `x`, its
left-hand side.

The recursive step `add_1_to_prev` gets `<<x.y>.sq>` as input, 
where `sq` is the whole course-of-values sequence; that is,
`<(x+(y-1)).(x+(y-2)). ... .(x+0)>`. This function must take 
the most recent one and add 1 to it: a call to `pr_R` 
selects `sq`, then the composition with `pr_L` fetches its 
leftmost value, namely `x+y-1`, to which we must add 1.

'''

main: add_recurs

add_recurs:
    rec add_1_to_prev base_case is_zero

is_zero_R:
    comp neg (comp gt pair pr_R k_0)

base_case:
    "gets called on <x.y> when y is zero hence sum is x"
    pr_L

add_1_to_prev:
    comp succ comp pr_L pr_R

'''

<!--- 

EXAMPLES!

ISSUE: IMPORT FOLDER SHOULD BE INCREMENTAL

---> 

### Preprocessor directives

These are used to provide default values to the command line flags
`-R`, `--read`,
`-W`, `--write`, and
`-I`, `--import_folder`. They will be superseded in case the 
corresponding CLI flags are present. Thus, for each of these
three options, there is a default in case neither pragmas nor
CLI flags apply (namely, `int`, `int`, and `stdprfs`); if exactly
one of them, pragma or flag, is present, it is enforced; and
if both are present, the `#pragma` declaration is ignored,
being inhibited by the CLI flag.
Call `prefscript --help` to see the allowed pragma values.



<!--- 

start with an _arbitrary
natural number_ (that might be useful for human readers to label and
reorder parts of the script) followed by the keyword "define:" 
(with the colon) and then, in sequence, the _name_ of the function
being defined, a human-oriented description in square brackets,
and _how_ it is constructed out of other functions in the script:
"pair" followed by two function names for the function that 
pairs their output up, "comp" followed by two function names 
for the composition function, or "mu" followed by a test function
in order to define a function by minimization (linear search
as described above).

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
recommended. The repository includes 
[`a few examples`](https://github.com/balqui/prefscript/tree/main/examples)
of such files, some intended to be imported from other files.

Add a first line with the contents `.pragma main: sign` to
run instead the function `sign` and omit the warning. 
See below under Directives for why this avoids the 
annoying message about the assumed main function, for 
how to import other scripts from separate files, and 
for additional useful extensions.

### Importing PReFScript objects

Scripts are maintained in objects of the class `PReFScript`,
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
so that you have available the auxiliary tupling functions
mentioned earlier; one way to do this is:

```
>>> from prefscript import PReFScript, cp
```

where `cantorpairs` gets renamed `cp` as inside `prefscript`
(but `import cantorpairs` would work as well).
 
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

[...] (shows the basic functions that are always available from the beginning)

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

[...] (as before but now includes the two newly defined functions)

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
the contents of `filename.prfs` (expected to reside in the working folder); 
and the `.pragma` directives
are explained next. None of these directives is absolutely required.
Useful examples may be `hw.prfs` and `is_pyth_02.prfs` in the `examples`
folder.

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
the usual way (ctrl-D on Linux). Remember that all integers in PReFScript
are unsigned (that is, natural numbers): negative values are
disallowed.

`.pragma output:` followed by one of the keywords `int` (default)
or `bool` or `ascii`; in the two latter cases, the integer computed
by the main function will be converted into a Boolean value or a
7-bit ASCII string before being output.

`.pragma extended:` followed by value `False` (default) or `True`.

If `True` then a number of extensions are enabled, namely: first, 
the capability of defining functions as arbitrary ASCII constants
or as `compair` compositions that merge into a single shot a `pair` 
with a `comp`: `compair f g h` takes three function names and
forms an intermediate function as `pair g h` composing then `f`
with it.

Second, the capability of defining functions as possibly 
parameterized primitive recursion, faster than the dismal 
delay introduced by its equivalence via `mu`-based primitive 
recursion.
 
More precisely, `primrec f g h` defines a new function `s` by
_course-of-values primitive recursion:_ for a given input `x`,
`f` tests `x` for being a base case, `g` is applied to `x` if
it is a base case (that is, when `f(x)` returned nonzero) and, 
in recursive cases, `h` is applied to a pair that has `x` as
left component and, as right component, a tuple containing 
all the values `s(x-1)`, `s(x-2)`, ..., `s(1)`, `s(0)`.

Its parameterized version `parprimrec f g h` is almost the
same, only that not _all_ of the input `x` is employed to
construct the sequence of values: the recursion traverses
only `pr_R(x)`, which is also the part tested for base cases, 
leaving room in `pr_L(x)` for an invariant parameter. 
All the while, the whole of `x` is used to call both 
the `base` and the `recurse` functions to which, hence,
both parts are available. Thus, for example, for 
`zero: comp neg sign` which tests for zero, applied 
to `pr_R(x)`, the constant `k_1` when `pr_R(x)` is zero,
and otherwise applying
`step: comp mul pair pr_LL pr_LR` one obtains the
exponential: the value `pr_L(x)` (the parameter) 
raised to the power `pr_R(x)`
(part traversed by the sequence of values): 
when `pr_R(x)`, the desired exponent, is zero,
we obtain 1 and, otherwise, the `step` recursion
is given the pair of `x` and the current sequence of values,
`<x.s>`, gets the base as `pr_LL: comp pr_L pr_L`, 
gets the power to one unit less in the exponent 
as the most recent addition to `s`, `pr_LR: comp pr_L pr_R`,
and simply multiplies them together. Standard primitive
recursion is able to do the job but causes some headaches
to fish up the right values hidden somewhere along a much
bigger sequence of values. Example files of all these
variants are provided in the 
[`examples`](https://github.com/balqui/prefscript/tree/main/examples)
folder.


### About the current version

Up to version v1.1, functions were to be constructed out of 
other _previously defined_ functions in the script. The
current version allows for any ordering of the functions
in the script. Parameterized primitive recursion is also
only possible in the current version, which will be also
less fussy and complain less as warnings have been reduced.
The current version has seen also quite some refactoring
of the source code, with a view to the future, planned
version 2.0 which we hope to ship out by the early fall
of 2026.


---> 
