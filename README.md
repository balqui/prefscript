# PReFScript: 
## Partial Recursive Functions for Scripting

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528

Project started: mid Germinal 2003.

Current version: 1.0, late Thermidor 2024.

Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used much as such.

### Scripts

In PReFScript, a script is a sequence of functions defined in terms of each
other and of a few basic functions via the partial recursion rules 
of composition and minimization. All functions are from the
natural numbers into the natural numbers and may be undefined
for some inputs. In order to handle tuples or sequences of natural
numbers, a Cantor-like encoding is used.
The always available basic functions include: 
`k_1`, the constant 1 function;
`id`, the identity function;
addition and multiplication, `add` and `mul` respectively,
that interpret the single number received as the Cantor encoding
of a pair `<x.y>` and compute the corresponding operation on `x` and 
`y`; modified difference `diff` that receives likewise a Cantor-encoded
pair  `<x.y>` and computes `max(0, x - y)` so that we always stay
within the natural numbers; and two functions related to projections
of Cantor-encoded sequences.

Scripts are maintained in objects of the class PReFScript,
that can be imported into your own Python program. 
Alternatively, a stand-alone interpreter is also provided. 
Thus, you have available two main ways of programming in PReFScript.

### Installation and ways to use PReFScript functions

See doc.md for all the details (somewhat incomplete as of today).


