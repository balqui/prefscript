'''
Project started mid Germinal 2023:
PReFScript: A Partial Recursive Functions Lab

Module version mid Messidor 2026:
prefscript with main class PReFScript and run entrypoint only
(file distribution slight refactoring on the monolithic design of Thermidor 2024)

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used as such.

Functions are stored in FunData instances.
Then, in a separate dict (used as namespace for 
eval calls), a runnable version of the code.
'''

from collections import defaultdict as ddict
from ascii7io import int2str, str2int
import cantorpairs as cp

from v1parser import Parser, SyntErr
from fundata import FunData

__version__ = "1.2"

# ~ In order to omit Gödel numbers too high, around 300 decimal digits,
# ~ LIMIT_GNUM set to 2**1000 but computed much faster via bit shift

LIMIT_GNUM = 2 << 999

# ~ Ancillary functions to implement mu-linear search and parameterized
# ~ and unparameterized primitive recursion.

def mu(x, test):
    "ancillary linear search function for implementing mu-minimization"
    z = 0
    while not test(cp.dp(x, z)):
        z += 1
    return z


def prim_rec(is_base, base, recurse):
	"ancillary course-of-values primitive recursion more efficient than by minimization"

	def c_of_v(x):
		"create the full course of values"
		sq = 0
		for y in range(x + 1):
			new = base(y) if is_base(y) else recurse(cp.dp(y, sq))
			sq = cp.dp(new, sq)
		return sq

	return lambda x: cp.pr_L(c_of_v(x))


def par_prim_rec(is_base, base, recurse):
	"primitive recursion with parameters - careful, names swapped from the course notes in Spanish"

	def c_of_v(z):
		"create the adequate course of values, not full anymore"
		x = cp.pr_R(z)
		sq = 0 # empty sequence
		for y in range(x + 1):
			new = base(z) if is_base(y) else recurse(cp.dp(z, sq))
			sq = cp.dp(new, sq)
		return sq

	return lambda x: cp.pr_L(c_of_v(x))


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
        self.valid = True   # program is correct until proven wrong
        self.main = dict()  # RENAME some day, as I am using also 'main' for the main function to be called
        self.strcode = dict()
        self.pycode = dict()
        self.gnums = dict()
        self.abouts = list()
        self.pragmas = ddict(str)
        self.store_gnums = store_goedel_numbers 
        self.add_basic("k_1", "The constant 1 function", "lambda x: 1", 0)
        self.add_basic("id", "The identity function", "lambda x: x", 1)
        self.add_basic("s_tup", "Single-argument version of suffix tuple", 
                       "lambda x: cp.s_tup(cp.pr_L(x), cp.pr_R(x))", 2)
        self.add_basic("proj", "Single-argument version of projection", 
                       "lambda x: cp.pr(cp.pr_L(x), cp.pr_R(x))", 3)
        self.add_basic("add", "Addition x+y of the two components of input <x.y>", 
                       "lambda x: cp.pr_L(x) + cp.pr_R(x)", 4)
        self.add_basic("mul", "Multiplication x*y of the two components of input <x.y>", 
                       "lambda x: cp.pr_L(x) * cp.pr_R(x)", 5)
        self.add_basic("diff", "Modified difference max(0, x-y) of the two components of input <x.y>", 
                       "lambda x: max(0, cp.pr_L(x) - cp.pr_R(x))", 6)
        self.parser = Parser()
        self.synt_err_handler = SyntErr()


    def add_basic(self, nick, comment, code, num):
        data = FunData()
        data["nick"] = nick
        data["comment"] = comment
        data["how_def"] = "basic"
        data["def_on"] = tuple()
        if self.store_gnums:
            self.gnums[nick] = cp.dp(0, num)
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
                          "= <" + str(cp.pr_L(gnum)) + "." + str(cp.pr_R(gnum)) + ">")
                else:
                    self.valid &= self.synt_err_handler(fatal = False, info = "Gödel number too large, omitted.")

        if what is not None:
            list_one(what, w_code)
        else:
            for nick in self.main:
                list_one(nick, w_code)


    def define(self, new_funct):
        'here comes a new function to add to the collection'

        if (nick := new_funct['nick']) in self.main:
            'repeated nick, check for consistency'
            if (self.main[nick]["how_def"] != new_funct['how_def'] or
                self.main[nick]["def_on"] != new_funct['def_on']):
                    self.valid &= self.synt_err_handler.report(nonfatal = False, 
                        info = f"Repeated, inconsistent definitions for function '{nick}' found.")
        else:
            self.main[nick] = new_funct
            on_what = new_funct['def_on']

            if new_funct['how_def'] == "comp":
                self.strcode[nick] = "lambda x: " + on_what[0] + "(" + on_what[1] + "(x))"
                if self.store_gnums and on_what[0] in self.gnums and on_what[1] in self.gnums:
                    gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]], self.gnums[on_what[1]]))
                    if gnum < LIMIT_GNUM:
                        self.gnums[nick] = gnum
                    else:
                        self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            info = f"Gödel number for '{nick}' too large, omitted.")

            elif new_funct['how_def'] == "pair":
                self.strcode[nick] = "lambda x: cp.dp(" + on_what[0] + "(x), " + on_what[1] + "(x))"
                if self.store_gnums and on_what[0] in self.gnums and on_what[1] in self.gnums:
                    gnum = cp.dp(2, cp.dp(self.gnums[on_what[0]], self.gnums[on_what[1]]))
                    if gnum < LIMIT_GNUM:
                        self.gnums[nick] = gnum
                    else:
                        self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            info = f"Gödel number for '{nick}' too large, omitted.")
    
            elif new_funct['how_def'] == "mu":
                self.strcode[nick] = "lambda x: mu(x, " + on_what[0] + ")"
                if self.store_gnums and on_what[0] in self.gnums:
                    gnum = cp.dp(3, self.gnums[on_what[0]])
                    if gnum < LIMIT_GNUM:
                        self.gnums[nick] = gnum
                    else:
                        self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            info = f"Gödel number for '{nick}' too large, omitted.")

            elif new_funct['how_def'] == "compair":
                if not self.pragmas['extended']:
                    self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  info = "Use of compair requires '.pragma extended: True', changed.")
                self.pragmas['extended'] = 'True'
                self.strcode[nick] = "lambda x: " + on_what[0] + "( cp.dp(" + on_what[1] + "(x), " + on_what[2] + "(x)))"
                if (self.store_gnums and on_what[0] in self.gnums and 
                    on_what[1] in self.gnums and on_what[2] in self.gnums):
                    gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]],
                           cp.dp(2, cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]]))))
                    if gnum < LIMIT_GNUM:
                        self.gnums[nick] = gnum
                    else:
                        self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            info = f"Gödel number for '{nick}' too large, omitted.")

            elif new_funct['how_def'] == "primrec":
                if not self.pragmas['extended']:
                    self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  info = "Use of primrec requires '.pragma extended: True', changed.")
                self.pragmas['extended'] = 'True'
                self.strcode[nick] = "prim_rec(" + on_what[0] + ", " + on_what[1] + ", " + on_what[2] + ")"
                if (self.store_gnums and on_what[1] in self.gnums and on_what[2] in self.gnums):
                    gnum = cp.dp(4, cp.dp(int(on_what[0]),
                               cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]])))
                    if gnum < LIMIT_GNUM:
                        self.gnums[nick] = gnum
                    else:
                        self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            info = f"Gödel number for '{nick}' too large, omitted.")

            elif new_funct['how_def'] == "parprimrec":
                if not self.pragmas['extended']:
                    self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  info = "Use of parprimrec requires '.pragma extended: True', changed.")
                self.pragmas['extended'] = 'True'
                self.strcode[nick] = "par_prim_rec(" + on_what[0] + ", " + on_what[1] + ", " + on_what[2] + ")"
                if (self.store_gnums and on_what[1] in self.gnums and on_what[2] in self.gnums):
                    gnum = cp.dp(5, cp.dp(int(on_what[0]),
                               cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]])))
                    if gnum < LIMIT_GNUM:
                        self.gnums[nick] = gnum
                    else:
                        self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            info = f"Gödel number for '{nick}' too large, omitted.")

            else:
                "ascii_const, as no other 'how' captured by parser - kept out of the Goedel numbering for the time being"
                if not self.pragmas['extended']:
                    self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  info = "Use of ascii constants requires '.pragma extended: True', changed.")
                self.pragmas['extended'] = 'True'
                self.strcode[nick] = "lambda x: str2int( '" + on_what[0] + "' )"

            self.pycode[nick] = eval(self.strcode[nick], globals() | self.pycode)


    def to_python(self, what):
        'returns the Python-runnable version of the function'
        if what not in self.pycode:
            self.valid &= self.synt_err_handler.report(nonfatal = False, 
                info = f"No Python code for function '{what}' found.")
            return None
        return self.pycode[what]


    def find_script_in_file(self, filename, main):
        try:
            with open(filename) as infile:
                 return infile.read()
        except IOError:
            if main:
                self.valid &= self.synt_err_handler.report(nonfatal = False, 
                              info = f"Script {filename} not found.")
            else:
                self.valid &= self.synt_err_handler.report(nonfatal = True, 
                              info = f"Imported script {filename} not found.")


    def load(self, filename, main = True):
        'load in definitions from .prfs file(s) - use .import to recurse into further loading'
        if filename.endswith('.prfs'):
            self.valid &= self.synt_err_handler.report(nonfatal = True, 
                          info = f"File name {filename} NOT expected to include the '.prfs' extension.")
        else:
            filename += '.prfs'
        script = self.find_script_in_file(filename, main)
        if not script:
            return None
        lastread = None
        for label, what in self.parser.parse(script):
            'make the FunData or store the about or the pragma or the import'
            if label == 'pragma':
                if main:
                    "pragmas in main file are stored"
                    self.pragmas[what[0]] = what[1]
                elif what[0] == 'extended' and what[1] == 'True':
                    "pragmas in imported files are ignored except extended when set to True"
                    if self.pragmas['extended'] != 'True':
                        self.valid &= self.synt_err_handler.report(nonfatal = True, 
                            info = f"Warning: the .pragma extended declaration found in {filename} affects globally.")
                    self.pragmas[what[0]] = what[1]
            if label == 'about':
                self.abouts.append('about ' + filename + ': ' + what) 
            if label == 'define':
                self.define(what)
                lastread = what['nick'] # nickname of the last function defined, used for default main
            if label == "import":
                "non-main recursive call"
                self.load(what, main = False)
        if main and not self.pragmas['main']:
            self.valid &= self.synt_err_handler.report(nonfatal = True, 
                 info = f"No main .pragma found in '{filename}'.")
            if self.valid and lastread:
                "warn that main assumed is lastread"
                self.valid &= self.synt_err_handler.report(nonfatal = True, 
                     info = f"Function '{lastread}' guessed to be the main function, cross fingers.")
                self.pragmas['main'] = lastread
            elif self.valid:
                self.valid &= self.synt_err_handler.report(nonfatal = False, 
                     info = f"No guess available for the main function.")


    def dialog(self):
        nick = input("Function name? ")
        comment = input("What is it? ")
        how = input("How is it made? [pair or comp or mu] ")
        on_what = input("Applied to what? [1 or 2 space-sep names] ")
        self.define(FunData(nick.strip(), comment.strip(), how.strip(), tuple(on_what.split())))


    def check_names(self):
        "checks that all function names needed to run main have been defined"

        def check_name(self, name, need = 'pragma main'):
            if name not in checked:
                checked.add(name)
                if name in self.main:
                    if self.main[name]['how_def'] != "ascii_const":
                        for nname in self.main[name]['def_on']:
                            check_name(self, nname, f"'{name}'")
                else:
                    "newly found undefined name"
                    self.valid &= self.synt_err_handler.report(nonfatal = False, 
                        info = f"Function '{name}' not found but needed by {need}.")

        checked = set()
        check_name(self, self.pragmas['main'])


def run():
    'Stand-alone CLI command to be handled as entry point - no Goedel numbers stored; handle the filename as argument'
    from argparse import ArgumentParser
    from pytokr import pytokr
    read, loop = pytokr(iter = True)
    aparser = ArgumentParser(prog = 'prefscript',
              description = 'Partial Recursive Functions Scripting interpreter')
    aparser.add_argument('filename', help = 'script filename to be run, extension .prfs assumed')
    aparser.add_argument('-a', '--about', 
            help = "show contents of .about directives in file and .import'd files before running",
            action = "store_true")
    aparser.add_argument('-v', '--version', 
            action = "version", version = f'{__version__}')
    args = aparser.parse_args()
    f = PReFScript()
    f.load(args.filename)
    if f.valid:
        f.check_names()
    if f.valid:
        'run it on data from stdin according to input/output/main pragmas'
        if args.about:
            print('\n'.join(f.abouts))

        r = f.to_python(f.pragmas["main"])

        if f.pragmas["output"] in ('', "int"):
            post = lambda x: x
        elif f.pragmas["output"] == "ascii":
            post = int2str
        elif f.pragmas["output"] == "bool":
            post = bool

        if f.pragmas["input"] in ('', "int"):
            arg = int(input()) 
        elif f.pragmas["input"] == "none":
            arg = 42 # for one
        elif f.pragmas["input"] == "intseq":
            arg = cp.tup_i(map(int, loop()))

    if f.valid:
        print(post(r(arg)))


if __name__ == "__main__":
    run()
