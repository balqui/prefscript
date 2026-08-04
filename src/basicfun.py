'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version early Thermidor 2026:
basicfun: class BasicFun to have everything that concerns the list 
of basic functions in a single place. A dict of FunData.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Open: should this be instead a subclass of FunData? 
Current answer: if yes, then this forces basic to be 
nonfrozen so no advantage; am now trying to use FunData 
objects directly. I need them compatible in the AST transformer.
'''

from fundata import FunData
    
class BasicFun(dict):
    '''
    Dictionary with the info required for each basic function.
    '''
    def __init__(self):
        dict.__init__(self)

        self["k_1"]   = FunData(
"k_1", 
"The constant 1 function", 
"basic", tuple(),
"lambda x: 1", 0)

        self["id"]    = FunData(
"id",
"The identity function", 
"basic", tuple(),
"lambda x: x", 1)

        self["s_tup"] = FunData(
"s_tup", 
"Single-argument version of suffix tuple", 
"basic", tuple(),
"lambda x: cp.s_tup(cp.pr_L(x), cp.pr_R(x))", 2)

        self["proj"]  = FunData(
"proj",
"Single-argument version of projection", 
"basic", tuple(),
"lambda x: cp.pr(cp.pr_L(x), cp.pr_R(x))", 3)

        self["add"]   = FunData(
"add",
"Addition x+y of the two components of input <x.y>", 
"basic", tuple(),
"lambda x: cp.pr_L(x) + cp.pr_R(x)", 4)

        self["mul"]   = FunData(
"mul",
"Multiplication x*y of the two components of input <x.y>",
"basic", tuple(),
"lambda x: cp.pr_L(x) * cp.pr_R(x)", 5)

        self["diff"]  = FunData(
"diff",
"Modified difference max(0, x-y) of the two components of input <x.y>",     
"basic", tuple(),
"lambda x: max(0, cp.pr_L(x) - cp.pr_R(x))", 6)
