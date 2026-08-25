'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version early Fructidor 2026:
computes Goedel numbers up to a limit.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_

Should be a variant of gen_py instead. 

Gemini suggested the idea of a tree on top of rich and to
consider printing only a few digits plus an ellipsis in 
case of Goedel numbers too high. These may be very good 
ideas for the future. See gnums_full.py for the prompt 
and the whole Gemini program of Aug 17th 2026; 
'''

from lark import Lark, Transformer, v_args # Tree, Token
from pathlib import Path                   # for handling imported files

import cantorpairs as cp

from fundata import FunData
from parser import funfact, seemsfactgen, prfsparser
from script import PReFScript       # for the recursive calls on imports

# A handful of ancillary constants and functions

FILENAMES = set()                   # main and imported in order to 
                                    # avoid import cycles - a bit ugly,
                                    # consider designing some other way

LIMIT_GNUM = 2 << 999 # 1000 bits ~ about 300 decimal digits

def sss(index):
    if index == -1:
        return ''
    else:
        h = cp.pr_L(index)
        if h in (0, 3):
            "basic or mu case, single defon"
            d = str(cp.pr_R(index))
        else:
            d = f"<{cp.pr_L(cp.pr_R(index))}.{cp.pr_R(cp.pr_R(index))}>"
        return f" = <{h}.{d}>"

def strfundata(fdat):
    "FunData fields appropriate for Goedel num viewing"
    s = fdat.fname 
    if fdat.howdf == "basic":
        s += f": {fdat.howdf},"
    else:
        s += f": {fdat.howdf}("
        s += ','.join(f"{ff}" for ff in fdat.defon) + "),"
    if fdat.index > -1:
        s += f" {fdat.index}{sss(fdat.index)}"
    return s


@v_args(inline=True)
class GNumCalc(Transformer):
    '''
    Very similar to ScriptMaker; much more than initially expected.
    Sometime in the future try to refactor everything so as to use
    here instead a ScriptMaker and change ONLY in PReFScript gen_py 
    into gen_gnum.
    '''

    def __init__(self, script, filename, import_folder = None, imported = False):
        "filename must be an already resolved Path()"
        super().__init__(self)
        self.script = script
        self.imported = imported
        if import_folder is not None:
            self.import_folder = Path(import_folder)
        else:
            self.import_folder = None
        self.filename = filename
        FILENAMES.add(self.filename)

    def single(self, cname):
        nm = cname.value
        cp.ensure.that(not seemsfactgen(nm), f"Error: name {nm} is disallowed.")
        if nm not in self.script:
            self.script.define(FunData(nm))
        return nm

    def parenth(self, same):
        return same

    def comp(self, left, right):
        nm = funfact()
        fdat = FunData(nm, howdf = "comp", defon = (left, right))
        fdat.index = self.newGnum(1, (left, right))
        self.script.define(fdat)
        return nm

    def pair(self, left, right):
        nm = funfact()
        fdat = FunData(nm, howdf = "pair", defon = (left, right))
        fdat.index = self.newGnum(2, (left, right))
        self.script.define(fdat)
        return nm

    def mu(self, test):
        nm = funfact()
        fdat = FunData(nm, howdf = "mu", defon = (test,))
        fdat.index = self.newGnum(3, (test,))
        self.script.define(fdat)
        return nm

    def newGnum(self, code, defon):
        cp.ensure.that(len(defon) > 0, f"Something is wrong combining {defon}")
        if all(self.script[d].index > -1 for d in defon):
            for ii, d in enumerate(reversed(defon)):
                if ii == 0:
                    nn = self.script[d].index
                else:
                    nn = cp.dp(self.script[d].index, nn)
            nn = cp.dp(code, nn)
            if nn < LIMIT_GNUM:
                return nn
        return -1

    def program(self, *defuns):
        if not self.imported:
            "main file, output Goedel numbers now"
            toohuge = list()
            for name in sorted(self.script, key = lambda nm: self.script[nm].index):
                if self.script[name].index == -1:
                    toohuge.append(name) 
                elif name != "main":
                    print(strfundata(self.script[name]))
            if toohuge:
                print("\nGoedel numbers unavailable, possibly too huge, for:")
                for name in toohuge:
                    print(strfundata(self.script[name]))
        return self.script

    def docstring(self, *docstrings):
        return ''

    def defun(self, cname, docstring, alias):
        "First two cases after skipping main are functions already in the script"
        nm = cname.value
        if seemsfactgen(alias):
            "name to override"
            fspec = self.script[alias]
            if docstring:
                cp.ensure.that(not fspec.docst, 
                    f"Unexpectedly found already a previous docstring in {nm}.")
                fspec.docst = docstring
            fspec.fname = nm
            self.script.remove(alias)
        elif nm in self.script:
            "pending name to be completed"
            cp.ensure.that(self.script[nm].howdf == "pending",
                f"Seems that you have two defs of {self.script[nm]}.")
            idx = self.script[nm].index
            self.script.remove(nm) # o/w defining it will fail
            fspec = FunData(nm, docst = docstring,
                            howdf = "alias", defon = (alias,), index = idx)
        else:
            fspec = FunData(nm, docst = docstring,
                            howdf = "alias", defon = (alias,), index = self.script[alias].index)
        if fspec.fname != "main" or not self.imported:
            "the only main stored is the one of the main file"
            self.script.define(fspec)
        return nm


    def importing(self, filename):

        def attempt(candidate, filename, cnt):
            "try candidate folder, careful with std.prfs"
            path = (candidate / filename).resolve()
            if path.exists():
                cp.ensure.that(filename != "std.prfs" or cnt == 0, 
                    "Presence of a nonstandard std.prfs file in " +
                    f"path {path} is disallowed.")
                return path

        filename = filename.strip('"')
        if not filename.endswith(".prfs"):
            filename += ".prfs"

        import_folders = list()
        if self.import_folder is not None:
            import_folders.append(self.import_folder)
        import_folders.append(self.filename.parent)
        import_folders.append(Path(__file__).parent / "stdprfs")

        importpath = None
        cnt = len(import_folders)
        for candidate in import_folders:
            "ordered search for the imported file"
            cnt -= 1
            importpath = attempt(candidate, filename, cnt)
            if importpath is not None:
                break
        cp.ensure.that(importpath is not None, 
            f"Did not find {filename} to import.")
        if importpath not in FILENAMES:
            FILENAMES.add(importpath)
            local_ast = prfsparser(open(importpath).read())
            local_scrmk = GNumCalc(PReFScript(), importpath, self.import_folder, imported = True)
            local_scr = local_scrmk.transform(local_ast)
            self.script |= local_scr
        return ''


class ShowGNums(GNumCalc):

    def tprint(self, ast):
        "for initial testing during development"
        print(ast.pretty())

    def gprint(self, ast):
        "printing actually occurs in the semantic routine for program"
        self.transform(ast)

'''
# ~ Old code to show how gnum's are to be handled in due time:

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
'''
