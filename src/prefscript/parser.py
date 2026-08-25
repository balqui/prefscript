'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version early Fructidor 2026:
Lark-based parser for PReFScript 2.0 onwards.
Script maker moved off to separate codegen.py module.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_
'''

# Grammar and parser

from lark import Lark

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
          | "rec" funspec funspec funspec    -> rec
          | "(" funspec ")"                  -> parenth
          | "ascii_const" ESCAPED_STRING     -> ascii_const

'''

prfsparser = Lark(prfs2_grammar, parser='lalr', start = 'program').parse

