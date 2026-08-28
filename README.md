# PReFScript: 
## Partial Recursive Functions for Scripting

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528

Project started: mid Germinal 2003.

Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used much as such.

Current version: 2.0, early Fructidor 2026. Previous 
documented, *incompatible* version: 1.2, mid Messidor 2026.

### Scripts

In PReFScript, a script is a sequence of functions defined 
in terms of each other and of a few basic functions via the 
partial recursion rules of composition and minimization. 
All functions are from the natural numbers into the natural 
numbers and may be undefined for some inputs. 

In order to handle tuples or sequences of natural numbers, 
a Cantor-like encoding is used; 
see <https://github.com/balqui/cantorpairs/blob/main/README.md>.

Specifically, the always available basic functions include: 
`k_1`, the constant 1 function;
`id`, the identity function;
addition and multiplication, `add` and `mul` respectively,
that interpret the single number received as the Cantor encoding
of a pair `<x.y>` and compute the corresponding operation on `x` and 
`y`; modified difference `diff` that receives likewise a Cantor-encoded
pair  `<x.y>` and computes `max(0, x - y)` so that we always stay
within the natural numbers; and two functions related to projections
of Cantor-encoded sequences.

### Installation and ways to use PReFScript functions

The usual `pip`-based process should work. Differently from
previous versions, all functionality in 2.0 is fully compatible
with a `pipx` installation. You may need to specify `--upgrade`
flags, depending on your previous installation. LLMs say that
`uv` should work as well.

The current version installs a stand-alone interpreter.
See [doc.md](https://github.com/balqui/prefscript/blob/main/docs/doc.md).

*The following applies to the previous version 1.2*:
Scripts were maintained in objects of the class PReFScript,
that could be imported into your own Python program. 
Thus, you had available two main ways of programming in 
PReFScript. All this does not apply anymore to version 2.0.


