'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version early Fructidor 2026:
class PReFScript storing all the functions in one script.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Functions are stored in FunData instances.
Then, in a separate dict used as namespace for 
eval calls, a runnable version of the code.

Open: consider setting up an alternative key: 
how it is constructed and the tuple of function
identifiers that participate in its definition;
would allow one to detect duplicates. 

Replaced SyntErr first by assert's and subsequently
by cp.ensure.that() - to be combined with whatever 
Lark offers for handling errors.

Remember that now cp.seq and cp.ensure are available.
'''

import cantorpairs as cp
from fundata import FunData
from basicfun import BasicFun
from ascii7io import str2int

# A handful of ancillary functions

def mu(x, test):
    "ancillary linear search function for implementing mu-minimization"
    z = 0
    while not test(cp.dp(x, z)):
        z += 1
    return z

def rec(recurse, base, is_base):
    '''
    primitive recursion with parameters: base receives input pair
    <param.val>, base only val, recurse receives
    <param.<indval.sq>> for sq the course of values up to indval-1
    NOW I BELIEVE I CANNOT AFFORD THAT STRUCTURE AND ACTUALLY NEED
    <<param.indval>.sq>> for sq the course of values up to indval
    as o/w I don't grab the indval correctly in base cases of fib.
    '''

    def c_of_v(z):
        "create the adequate course of values"
        x = cp.pr_R(z)
        p = cp.pr_L(z)
        sq = 0 # empty sequence
        for y in range(x + 1):
            z = cp.dp(p, y)
            new = base(z) if is_base(y) else recurse(cp.dp(z, sq))
            sq = cp.dp(new, sq)
        return sq

    return lambda x: cp.pr_L(c_of_v(x))


class PReFScript(dict):

    def __init__(self):
        '''
        Maps each nick to a FunData; initially already contains
        the basic functions. Additional separate dict with runnable 
        functions; may keep getting other fields for pragmas 
        and other minor infos. 
        Goedel number handling and raw Python strings: pending to
        undergo refactoring.
        Doubles as a dependency graph via the 'defon' fields
        in the FunData instances.
        '''
        super().__init__(self)
        self |= BasicFun()    # initialize with the basic functions
        self.pycode = dict()  # namespace for its own lambdas

    def list(self, what = None, w_code = 0):
        '''
        if what is None: list everything
        else: search for that 'what' in the dict.
        Pending: delegate one day the w_code to FunData.
        w_code 0: no code, 1: how and on what, 2: strcode 
        '''
        def list_one(fdat, w_code):
            s = f"{fdat.fname}: " 
            if fdat.docst:
                s += f"[{fdat.docst}] "
            if w_code:
                'add how it is defined'
                if fdat.howdf == "basic":
                    s += "basic"
                else:
                    s += f"{fdat.howdf} on {', '.join(fdat.defon)}"
            if w_code == 2:
                s += f"; {fdat.rawpy}."
            else:
                s += "."
            return s

        if what is not None:
            print(list_one(self[what], w_code))
        else:
            for nick in self:
                print(list_one(self[nick], w_code))

    def define(self, new_funct):
        'here comes a new function to add to the collection'
        nick = new_funct.fname
        if nick in self and self[nick].howdf != "pending":
            'repeated nick, check for consistency, MAYBE INSUFFICIENT'
            cp.ensure.that(self[nick].howdf == new_funct.howdf and
                self[nick].defon == new_funct.defon, f"Repeated, " +
                "inconsistent definitions for function '{nick}' found.")
        else:
            self[nick] = new_funct

    def remove(self, nick):
        "for placeholders, use with care"
        del self[nick]

    def gen_py(self, name, need = 'PReFScript syntax specs'):
        if name in self.pycode:
            "already seen, just ensure we are not in a definition loop"
            cp.ensure.that(self.pycode[name] != "None", 
                f"Function '{name}' belongs to a disallowed definition loop.")
        else:
            self.pycode[name] = "None" # make sure never to loop on it
            cp.ensure.that(name in self,
                f"Function {name} not found but required by {need}.") 
                                # that test never seems to fail
            cp.ensure.that(self[name].howdf != "pending",
                f"Function {name} undefined but required by {need}.")
            if self[name].howdf == "ascii_const":
                "the def_on part of an ascii_const is already handled"
                self.pycode[name] = eval(self[name].rawpy, globals() | self.pycode)
            else:
                for nname in self[name].defon:
                    "we need first the recursive calls"
                    self.gen_py(nname, name)
                self.pycode[name] = eval(self[name].rawpy, globals() | self.pycode)

    def to_python(self, what):
        'returns the Python-runnable version of the function'
        if what not in self.pycode:
            self.gen_py(what)
        return self.pycode[what]
