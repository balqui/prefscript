'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version early Fructidor 2026:
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

Nicknames are alphanum strings not starting with a number (no surprise); 
they must NOT consist of three underscores followed by digits.

The runnable Python code is a separate dict so as to pass it together 
with globals to eval.

Open: do I really need the copy() method?
'''

from dataclasses import dataclass #, replace #, field # for copy...
from typing import Tuple
from cantorpairs import ensure

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
    index: int = -1         # Goedel nums, but only if requested

    def __post_init__(self):
        match self.howdf:
            case 'pending' | 'basic': pass
            case 'alias' if len(self.defon) == 1:
                self.rawpy = f"lambda x: {self.defon[0]}(x)"
            case 'ascii_const' if len(self.defon) == 1:
                self.rawpy = f"lambda x: str2int({self.defon[0]})"
            case 'comp' if len(self.defon) == 2:
                self.rawpy = f"lambda x: {self.defon[0]}({self.defon[1]}(x))"
            case 'pair' if len(self.defon) == 2:
                self.rawpy = f"lambda x: cp.dp({self.defon[0]}(x), {self.defon[1]}(x))"
            case 'mu' if len(self.defon) == 1:
                self.rawpy = f"lambda x: mu(x, {self.defon[0]})"
            case 'rec' if len(self.defon) == 3: 
                self.rawpy = f"lambda x: rec({self.defon[0]}, {self.defon[1]}, {self.defon[2]})(x)"
            # ~ case 'pr' | 'ppr': pass     # deprecated!
            case _:
                ensure.that(False, (f"Bad 'how defined' or wrong number "
                               f"of arguments for it in {self}"))


# ~ if copy() is ever uncommented, it needs from dataclasses import replace
    # ~ def copy(self, **changes) -> Self:
        # ~ "Creates a duplicate of self, optionally overriding fields."
        # ~ return replace(self, **changes)
