#! /usr/bin/python3
'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version mid Thermidor 2026:
prefscript.py: temporary main program

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

NEXT:
- inputs: none, seq, pair? Maybe via CLI flag
- close issues (prepare first a list)
- document v2
- Goedel number generation should be much closer to
  Python source generation than it is right now.
  Must refactor the whole of it.
- A minimal GUI on Windows?
'''

from argparse import ArgumentParser
from pathlib import Path
from sys import stdin

from pytokr import pytokr

import cantorpairs as cp
from parser import prfsparser, ScriptMaker
from script import PReFScript
from ascii7io import int2str

__version__ = "2.0"

ap = ArgumentParser(
    description = 'An interpreter of a scripting language '
                  'based on the partial recursive functions.')

# CLI-only arguments:

ap.add_argument('filename', nargs = '?', default = None, 
                help = "file containing the script "
                      "(suffix .prfs assumed)")
ap.add_argument('-V', '--version', action = 'version', version = f"{ap.prog} v. {__version__}")
# ~ ap.add_argument("-C", "--cmd", 
    # ~ help="Run as a command on stdin.",
    # ~ action="store_true") 
ap.add_argument("-P", "--show_parsing", 
    help = "Display the Abstract Syntax Tree of the script, don't run it.",
    action = "store_true") 
ap.add_argument("-G", "--Goedel_nums", 
    help = "Show Goedel numbers of functions while not too large,"\
           " don't run the script.",
    action = "store_true") 

# pragma-enabled arguments:

ap.add_argument("-I", "--import_folder", # nargs = 1, 
    help = "additional folder where to search for imported files",
    action = "extend")                 # should allow maybe more than one
ap.add_argument("-R", "--read", 
    default = "int",
    help = "Input type format: int (default) or intseq or nothing" \
         " (input one int or several or nothing at all)") 
ap.add_argument("-W", "--write", 
    default = "int",
    help = "Output type format:"\
           " int (default) or bool or ascii" \
           " (output is cast into that type)") 

read, loop = pytokr.pytokr(iter = True)    # not sure why only one is insufficient

app = ap.parse_args()

import_folder = app.import_folder
if import_folder is not None:
    import_folder = import_folder[0]      # should clarify and refactor

# ~ if app.cmd:
    # ~ "Can't work right now due to the import-related dependency graph"
    # ~ script_text = stdin.read()

if (f := app.filename) is not None:
    with open(f) as ff:
        script_text = ff.read()
    ast = prfsparser(script_text)
    run = True
    if app.show_parsing:
        print(ast.pretty())
        run = False
    if app.Goedel_nums:
        from gnums import ShowGNums
        gen_gnums = ShowGNums(PReFScript(), Path(f).resolve(), import_folder)
        gen_gnums.gprint(ast)
        run = False
    if run:
        "Handle first input and output formats"
        # ~ cp.ensure.that(app.read in (None, "int", "intseq", "nothing"), 
        cp.ensure.that(app.read in ("int", "intseq", "nothing"), 
                       f"Unknown --read value {app.read}")
        # ~ cp.ensure.that(app.write in (None, "int", "ascii", "bool"), 
        cp.ensure.that(app.write in ("int", "ascii", "bool"), 
                       f"Unknown --write value {app.write}")
        outf = int2str if app.write == "ascii" \
                       else lambda x: eval(app.write)(x)
        scrmk = ScriptMaker(PReFScript(), Path(f).resolve(), import_folder)
        scr = scrmk.transform(ast)
        scr.to_python('main')
        mainf = scr.pycode['main']
        while True:
            match app.read:
                case "int": 
                    if n := input():
                        print(outf(mainf(int(n))))
                    else:
                        break
                case "intseq": 
                    print(outf(mainf(cp.tup_i(map(int, loop())))))
                    break
                case "nothing":
                    print(outf(mainf(42)))
                    break
                case _: 
                    print("arg app.read is", app.read)
            # ~ n := input():
            # ~ n = int(n)
            # ~ print(outf(mainf(n)))
        exit()
else:
    print("Try prefscript --help")
    
