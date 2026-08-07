#! /usr/bin/python3
'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version mid Thermidor 2026:
prefscript.py: temporary main program

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''


__version__ = "2.0"

from parser import prfsparser, ScriptMaker
from script import PReFScript
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('f', nargs='?', default=None)

if f := ap.parse_args().f:
    with open(f) as ff:
        ast = prfsparser(ff.read())
    print(ast.pretty())
    scrmk = ScriptMaker(PReFScript())
    scr = scrmk.transform(ast)
    # ~ scr.list()
    scr.to_python('main')
    mainf = scr.pycode['main']
    if not scr.valid:
        pass
        # ~ scr.list(w_code = 1)
    else:
        # ~ print("\nTests:")
        # ~ while n := input("In: "):
            # ~ n = int(n)
            # ~ print("Out:", mainf(n))
        while n := input():
            n = int(n)
            print(n, mainf(n))
    exit()
