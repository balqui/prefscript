'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version mid Thermidor 2026:
pref_script.py: class PReFScript storing all the functions in one script

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Functions are stored in FunData instances.
Then, in a separate dict used as namespace for 
eval calls, a runnable version of the code.

Open: consider setting up an alternative key: 
how it is constructed and the tuple of function
identifiers that participate in its definition;
would allow one to detect duplicates. 

Open: SyntErr might be replaceable by a combination
of assert's and whatever Lark offers for handling
errors, this is to be reviewed.

Open: shall we keep pragmas? Maybe just command line flags?
'''

# ~ from collections import defaultdict as ddict # maybe for pragmas?

import cantorpairs as cp
from fundata import FunData
from basicfun import BasicFun
from synterr import SyntErr

__version__ = "2.0"

# A handful of ancillary functions

def mu(x, test):
    "ancillary linear search function for implementing mu-minimization"
    z = 0
    while not test(cp.dp(x, z)):
        z += 1
    return z



class PReFScript(dict):

    def __init__(self): #, store_goedel_numbers = ""):
        '''
        Maps each nick to a FunData; initially already contains
        the basic functions. Additional separate dicts with pragmas 
        and runnable functions; plus minor other fields. 
        Goedel number handling and raw Python strings: pending.
        Doubles as a dependency graph via the 'defon' fields
        in the FunData instances.
        '''
        super().__init__(self)
        self |= BasicFun()    # initialize with the basic functions
        self.valid = True     # program is correct until proven wrong
        # ~ self.pragmas = ddict(str)
        self.pycode = dict()  # namespace for its own lambdas
        self.synt_err_handler = SyntErr()
        # ~ self.store_gnums = store_goedel_numbers # doubtful, leave for now

    def list(self, what = None, w_code = 0):
        '''
        if what is None: list everything
        else: search for that what on the dict.
        Delegate one day the w_code and gnum to FunData.
        w_code 0: no code, 1: how and on what, 2: strcode also
        Gödel number printed depending on self.store_gnums and 
        how big it is
        '''
        def list_one(fdat, w_code):
            s = f"{fdat.fname}: " 
            if fdat.docst:
                s += f"[{fdat.docst}]"
            if w_code:
                'add how it is defined'
                s += f", {fdat.howdf} on {fdat.defon}"
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

            # ~ if self.store_gnums:
                # ~ if nick in self.gnums:
                    # ~ gnum = self.gnums[nick]
                    # ~ print(" Gödel number:", gnum,
                          # ~ "= <" + str(cp.pr_L(gnum)) + "." + str(cp.pr_R(gnum)) + ">")
                # ~ else:
                    # ~ self.valid &= self.synt_err_handler(fatal = False, info = "Gödel number too large, omitted.")

    def define(self, new_funct):
        'here comes a new function to add to the collection'
        nick = new_funct.fname
        if nick in self and self[nick].howdf != "pending":
            'repeated nick, check for consistency, MAYBE INSUFFICIENT'
            if (self[nick].howdf != new_funct.howdf or
                self[nick].defon != new_funct.defon):
                    self.valid &= self.synt_err_handler.report(nonfatal = False,
                    info = f"Repeated, inconsistent definitions for function '{nick}' found.")
        else:
            self[nick] = new_funct

    def remove(self, nick):
        "for placeholders, use with care"
        del self[nick]

    def gen_py(self, name, need = 'pragma main'):
        "I guess 'pragma main' is not the right message anymore"
        if name not in self.pycode:
            "make sure never to loop on it"
            self.pycode[name] = "None"
            if name in self and self[name].howdf != "pending":
                if self[name].howdf != "ascii_const":
                    "the def_on part of an ascii_const is a mere string already handled"
                    for nname in self[name].defon:
                        "we need first the recursive calls"
                        self.gen_py(nname, name)
                self.pycode[name] = eval(self[name].rawpy, globals() | self.pycode)
            else:
                "newly found undefined name"
                self.valid &= self.synt_err_handler.report(nonfatal = False, 
                    info = f"Function '{name}' not found but needed by {need}.")
                # ~ print("!!!!!!!!!!!!!", self.valid)
        elif self.pycode[name] == "None":
            "already attempted, make sure not to fall in a definition loop"
            self.valid &= self.synt_err_handler.report(nonfatal = False, 
                info = f"Function '{name}' belongs to a disallowed definition loop.")

    def to_python(self, what):
        'returns the Python-runnable version of the function'
        if what not in self.pycode:
            self.gen_py(what)
        if self.valid:
            return self.pycode[what]
