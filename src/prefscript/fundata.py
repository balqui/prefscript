'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version early Thermidor 2026:
fundata: class FunData storing all necessary information about 
one partial recursive function

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

For the time being, we maintain the most basic information: 
how made and on what (ingredient functions). Corresponds to
what the tree walker finds in a funspec subtree. Tree walking
is bottom-up so I cannot have a frozen dataclass because info
(the name and maybe everything else) is getting added later 
along the way. 

Uses __post_init__ to raise a ValueError exception if howdf is not 
valid. Open: add a custom exception? Current answer: maybe.

In the future we might add the Goedel number if not too big 
(which actually repeats the previous info), the docstring and
who knows exactly what else.

Nicknames are alphanum strings not starting with a number (no surprise); 
they must NOT consist of three underscores followed by digits.

The runnable Python code is a separate dict so as to pass it together 
with globals to eval.

Open: where do we handle the decision whether to 
store (some) Goedel numbers? And where do we store them?

Open: do I really need the copy() method?
'''

# ~ import cantorpairs as cp # only needed by gnums, if at all
from dataclasses import dataclass #, replace #, field
from typing import Tuple

@dataclass
class FunData:
    '''
    Simple class for a single PReFScript function data.
    Not anymore frozen as not all info available at once.
    Although basic and alias are not really different, 
    their usage is, decided to keep the distinction.
    '''
    fname: str              # The name may be an internal surrogate.
    docst: str = ""
    howdf: str = "pending"  # Checked for validity in __post_init__.
    defon: Tuple[str, ...] = tuple()
    rawpy: str = ""
    index: int = -1

    def __post_init__(self):
        match self.howdf:
            case 'pending' | 'basic': pass
            case 'alias' if len(self.defon) == 1:
                self.rawpy = f"lambda x: {self.defon[0]}(x)"
            case 'comp' if len(self.defon) == 2:
                self.rawpy = f"lambda x: {self.defon[0]}({self.defon[1]}(x))"
            case 'pair' if len(self.defon) == 2:
                self.rawpy = f"lambda x: cp.dp({self.defon[0]}(x), {self.defon[1]}(x))"
            case 'mu' if len(self.defon) == 1:
                self.rawpy = f"lambda x: mu(x, {self.defon[0]})"
            case 'pr' | 'ppr': pass
            case '_'   : 
                assert False, (f"Bad 'how defined' or wrong number "
                               f"of args for it in {self}")


# ~ if copy() is ever uncommented, it needs from dataclasses import replace
    # ~ def copy(self, **changes) -> Self:
        # ~ "Creates a duplicate of self, optionally overriding fields."
        # ~ return replace(self, **changes)


# ~ Old code to show how gnum's are to be handled in due time:

                # ~ if self.store_gnums and on_what[0] in self.gnums and on_what[1] in self.gnums:
                    # ~ gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]], self.gnums[on_what[1]]))
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")

            # ~ elif new_funct['how_def'] == "pair":
                # ~ self.strcode[nick] = "lambda x: cp.dp(" + on_what[0] + "(x), " + on_what[1] + "(x))"
                # ~ if self.store_gnums and on_what[0] in self.gnums and on_what[1] in self.gnums:
                    # ~ gnum = cp.dp(2, cp.dp(self.gnums[on_what[0]], self.gnums[on_what[1]]))
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")
    
            # ~ elif new_funct['how_def'] == "mu":
                # ~ self.strcode[nick] = "lambda x: mu(x, " + on_what[0] + ")"
                # ~ if self.store_gnums and on_what[0] in self.gnums:
                    # ~ gnum = cp.dp(3, self.gnums[on_what[0]])
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")

            # ~ elif new_funct['how_def'] == "compair":
                # ~ if not self.pragmas['extended']:
                    # ~ self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  # ~ info = "Use of compair requires '.pragma extended: True', changed.")
                # ~ self.pragmas['extended'] = 'True'
                # ~ self.strcode[nick] = "lambda x: " + on_what[0] + "( cp.dp(" + on_what[1] + "(x), " + on_what[2] + "(x)))"
                # ~ if (self.store_gnums and on_what[0] in self.gnums and 
                    # ~ on_what[1] in self.gnums and on_what[2] in self.gnums):
                    # ~ gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]],
                           # ~ cp.dp(2, cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]]))))
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")

            # ~ elif new_funct['how_def'] == "primrec":
                # ~ if not self.pragmas['extended']:
                    # ~ self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  # ~ info = "Use of primrec requires '.pragma extended: True', changed.")
                # ~ self.pragmas['extended'] = 'True'
                # ~ self.strcode[nick] = "prim_rec(" + on_what[0] + ", " + on_what[1] + ", " + on_what[2] + ")"
                # ~ if (self.store_gnums and on_what[1] in self.gnums and on_what[2] in self.gnums):
                    # ~ gnum = cp.dp(4, cp.dp(int(on_what[0]),
                               # ~ cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]])))
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")

            # ~ elif new_funct['how_def'] == "parprimrec":
                # ~ if not self.pragmas['extended']:
                    # ~ self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  # ~ info = "Use of parprimrec requires '.pragma extended: True', changed.")
                # ~ self.pragmas['extended'] = 'True'
                # ~ self.strcode[nick] = "par_prim_rec(" + on_what[0] + ", " + on_what[1] + ", " + on_what[2] + ")"
                # ~ if (self.store_gnums and on_what[1] in self.gnums and on_what[2] in self.gnums):
                    # ~ gnum = cp.dp(5, cp.dp(int(on_what[0]),
                               # ~ cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]])))
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")

            # ~ else:
                # ~ "ascii_const, as no other 'how' captured by parser - kept out of the Goedel numbering for the time being"
                # ~ if not self.pragmas['extended']:
                    # ~ self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  # ~ info = "Use of ascii constants requires '.pragma extended: True', changed.")
                # ~ self.pragmas['extended'] = 'True'
                # ~ self.strcode[nick] = "lambda x: str2int( '" + on_what[0] + "' )"
