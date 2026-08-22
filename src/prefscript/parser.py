'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version late Thermidor 2026:
Lark-based parser and script maker for PReFScript 2.0 onwards.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_

Refactor one day: split in different files the grammar and parser
from the semantic routines in the Transform subclass.
'''

from lark import Lark, Transformer, v_args
from fundata import FunData
from pathlib import Path            # for handling imported files
from script import PReFScript       # for the recursive calls on imports

from cantorpairs import ensure

FILENAMES = set()                   # main and imported in order to 
                                    # avoid import cycles - a bit ugly,
                                    # consider designing some other way

# A handful of ancillary functions

def funfactgen():
    "function name factory generator, get names by calling funfact"
    i = 69
    while True:
        yield f"___{i}"
        i += 1

funfact = funfactgen().__next__

def seemsfactgen(nm):
    return nm.startswith('___') and nm[3:].isdigit()


# Grammar, parser and semantic transformer

prfs2_grammar = '''

%import common.CNAME
%import common.WS
%import common.SH_COMMENT
%import common.CPP_COMMENT
%import common.ESCAPED_STRING

%ignore WS
%ignore SH_COMMENT
%ignore CPP_COMMENT

program   : importing* defun+

importing : "import" ESCAPED_STRING

defun     : CNAME ":" docstring funspec

docstring : ESCAPED_STRING*

funspec   : CNAME                            -> single
          | "comp" funspec funspec           -> comp
          | "pair" funspec funspec           -> pair
          | "mu" funspec                     -> mu
          | "(" funspec ")"                  -> parenth
          | "rec" funspec funspec funspec    -> rec

'''

prfsparser = Lark(prfs2_grammar, parser='lalr', start = 'program').parse

@v_args(inline=True)
class ScriptMaker(Transformer):
    '''
    Instances of transformers traverse the AST in postorder. 
    They need one method for each sort of tree node, that is, 
    grammar label; these methods receive the transformed 
    subtrees and must return the transformed current node.

    The v_args decorator allows the methods in the Transformer
    instance to avoid the "children" tuple and refer directly
    to the subtree funspec's.

    ScriptMaker objects contain a local PReFScript that is 
    "in construction": they transform each AST 'funspec' node into 
    a FunData which gets added to the script, returning its name.
    Imports are handled via recursive calls on a fresh script that
    gets added to the script under construction afterwards.
    
    The 'program' simply returns the finally constructed script.

    Instead of inheriting the name, we set up surrogates and
    leave for later the name change if convenient.
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
        ensure.that(not seemsfactgen(nm), f"Error: name {nm} is disallowed.")
        if nm not in self.script:
            self.script.define(FunData(nm))
        return nm

    def parenth(self, same):
        return same

    def comp(self, left, right):
        nm = funfact()
        fdat = FunData(nm, howdf = "comp", defon = (left, right))
        self.script.define(fdat)
        return nm

    def pair(self, left, right):
        nm = funfact()
        fdat = FunData(nm, howdf = "pair", defon = (left, right))
        self.script.define(fdat)
        return nm

    def mu(self, test):
        nm = funfact()
        fdat = FunData(nm, howdf = "mu", defon = (test,))
        self.script.define(fdat)
        return nm

    def rec(self, recurse, base, is_base):
        nm = funfact()
        fdat = FunData(nm, howdf = "rec", defon = (recurse, base, is_base))
        self.script.define(fdat)
        return nm

    def program(self, *imports_and_defuns):
        return self.script

    def docstring(self, *docstrings):
        "They are tokens, but somehow each can be handled as string"
        return ' '.join(ds.strip('"') for ds in docstrings)

    def defun(self, cname, docstring, alias):
        "First two cases after skipping main are functions already in the script"
        nm = cname.value
        if nm == "main" and self.imported:
            "silently ignore it"
            return ''
        if seemsfactgen(alias):
            "name to override"
            fspec = self.script[alias]
            if docstring:
                ensure.that(not fspec.docst, 
                    f"Unexpectedly found already a previous docstring in {nm}.")
                fspec.docst = docstring
            fspec.fname = nm
            self.script.remove(alias)
        elif nm in self.script:
            "pending name to be completed"
            ensure.that(self.script[nm].howdf == "pending",
                f"Seems that you have two defs of {self.script[nm]}.")
            self.script.remove(nm) # o/w defining it will fail
            fspec = FunData(nm, docst = docstring,
                            howdf = "alias", defon = (alias,))
        else:
            fspec = FunData(nm, docst = docstring,
                            howdf = "alias", defon = (alias,))
        self.script.define(fspec)
        return nm

    def importing(self, filename):

        def attempt(candidate, filename, cnt):
            "try candidate folder, careful with std.prfs"
            path = (candidate / filename).resolve()
            if path.exists():
                ensure.that(filename != "std.prfs" or cnt == 0, 
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
        ensure.that(importpath is not None, 
            f"Did not find {filename} to import.")
        if importpath not in FILENAMES:
            FILENAMES.add(importpath)
            local_ast = prfsparser(open(importpath).read())
            local_scrmk = ScriptMaker(PReFScript(), importpath, imported = True)
            local_scr = local_scrmk.transform(local_ast)
            self.script |= local_scr
        return ''
