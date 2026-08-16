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

from pathlib import Path

# ~ from prefscript import __version__

ap = ArgumentParser(
    # ~ prog = 'PReFScript',
    description = 'An interpreter of a scripting language '
                  'based on the partial recursive functions.')
ap.add_argument('filename', nargs='?', default=None, 
                help="file containing the script "
                      "(suffix .prfs assumed)")
ap.add_argument('-V', '--version', action='version', version=f"{ap.prog} v. {__version__}")
ap.add_argument("-I", "--import_folder", nargs=1, 
    help="additional folder where to search for imported files",
    action="extend")
ap.add_argument("--showtree", 
    help="Display the Abstract Syntax Tree of the script",
    action="store_true")

# ~ to add: version, import folder, show tree, 

app = ap.parse_args()

if (f := app.filename) is not None:
    import_folder = app.import_folder
    if import_folder is not None:
        import_folder = import_folder[0]
    with open(f) as ff:
        ast = prfsparser(ff.read())
    if app.showtree:
        print(ast.pretty())
    scrmk = ScriptMaker(PReFScript(), Path(f).resolve(), import_folder)
    scr = scrmk.transform(ast)
    # ~ scr.list()
    scr.to_python('main')
    mainf = scr.pycode['main']
    while n := input():
        n = int(n)
        print(mainf(n))
    exit()
else:
    print("Try prefscript --help")
    
