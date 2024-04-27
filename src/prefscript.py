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

import re
import scaff.cantorpairs as cp
# ~ import cantorpairs as cp
# ~ from fundata import FunData # class FunData added here now

# ~ limit in order to omit Gödel numbers too high, around 300 decimal digits
# ~ LIMIT_GNUM set to 2**1000 but computed much faster via bit shift

LIMIT_GNUM = 2 << 999

class FunData(dict):
    'Simple class for PReFScript functions data'

    def __init__(self):
        dict.__init__(self)
        self["nick"] = None
        self["comment"] = None
        self["how_def"] = None
        self["def_on"] = None

    def __str__(self):
        return self["nick"] + "\n " + self["comment"] 

    def how_def(self):
        return self["how_def"] + ": " + ' '.join(on_what for on_what in self["def_on"])


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
          main for the function data,
          gnums for Gödel numbers,
          pycode for Python runnable code, 
          key is always nick for all of them;
        include here the basic functions;
        their implementation assumes 'import cantorpairs as cp'
        '''
        self.main = dict()
        self.strcode = dict()
        self.pycode = dict()
        self.gnums = dict()
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
        gnum = cp.dp(0, num)
        self.gnums[nick] = gnum
        self.main[nick] = data
        self.strcode[nick] = code
        self.pycode[nick] = eval(code, globals() | self.pycode)


    def list(self, what = None, w_code = 0):
        '''
        if what is None: list everything
        else: search for that what on the dicts
        w_code 0: no code, 1: how and on what, 2: strcode also
        Gödel number printed depending on self.store_gnums and how big it is
        '''
        def list_one(nick, w_code):
            print("\n" + str(self.main[nick]))
            if w_code:
                'print how it is defined'
                print(" " + self.main[nick].how_def())
            if w_code == 2:
                'print also the Python code in this case only'
                print(" " + self.strcode[nick])
            if self.store_gnums:
                if nick in self.gnums:
                    gnum = self.gnums[nick]
                    print(" Gödel number:", gnum,
                          "= <" + str(cp.pr_l(gnum)) + "." + str(cp.pr_r(gnum)) + ">")
                else:
                    print(" Gödel number too large, omitted")

        if what is not None:
            list_one(what, w_code)
        else:
            for nick in self.main:
                list_one(nick, w_code)


    def define(self, how, on_what, nick, comment):
        'here comes a new function to add to the dicts appropriately'
        if nick in self.main:
            print("Nickname " + nick + " already in use. New definition ignored.")
            return None
        numhow = self.hownums[how]
        if numhow == 0:
            print("Addition of new basic functions is unsupported as yet. New definition ignored.")
            return None
        wrong = ""
        if on_what[0] not in self.main:
            wrong = on_what[0]
        elif numhow < 3 and on_what[1] not in self.main:
            wrong = on_what[1]
        if wrong:
            print("Nickname " + wrong + " unknown. Definition of " + nick + " ignored.")
            return None
        data = FunData()
        data["nick"] = nick
        data["comment"] = comment
        data["how_def"] = how
        data["def_on"] = on_what
        if self.store_gnums and on_what[0] in self.gnums:
            lft = self.gnums[on_what[0]]
            if numhow < 3:
                if on_what[1] in self.gnums:
                    'set up gnum for pair or comp'
                    rgt = self.gnums[on_what[1]]
                    gnum = cp.dp(numhow, cp.dp(lft, rgt))
                    if gnum < LIMIT_GNUM:
                        self.gnums[nick] = gnum
            else:
                'set up gnum for minimization'
                gnum = cp.dp(3, lft)
                if gnum < LIMIT_GNUM:
                    self.gnums[nick] = gnum
        if numhow == 1:
            'composition'
            # ~ data["code"] = "lambda x: " + on_what[0] + "(" + on_what[1] + "(x))"
            self.strcode[nick] = "lambda x: " + on_what[0] + "(" + on_what[1] + "(x))"
        if numhow == 2:
            'pairing'
            # ~ data["code"] = "lambda x: cp.dp(" + on_what[0] + "(x), " + on_what[1] + "(x))"
            self.strcode[nick] = "lambda x: cp.dp(" + on_what[0] + "(x), " + on_what[1] + "(x))"
        if numhow == 3:
            'mu-minimization'
            # ~ data["code"] = "lambda x: mu(x, " + on_what[0] + ")"
            self.strcode[nick] = "lambda x: mu(x, " + on_what[0] + ")"
        self.main[nick] = data
        # ~ self.pycode[nick] = eval(data["code"], globals() | self.pycode)
        self.pycode[nick] = eval(self.strcode[nick], globals() | self.pycode)


    def to_python(self, what):
        'returns the Python-runnable version of the function'
        if what not in self.pycode:
            print("Nickname " + what + " not defined.")
            return None
        return self.pycode[what]


    def load(self, filename):
        'load in definitions from .prfs file'
        patt = re.compile("(\d|\s)*define\:\s*(\w+)\s+\[\s*((\w|\s|[.,:;<>\)\(?\-+*]?)+)\]\s+(((pair)\s+(\w*\s+\w+)\s+)|((comp)\s+(\w*\s+\w+)\s+)|((mu)\s+(\w*)\s+))")
        with open(filename) as infile:
            script = infile.read()
        for funct in re.finditer(patt, script):
            nick = funct.group(2)
            comment = funct.group(3)
            if funct.group(7) is not None:
                how = funct.group(7)
            if funct.group(10) is not None:
                how = funct.group(10)
            if funct.group(13) is not None:
                how = funct.group(13)
            if funct.group(8) is not None:
                on_what = tuple(funct.group(8).split())
            if funct.group(11) is not None:
                on_what = tuple(funct.group(11).split())
            if funct.group(14) is not None:
                on_what = tuple(funct.group(14).split())
            self.define(how.strip(), on_what, nick.strip(), comment.strip())


    def formerload(self, filename):
        'load definitions from file, temporary current format (inoperative)'
        with open(filename) as f:
            for line in f:
                line = line.split('|')
                on = tuple(line[4].split())
                self.define(line[3].strip(), on, line[1].strip(), line[2].strip())


    def dialog(self):
        nick = input("Function nickname? ")
        comment = input("What is it? ")
        how = input("How is it made? [pair or comp or mu] ")
        on_what = input("Applied to what? [1 or 2 space-sep names] ")
        on_what = on_what.split()
        self.define(how.strip(), tuple(on_what), nick.strip(), comment.strip())
