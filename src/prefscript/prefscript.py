#! /usr/bin/python3
'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version early Fructidor 2026:
prefscript.py main program.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

from argparse import ArgumentParser
from pathlib import Path
from sys import stdin

from .pytokr.pytokr import pytokr

from . import cantorpairs as cp
from .parser import prfsparser
from .codegen import ScriptMaker
from .script import PReFScript
from .ascii7io import int2str
from .praprepro import PraPrePro # pragma pre-processor

__version__ = "2.0.1"

def main():

	ap = ArgumentParser(
	    description = 'An interpreter of a scripting language '
	                  'based on the partial recursive functions.')
	
	# CLI-only arguments:
	
	ap.add_argument('filename', nargs = '?', default = None, 
	                help = "file containing the script "
	                      "(suffix .prfs assumed)")
	ap.add_argument('-V', '--version', action = 'version', 
	                version = f"{ap.prog} v. {__version__}")
	ap.add_argument("-P", "--show_parsing", 
	    help = "Display the Abstract Syntax Tree of the script,"\
	           " don't run it.",
	    action = "store_true") 
	ap.add_argument("-G", "--Goedel_nums", 
	    help = "Show Goedel numbers of functions while not too large,"\
	           " don't run the script.",
	    action = "store_true") 
	
	# pragma-enabled arguments:
	
	ap.add_argument("-I", "--import_folder", nargs = 1, 
	    default = None,               # refreshed below upon reading pragmas
	    help = "additional folder where to search for imported files",
	    action = "extend")                # should allow maybe more than one
	ap.add_argument("-R", "--read", 
	    default = None,               # refreshed below upon reading pragmas
	    help = "Input type format: int (default) or"\
	           " intpair or intseq or nothing" \
	           " (input one int or two or several or nothing at all)") 
	ap.add_argument("-W", "--write", 
	    default = None,               # refreshed below upon reading pragmas
	    help = "Output type format:"\
	           " int (default) or bool or ascii" \
	           " (output is cast into that type)") 
	
	prprpr = PraPrePro()
	
	read, loop = pytokr(iter = True)
	
	app = ap.parse_args()
	
	if (f := app.filename) is not None:
	    with open(f) as ff:
	        "let exception through if it is not there"
	        script_text = ff.read()
	
	    # check out pragmas and see if they are superseded by CLI args
	    pragmas = dict(prprpr.parse(script_text))
	    if app.read is None:
	        app.read = pragmas["read"] if "read" in pragmas else "int"
	    if app.write is None: 
	        app.write = pragmas["write"] if "write" in pragmas else "int"
	    import_folder = app.import_folder
	    if import_folder is None:
	        import_folder = pragmas["import_folder"] \
	                        if "import_folder" in pragmas else None
	    else:
	        import_folder = import_folder[0]
	
	    ast = prfsparser(script_text)
	    run = True
	    if app.show_parsing:
	        print(ast.pretty())
	        run = False
	    if app.Goedel_nums:
	        from gnums import ShowGNums
	        gen_gnums = ShowGNums(PReFScript(), 
	                              Path(f).resolve(), import_folder)
	        gen_gnums.gprint(ast)
	        run = False
	    if run:
	        "Handle first input and output formats"
	        cp.ensure.that(
	            app.read in ("int", "intpair", "intseq", "nothing"), 
	            f"Unknown --read value {app.read}")
	        cp.ensure.that(
	            app.write in ("int", "ascii", "bool"), 
	            f"Unknown --write value {app.write}")
	        outf = int2str if app.write == "ascii" \
	                       else lambda x: eval(app.write)(x)
	        scrmk = ScriptMaker(PReFScript(), 
	                            Path(f).resolve(), import_folder)
	        scr = scrmk.transform(ast)
	        scr.to_python('main')
	        mainf = scr.pycode['main']
	        match app.read:
	            case "int": 
	                print(outf(mainf(int(read()))))
	            case "intpair": 
	                print(outf(mainf(cp.dp(int(read()), int(read())))))
	            case "intseq": 
	                print(outf(mainf(cp.tup_i(map(int, loop())))))
	            case "nothing":
	                print(outf(mainf(42)))
	else:
	    print("Try prefscript --help")

if __name__ == "__main__":
    main()
