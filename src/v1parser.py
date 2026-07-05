'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module:
v1parser: re-based parser for versions up to 1.2
(file distribution slight refactoring on the monolithic design of Thermidor 2004)

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

# ~ from collections import defaultdict as ddict
from re import compile as re_compile, finditer as re_finditer
# ~ from ascii7io import int2str, str2int, int2raw_str # users are not expected to need int2raw_str
# ~ import cantorpairs
# ~ cp = cantorpairs

from fundata import FunData

__version__ = "1.2"

class Parser:
    '''Prepare an re-based parser to be used upon reading scripts
    The single Parser with single parse generator is likely to mess up
    the recursive imports, I bet it does not work yet.
    '''

    def __init__(self):
        "group names require Python >= 3.11"
        from re import compile as re_compile, finditer as re_finditer
        about = r"\s*\.about(?P<about>.*)\n"                           # arbitrary documentation
        pragma = r"\s*\.pragma\s+(?P<which>\w+):?\s+(?P<what>\w+)\s*"  # compilation directives
        importing = r"\s*\.import\s+(?P<to_import>[\w._-]+)\s*"        # additional external script
        a7str = r'''(?P<quote>['"])(?P<a7str>.*)(?P=quote)'''
        startdef = r"\d+\s+define\:\s*"
        group1_nick = r"(?P<nick>\w+)\s+"
        group2_comment = r"\[\s*(?P<comment>(\w|\s|[.,:;<>=)(?!/+*-])+)\]\s+" 
        group4_how = r"(?P<how>pair|comp|mu|compair|primrec|ascii_const|parprimrec)\s+" 
        group5_on_what = r"((?P<on_what>([a-zA-Z_]\w*\s+)+)|" + a7str + ")"  # nick args required not to start with a number
        define = (startdef +  
              group1_nick + 
              group2_comment + 
              group4_how +
              group5_on_what)
        self.the_parser = re_compile(define + '|' + about + '|' + pragma + '|' + importing)

    def parse(self, source):
        for thing in re_finditer(self.the_parser, source):
            "can one find out non-matched portions to message the user about?"
            things = thing.groupdict(default = '')
            if about := things['about']:
                yield 'about', about
            if which := things['which']:
                yield 'pragma', (which, things['what'])
            if to_import := things['to_import']:
                yield 'import', to_import
            if nick := things['nick']:
                if things['how'] == "ascii_const":
                    on_what = [things['a7str']]
                else:
                    on_what = things['on_what'].split()
                yield "define", FunData(nick, things['comment'], things['how'], on_what)


class SyntErr:
    "handle syntactic errors in the script - VERY PRIMITIVE for the time being"

    def __init__(self):
        from sys import stderr
        self.e = stderr

    def report(self, nonfatal = False, info = ''):
        "return value to be given to the valid field / alt: fatal here and nonvalid at script"
        p = 'Nonf' if nonfatal else 'F'
        print(p + 'atal error in PReFScript:', info, sep = '\n  ', file = self.e)
        return nonfatal


