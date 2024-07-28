'''
PReFScript: A Partial Recursive Functions Lab

Rather: Towards a Partial Recursive Functions lab.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Project started: mid Germinal 2003.
Current version: 0.3, early Thermidor 2024.

A Python-based environment to explore and experiment with partial 
recursive functions; naturally doubles as a (purely functional) 
programming language, but it is not intended to be used as such.

Each function in a script has: associated Gödel number, nickname, 
comments, and code (string); also, the last operation used to 
construct it. Then, in a separate dict (used as namespace for 
eval calls), a runnable version of the code.

Nicknames are alphanum strings not starting with a number (no surprise).

CONSIDER ADDING A CLASS FOR HANDLING INFO/WARNING/ERROR/FATAL MESSAGES
'''

from collections import defaultdict as ddict
from re import compile as re_compile, finditer as re_finditer
# ~ import cantorpairs
import cantorpairs as cp
# ~ import scaff.cantorpairs as cp
# ~ import cantorpairs.src.cantorpairs as cp
# ~ from fundata import FunData # class FunData added here now

__version__ = "0.3"

# ~ limit in order to omit Gödel numbers too high, around 300 decimal digits
# ~ LIMIT_GNUM set to 2**1000 but computed much faster via bit shift

from ascii7io import int2str, str2int, int2raw_str # users are not expected to need int2raw_str

# ~ ALSO VALUE .pragma input: none, for the hw.prfs program


LIMIT_GNUM = 2 << 999

class FunData(dict):
    'Simple class for PReFScript functions data'

    def __init__(self, nick = None, comment = None, how_def = None, def_on = None):
        dict.__init__(self)
        self["nick"] = nick
        self["comment"] = comment
        self["how_def"] = how_def
        self["def_on"] = def_on

    def __str__(self):
        return self["nick"] + "\n " + self["comment"] 

    def how_def(self):
        if self["how_def"] == "basic":
            return "basic"
        return self["how_def"] + ": " + ' '.join(on_what for on_what in self["def_on"])


def mu(x, test):
    "ancillary linear search function for implementing mu-minimization"
    z = 0
    while not test(cp.dp(x, z)):
        z += 1
    return z


class Parser:
    '''Prepare an re-based parser to be used upon reading scripts
    The single Parser with single parse generator is likely to mess up
    the recursive imports, I bet it does not work yet.
    '''

    def __init__(self):
        "group names require Python >= 3.11"
        from re import compile as re_compile, finditer as re_finditer
        about = "\s*\.about(?P<about>.*)\n"                           # arbitrary documentation
        pragma = "\s*\.pragma\s+(?P<which>\w+):?\s+(?P<what>\w+)\s*"  # compilation directives
        importing = "\s*\.import(?P<to_import>\w+)\s*"                # additional external script
        a7str = '''(?P<quote>['"])(?P<a7str>.*)(?P=quote)'''
        startdef = "\d+\s+define\:\s*"
        group1_nick = "(?P<nick>\w+)\s+"
        group2_comment = "\[\s*(?P<comment>(\w|\s|[.,:;<>=)(?!/+*-])+)\]\s+"    # has group 3 inside
        # ~ groups_how_on_what = "(?P<how>pair|comp|mu|compair|primrec|ascii_const)\s+(?P<on_what>(\w+\s+)*)" # args NOT required not to start with a number
        group4_how = "(?P<how>pair|comp|mu|compair|primrec|ascii_const)\s+" 
        group5_on_what = "((?P<on_what>([a-zA-Z_]\w*\s+)+)|" + a7str + ")"  # nick args required not to start with a number
        define = (startdef +  
              group1_nick + 
              group2_comment + 
              group4_how +
              group5_on_what)
        self.the_parser = re_compile(define + '|' + about + '|' + pragma + '|' + importing)

    def parse(self, source):
        # ~ from re import compile as re_compile, finditer as re_finditer
        for thing in re_finditer(self.the_parser, source):
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



        # ~ yield 'd', FunData() # or whatever
# ~ for thing in re_finditer(re_compile(script), stdin.read()):
	# ~ nick = thing.group(1)
	# ~ if comment := thing.group(2):
		# ~ comment = comment.strip()
	# ~ how = thing.group(5)
	# ~ if on_what := thing.group(6):
		# ~ on_what = tuple(on_what.split())
	# ~ print(str(how), str(on_what), str(nick), '/'+str(comment)+'/')
	# ~ if g7 := thing.group(7):
		# ~ print("in .about", g7)
	# ~ elif g8 := thing.group(8):
		# ~ print("in .pragma", g8, thing.group(9))
	# ~ print("thing seen, stripped:", "-" + thing.group(0).strip() + "-")
	# ~ for i, g in enumerate(thing.groups()):
		# ~ print("thing group", i+1, g) 

# ~ for thing in re_finditer(re_compile(about), stdin.read()):
	# ~ print("thing seen:", thing.group(0), thing.groups())

# ~ for thing in re_finditer(re_compile(script), stdin.read()):
	# ~ if g16 := thing.group(16):
		# ~ print("in .about", g16)
	# ~ elif g14 := thing.group(14):
		# ~ print("in .pragma", g14, thing.group(15))
	# ~ print("thing seen, stripped:", "-" + thing.group(0).strip() + "-")
	# ~ print("thing groups:", thing.groups())
	# ~ else:
		# ~ funct = thing
		# ~ how = "no-how"
		# ~ on_what = "no-on-what"
	
		# ~ nick = funct.group(1)
		# ~ comment = funct.group(2)
		# ~ if funct.group(7) is not None:
			# ~ "how becomes 'pair'"
			# ~ how = funct.group(7)
		# ~ if funct.group(10) is not None:
			# ~ how = funct.group(10)
		# ~ if funct.group(13) is not None:
			# ~ how = funct.group(13)
		# ~ if funct.group(8) is not None:
			# ~ on_what = tuple(funct.group(8).split())
		# ~ if funct.group(11) is not None:
			# ~ on_what = tuple(funct.group(11).split())
		# ~ if funct.group(14) is not None:
			# ~ on_what = tuple(funct.group(14).split())
		# ~ print(how.strip(), on_what, nick.strip(), '/'+comment.strip()+'/')

        # ~ for funct in re_finditer(self.patt, script):
            # ~ nick = funct.group(2)
            # ~ comment = funct.group(3)
            # ~ if funct.group(7) is not None:
                # ~ how = funct.group(7)
            # ~ if funct.group(10) is not None:
                # ~ how = funct.group(10)
            # ~ if funct.group(13) is not None:
                # ~ how = funct.group(13)
            # ~ if funct.group(8) is not None:
                # ~ on_what = tuple(funct.group(8).split())
            # ~ if funct.group(11) is not None:
                # ~ on_what = tuple(funct.group(11).split())
            # ~ if funct.group(14) is not None:
                # ~ on_what = tuple(funct.group(14).split())


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
        (re compilation moved from load to here so as to avoid
         recomputing it with several load calls - this is going
         to change right next)
        '''
        self.valid = True # program is correct until proven wrong
        self.main = dict()
        self.strcode = dict()
        self.pycode = dict()
        self.gnums = dict()
        self.abouts = list()
        self.pragmas = ddict(str)
        self.store_gnums = store_goedel_numbers 
        # ~ self.hownums = { "basic": 0, "comp": 1, "pair": 2, "mu": 3 } # extend with compair and primrec and arbitrary int/ascii constants
        # ~ self.hownums["ascii_const"] = 6
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
        # ~ self.patt = re_compile("(\d|\s)*define\:\s*(\w+)\s+\[\s*((\w|\s|[.,:;<>\)\(?\-+*]?)+)\]\s+(((pair)\s+(\w*\s+\w+)\s+)|((comp)\s+(\w*\s+\w+)\s+)|((mu)\s+(\w*)\s+))")
        self.parser = Parser()



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
                    print(" Gödel number too large, omitted")

        if what is not None:
            list_one(what, w_code)
        else:
            for nick in self.main:
                list_one(nick, w_code)


# ~ self.hownums = { "basic": 0, "comp": 1, "pair": 2, "mu": 3 } # extend with compair and primrec and arbitrary int/ascii constants
# ~ self.hownums["ascii_const"] = 6
# ~ pair|comp|mu|compair|primrec|ascii_const
# ~ nick, comment, how_def, def_on
# ~ def define(self, how, on_what, nick, comment):

    def define(self, new_funct):
        'here comes a new function to add to the collection'
        if new_funct['nick'] in self.main:
            'repeated nick, check for consistency, PENDING until error reporting in place'
            self.valid = False

            # ~ if (self.main[nick]["how_def"] != how or
                # ~ self.main[nick]["def_on"] != on_what):
                    # ~ self.valid = False
                    # ~ print("Script not valid:", nick, "defined in incompatible ways more than once.")
            # ~ return None

        nick = new_funct['nick']
        self.main[nick] = new_funct
        on_what = new_funct['def_on']

        # ~ numhow = self.hownums[how]
        # ~ if numhow == 0:
            # ~ print("Addition of new basic functions is unsupported as yet. New definition ignored.")
            # ~ return None
        # ~ wrong = ""
        # ~ if numhow < 4 and on_what[0] not in self.main:
            # ~ wrong = on_what[0]
        # ~ elif numhow < 3 and on_what[1] not in self.main:
            # ~ wrong = on_what[1]
        # ~ if numhow < 6 and wrong:
            # ~ "ALL THE HANDLING OF ERRORS TO BE REFACTORED"
            # ~ print("Nickname " + wrong + " unknown. Definition of " + nick + " ignored.")
            # ~ return None
        # ~ data = FunData()
        # ~ data["nick"] = nick
        # ~ data["comment"] = comment
        # ~ data["how_def"] = how
        # ~ data["def_on"] = on_what

# ~ TO TAKE CARE OF ERRORS LEFT FOR LATER ON - REMEMBER TO TEST THE LENGTH OF on_what

        if new_funct['how_def'] == "comp":
            if on_what[0] not in self.main:
                self.valid = False
            if on_what[1] not in self.main:
                self.valid = False
            self.strcode[nick] = "lambda x: " + on_what[0] + "(" + on_what[1] + "(x))"
            if self.store_gnums and on_what[0] in self.gnums and on_what[1] in self.gnums:
                gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]], self.gnums[on_what[1]]))
                if gnum < LIMIT_GNUM:
                    self.gnums[nick] = gnum

        elif new_funct['how_def'] == "pair":
            if on_what[0] not in self.main:
                self.valid = False
            if on_what[1] not in self.main:
                self.valid = False
            self.strcode[nick] = "lambda x: cp.dp(" + on_what[0] + "(x), " + on_what[1] + "(x))"
            if self.store_gnums and on_what[0] in self.gnums and on_what[1] in self.gnums:
                gnum = cp.dp(2, cp.dp(self.gnums[on_what[0]], self.gnums[on_what[1]]))
                if gnum < LIMIT_GNUM:
                    self.gnums[nick] = gnum

        elif new_funct['how_def'] == "mu":
            if on_what[0] not in self.main:
                self.valid = False
            self.strcode[nick] = "lambda x: mu(x, " + on_what[0] + ")"
            if self.store_gnums and on_what[0] in self.gnums:
                gnum = cp.dp(3, self.gnums[on_what[0]])
                if gnum < LIMIT_GNUM:
                    self.gnums[nick] = gnum

        elif new_funct['how_def'] == "compair":
            if on_what[0] not in self.main:
                self.valid = False
            if on_what[1] not in self.main:
                self.valid = False
            if on_what[2] not in self.main:
                self.valid = False
            self.strcode[nick] = "lambda x: " + on_what[0] + "( cp.dp(" + on_what[1] + "(x), " + on_what[2] + "(x)))"
            if (self.store_gnums and on_what[0] in self.gnums and 
                on_what[1] in self.gnums and on_what[2] in self.gnums):
                gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]],
                       cp.dp(2, cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]]))))
                if gnum < LIMIT_GNUM:
                    self.gnums[nick] = gnum

        elif new_funct['how_def'] == "primrec":
            # ~ if on_what[0] not in self.main:
                # ~ self.valid = False
            # ~ if on_what[1] not in self.main:
                # ~ self.valid = False
            # ~ if on_what[2] not in self.main:
                # ~ self.valid = False
            self.valid = False                       # NOT READY YET
            # ~ self.strcode[nick] = "lambda x: " + on_what[0] + "( cp.dp(" + on_what[1] + "(x), " + on_what[2] + "(x)))"
            # ~ if (self.store_gnums and on_what[0] in self.gnums and 
                # ~ on_what[1] in self.gnums and on_what[2] in self.gnums):
                # ~ gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]],
                       # ~ cp.dp(2, cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]]))))
                # ~ if gnum < LIMIT_GNUM:
                    # ~ self.gnums[nick] = gnum

        elif new_funct['how_def'] == "ascii_const":
            "ascii_const functions kept out of the Goedel numbering for the time being"
            self.strcode[nick] = "lambda x: str2int( '" + on_what[0] + "' )"

        else:
            "to handle better at some point"
            self.valid = False
            print("something wrong related to:", new_funct['how_def'])

        self.pycode[nick] = eval(self.strcode[nick], globals() | self.pycode)


    def to_python(self, what):
        'returns the Python-runnable version of the function'
        if not self.valid:
            print("Script not valid. Run with care.")
        if what not in self.pycode:
            print("Nickname " + what + " not defined.")
            return None
        return self.pycode[what]


    def load(self, filename):
        'load in definitions from .prfs file - accepts several calls in sequence - also accepts recursive imports - MIND, on a single parser'
        with open(filename) as infile:
            "filename expected to end with .prfs but not enforced nor defaulted to"
            script = infile.read()
        for label, what in self.parser.parse(script):
            'make the FunData or store the about or the pragma or the import'
            if label == 'pragma':
                self.pragmas[what[0]] = what[1] 
            if label == 'about':
                self.abouts.append(what) 
            if label == 'define':
                "Right now undo the FunData creation to create it again later, must refactor"
                self.define(FunData(what["nick"], what["comment"], what["how_def"], what["def_on"]))
                lastread = what['nick'] # nickname of the last function defined, use it for default main
            if label == "import":
                self.load(what)
        if not self.pragmas['main']:
            self.pragmas['main'] = lastread

            # ~ CAREFUL WITH .pragma'S IN IMPORTED FILES


    def dialog(self):
        nick = input("Function nickname? ")
        comment = input("What is it? ")
        how = input("How is it made? [pair or comp or mu] ")
        on_what = input("Applied to what? [1 or 2 space-sep names] ")
        self.define(FunData(nick.strip(), comment.strip(), how.strip(), tuple(on_what.split())))


    def check_names(self, name = ''):
        if not name and self.pragmas['main']:
            name = self.pragmas['main']
        for nname in self.main[name]['def_on']:
            if nname in self.main:
                self.check_names(nname)
            elif self.main[name]['how_def'] != "ascii_const":
                self.valid = False
                print("Script not valid:", nname, "not found but needed by", name)



def run():
    'Stand-alone CLI command to be handled as entry point - no Goedel numbers stored'
    # ~ handle the filename as argument
    from argparse import ArgumentParser
    aparser = ArgumentParser(prog = 'prefscript',
              description = 'Partial Recursive Functions Scripting interpreter')
    aparser.add_argument('filename', help = 'Script filename')
    # ~ ADD A HELP OPTION BASED ON THE .about CLAUSES, IN GOOD ORDER
    args = aparser.parse_args()
    f = PReFScript()
    f.load(args.filename)
    f.check_names()
    if f.valid:
        'run it on data, an int for now coming along in stdin, REFACTOR whether load returns status'
        r = f.to_python(f.pragmas["main"])
        if f.pragmas["output"] in ('', "int"):
            post = lambda x: x
        elif f.pragmas["output"] == "ascii":
            post = int2str
        elif f.pragmas["output"] == "bool":
            post = bool
        else:
            "error message?"
            pass
        # extend with other options
        if f.pragmas["input"] in ('', "int"):
            arg = int(input()) 
        elif f.pragmas["input"] == "none":
            arg = 666 # for one
        elif f.pragmas["input"] == "intseq":
            arg = cp.tup_i(map(int, input().split()))
        else:
            "error message?"
            pass

        # ~ v3 = input().split() # temporary for is pyth 01             

        arg = cp.dp(cp.pr(arg, 0), cp.dp(cp.pr(arg, 1), cp.pr(arg, 2)))
        print(post(r(arg)))
        # temporary for is pyth 01           

        # ~ rv3 = cp.dp(int(v3[0]), cp.dp(int(v3[1]), int(v3[2])))
        # ~ print(post(r(cp.dp(int(v3[0]), cp.dp(int(v3[1]), int(v3[2]))))))
        # ~ print(rv3, post(r(rv3)))


        # ~ print(arg, cp.pr(arg, 0), cp.pr(arg, 1), cp.pr(arg, 2))
        # ~ print(post(r(arg)))

        # ~ CHOOSE ACCORDING TO .pragma input
        # ~ print(post(r(666))) 
        # ~ v = int(input()) # temporary for frag_is pyth 01
        # ~ for i in range(v):
            # ~ for j in range(v):
            # ~ print(i, post(r(i)))

if __name__ == "__main__":
    run()
