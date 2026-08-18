'''
Refactoring of a fragment of a piece of code written by Gemini, 
Aug 17th 2026; see gnums_full.py for the prompt and the whole 
program previous to refactoring.
'''

from lark import Lark, Transformer, Tree, Token
from rich import print as rprint
from rich.tree import Tree as RichTree

import cantorpairs as cp

@v_args(inline=True)
class GNumCalc(Transformer):
    '''
    Similar to ScriptMaker; differences: docstrings and import are
    fully ignored here but Goedel numbers are set in the index field.
    '''

    def single(self, cname):
        nm = cname.value
        assert not seemsfactgen(nm), f"Error: name {nm} is disallowed."
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

    def program(self, *defuns):
        print(f"In 'program' received {len(defuns)} subtrees: \n{defuns}")
        return defuns

    def docstring(self, *docstrings):
        pass

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
                assert not fspec.docst, f"Unexpectedly found already" \
                       " a previous docstring in {nm}."
                fspec.docst = docstring
            fspec.fname = nm
            self.script.remove(alias)
        elif nm in self.script:
            "pending name to be completed"
            assert self.script[nm].howdf == "pending", \
                   f"Seems that you have two defs of {self.script[nm]}."
            self.script.remove(nm) # o/w defining it will fail
            fspec = FunData(nm, docst = docstring,
                            howdf = "alias", defon = (alias,))
        else:
            fspec = FunData(nm, docst = docstring,
                            howdf = "alias", defon = (alias,))
        self.script.define(fspec)
        return nm

    def importing(self, filename):
        pass



    def number(self, args):
        token = args[0]
        val = int(token.value)
        # Wrap token in a tree node or store value
        node = Tree("number", [token])
        node.value = val
        return node

    def add(self, args):
        left, right = args[0], args[1]
        node = Tree("add", [left, right])
        node.value = left.value + right.value
        return node

    def mul(self, args):
        left, right = args[0], args[1]
        node = Tree("mul", [left, right])
        node.value = left.value * right.value
        return node

# 3. Convert Lark AST -> Rich Tree with labels
def build_rich_tree(lark_node, rich_parent=None) -> RichTree:
    # Format current node label with color markup
    if isinstance(lark_node, Tree):
        val = getattr(lark_node, "value", "?")
        label = f"[bold cyan]{lark_node.data.upper()}[/bold cyan] [yellow](val = {val})[/yellow]"
    else:  # Leaf Token
        label = f"[green]NUMBER[/green]: {lark_node.value}"

    # Create root or add child
    if rich_parent is None:
        tree = RichTree(label)
    else:
        tree = rich_parent.add(label)

    # Recurse children
    if isinstance(lark_node, Tree):
        for child in lark_node.children:
            build_rich_tree(child, rich_parent=tree)

    return tree

class ShowGNums(GNumCalc):

    def print(self, ast):
        rprint(build_rich_tree(self.transform(ast)))

    def tprint(self, ast):
        "for initial testing during development"
        print(ast.pretty())

    def gprint(self, *asts):
        "for initial testing during development"
        print(f"Got {asts} of len {len(asts)} for gprint.")
        for ast in asts:
            print(ast.pretty())

# ~ Old code to show how gnum's are to be handled in due time:

                # ~ if self.store_gnums and on_what[0] in self.gnums and on_what[1] in self.gnums:
                    # ~ gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]], self.gnums[on_what[1]]))
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")

            # ~ elif new_funct['how_def'] == "pair":
                # ~ self.strcode[nick] = "lambda x: cp.dp(" + on_what[0] + "(x), " + on_what[1] + "(x))"
                # ~ if self.store_gnums and on_what[0] in self.gnums and on_what[1] in self.gnums:
                    # ~ gnum = cp.dp(2, cp.dp(self.gnums[on_what[0]], self.gnums[on_what[1]]))
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")
    
            # ~ elif new_funct['how_def'] == "mu":
                # ~ self.strcode[nick] = "lambda x: mu(x, " + on_what[0] + ")"
                # ~ if self.store_gnums and on_what[0] in self.gnums:
                    # ~ gnum = cp.dp(3, self.gnums[on_what[0]])
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")

            # ~ elif new_funct['how_def'] == "compair":
                # ~ if not self.pragmas['extended']:
                    # ~ self.valid &= self.synt_err_handler.report(nonfatal = True, 
                                  # ~ info = "Use of compair requires '.pragma extended: True', changed.")
                # ~ self.pragmas['extended'] = 'True'
                # ~ self.strcode[nick] = "lambda x: " + on_what[0] + "( cp.dp(" + on_what[1] + "(x), " + on_what[2] + "(x)))"
                # ~ if (self.store_gnums and on_what[0] in self.gnums and 
                    # ~ on_what[1] in self.gnums and on_what[2] in self.gnums):
                    # ~ gnum = cp.dp(1, cp.dp(self.gnums[on_what[0]],
                           # ~ cp.dp(2, cp.dp(self.gnums[on_what[1]], self.gnums[on_what[2]]))))
                    # ~ if gnum < LIMIT_GNUM:
                        # ~ self.gnums[nick] = gnum
                    # ~ else:
                        # ~ self.valid &= self.synt_err_handler.report(nonfatal = False, 
                            # ~ info = f"Gödel number for '{nick}' too large, omitted.")

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
