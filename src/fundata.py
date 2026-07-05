'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module:
fundata: class FunData storing all necessary information about 
one function, includes as well ancillary algorithms mu and prim_rec
(file distribution slight refactoring on the monolithic design of Thermidor 2004)

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Each function in a script has: associated Gödel number, nickname, 
comments, and code (string); also, the last operation used to 
construct it. Then, in a separate dict at script level (and used 
as namespace for eval calls), a runnable version of the code.

Nicknames are alphanum strings not starting with a number (no surprise).
'''

import cantorpairs as cp

# ~ from collections import defaultdict as ddict
# ~ from re import compile as re_compile, finditer as re_finditer
# ~ from ascii7io import int2str, str2int, int2raw_str # users are not expected to need int2raw_str
# ~ import cantorpairs
# ~ cp = cantorpairs

# ~ from v1parser import Parser, SyntErr

__version__ = "1.2"

class FunData(dict):
    'Simple class for PReFScript functions data'

    def __init__(self, nick = None, comment = None, how_def = None, def_on = None):
        dict.__init__(self)
        self["nick"] = nick # function name
        self["comment"] = comment
        self["how_def"] = how_def
        self["def_on"] = def_on

    def __str__(self):
        return self["nick"] + "\n " + self["comment"] 

    def how_def(self):
        if self["how_def"] == "basic":
            return "basic"
        return self["how_def"] + ": " + ' '.join(on_what for on_what in self["def_on"])


