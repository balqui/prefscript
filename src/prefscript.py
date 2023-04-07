'''
PReFScript: A Partial Recursive Functions Lab

Rather: Towards a Partial Recursive Functions lab.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used as such.

Each function in a script has: associated Gödel number, internal
name (string with the Gödel number), nickname, comments, and code.
Gödel number stored with last operation used to construct it.
'''

import scaff.cantorpairs as cp
# ~ import cantorpairs as cp
from fundata import FunData

class PReFScript:

    def __init__(self):
        '''
        Dicts for storing the functions:
          main for the function data, key is Gödel number,
          nicks for connecting the Gödel number to the nick key,
          pycode for making them runnable, key is nick;
        include here the basic functions;
        their implementation assumes 'import cantorpairs as cp'
        '''
        self.main = dict()
        self.pycode = dict()
        self.nicks = dict()
        self.hownums = { "basic": 0, "comp": 1, "pair": 2, "mu": 3 }
        self.add_basic("k_1", "The constant 1 function", "lambda x: 1", 0)
        self.add_basic("id", "The identity function", "lambda x: x", 1)
        self.add_basic("s_tup", "Single-argument version of suffix tuple", 
                       "lambda x: cp.s_tup(cp.pr_l(x), cp.pr_r(x))", 2)
        self.add_basic("proj", "Single-argument version of projection", 
                       "lambda x: cp.pr(cp.pr_l(x), cp.pr_r(x))", 3)
        self.add_basic("add", "Addition x+y of the two components of input <x.y>", 
                       "lambda x: cp.pr_l(x) + cp.pr_r(x)", 4)
        self.add_basic("mul", "Multiplication x*y of the two components of input <x.y>", 
                       "lambda x: cp.pr_l(x) * cp.pr_r(x)", 5)
        self.add_basic("diff", "Modified difference max(0, x-y) of the two components of input <x.y>", 
                       "lambda x: max(0, cp.pr_l(x) - cp.pr_r(x))", 6)

    def add_basic(self, nick, comment, code, num):
        data = FunData()
        data["nick"] = nick
        data["comment"] = comment
        data["how_def"] = "basic"
        data["def_on"] = tuple()
        data["code"] = code
        gnum = cp.dp(0, num)
        self.nicks[nick] = gnum
        self.main[gnum] = data
        self.pycode[nick] = eval(code, globals() | self.pycode)

    def list(self, what = None, verbose = False):
        'if what == None: list everything, o/w search for what on the dicts'
        pass

    def define(self, how, on_what, nick, comment):
        'new function to add to the dicts appropriately'
        if nick in self.nicks:
            print("Nickname " + nick + " already in use. New definition ignored.")
            return None
        numhow = self.hownums[how]
        if numhow == 0:
            print("Addition of basic functions unsupported as yet. New definition ignored.")
            return None            
        if numhow == 3:
            print("Minimization is still unsupported right now. New definition ignored.")
            return None            
        data = FunData()
        data["nick"] = nick
        data["comment"] = comment
        data["how_def"] = how
        data["def_on"] = on_what
        if numhow in (1, 2):
            lft = self.nicks[on_what[0]]
            rgt = self.nicks[on_what[1]]
            gnum = cp.dp(numhow, cp.dp(lft, rgt))
        else:
            'numhow is 3, minimization, unsupported right now'
            pass
        if numhow == 1:
            'composition'
            data["code"] = "lambda x: " + on_what[0] + "(" + on_what[1] + "(x))"
        if numhow == 2:
            'pairing'
            data["code"] = "lambda x: cp.dp(" + on_what[0] + "(x), " + on_what[1] + "(x))"
        self.nicks[nick] = gnum
        self.main[gnum] = data
        self.pycode[nick] = eval(data["code"], globals() | self.pycode)

    def to_python(self, what):
        'returns a Python-runnable version of the function'
        if what not in self.pycode:
            print("Nickname " + what + " not defined.")
            return None
        return self.pycode[what]

