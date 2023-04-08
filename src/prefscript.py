'''
PReFScript: A Partial Recursive Functions Lab

Rather: Towards a Partial Recursive Functions lab.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used as such.

Each function in a script has: associated Gödel number, nickname, 
comments, and code (string); also, the last operation used to 
construct it. Then, in a separate dict (used as namespace for 
eval calls), a runnable version of the code.
'''

import scaff.cantorpairs as cp
# ~ import cantorpairs as cp
from fundata import FunData


def mu(x, test):
    "ancillary linear search function for implementing mu-minimization"
    z = 0
    while not test(cp.dp(x, z)):
        z += 1
    return z


class PReFScript:

    def __init__(self, store_goedel_numbers = ""):
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
        self.store_gnums = store_goedel_numbers # not in use at the moment
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

    def list(self, what = None, verbose = 0):
        '''
        plans:
         if what == None: list everything, o/w search for what on the dicts
         obey verbosity level
        all this still unimplemented, always lists everything fully
        '''
        for gnum in self.main:
            print(str(self.main[gnum]))
            # ~ print(" Gödel number:", gnum, 
            # ~ "= <" + str(cp.pr_l(gnum)) + "." + str(cp.pr_r(gnum)) + ">\n")

    def define(self, how, on_what, nick, comment):
        'here comes a new function to add to the dicts appropriately'
        if nick in self.nicks:
            print("Nickname " + nick + " already in use. New definition ignored.")
            return None
        numhow = self.hownums[how]
        if numhow == 0:
            print("Addition of new basic functions is unsupported as yet. New definition ignored.")
            return None
        wrong = ""
        if numhow == 3:
            if on_what not in self.nicks:
                wrong = on_what
        else:
            "numhow 1 or 2"
            if on_what[0] not in self.nicks:
                wrong = on_what[0]
            elif on_what[1] not in self.nicks:
                wrong = on_what[1]
        if wrong:
            print("Nickname " + wrong + " unknown. New definition ignored.")
            return None
        data = FunData()
        data["nick"] = nick
        data["comment"] = comment
        data["how_def"] = how
        data["def_on"] = on_what
        # ~ if self.store_gnums: # to be checked once keys are moved to nicks
        if numhow in (1, 2):
            'set up gnum'
            lft = self.nicks[on_what[0]]
            rgt = self.nicks[on_what[1]]
            gnum = cp.dp(numhow, cp.dp(lft, rgt))
        else:
            'numhow is 3, minimization'
            gnum = cp.dp(3, self.nicks[on_what])
        if numhow == 1:
            'composition'
            data["code"] = "lambda x: " + on_what[0] + "(" + on_what[1] + "(x))"
        if numhow == 2:
            'pairing'
            data["code"] = "lambda x: cp.dp(" + on_what[0] + "(x), " + on_what[1] + "(x))"
        if numhow == 3:
            'mu-minimization'
            data["code"] = "lambda x: mu(x, " + on_what + ")"
        self.nicks[nick] = gnum
        self.main[gnum] = data
        self.pycode[nick] = eval(data["code"], globals() | self.pycode)

    def to_python(self, what):
        'returns the Python-runnable version of the function'
        if what not in self.pycode:
            print("Nickname " + what + " not defined.")
            return None
        return self.pycode[what]

    def load(self, filename):
        'load definitions from file, temporary current format (inoperative)'
        with open(filename) as f:
            for line in f:
                line = line.split('|')
                on = line[4].split()
                if len(on) > 1:
                    on = tuple(on)
                else:
                    on = on[0]
                self.define(line[3].strip(), on, line[1].strip(), line[2].strip())

    def dialog(self):
        nick = input("Function nickname? ")
        comment = input("What is it? ")
        how = input("How is it made? [pair or comp or mu] ")
        on_what = input("Applied to what? [1 or 2 names] ")
        on_what = on_what.split()
        if len(on_what) > 1:
            on_what = tuple(on_what)
        else:
            on_what = on_what[0]
        self.define(how.strip(), on_what, nick.strip(), comment.strip())
