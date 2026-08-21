'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version early Thermidor 2026:
basicfun: class BasicFun to have everything that concerns the list 
of basic functions in a single place. A dict of FunData.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

from fundata import FunData
import cantorpairs as cp
    
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
"lambda x: 1", cp.dp(0, 0))

        self["id"]    = FunData(
"id",
"The identity function", 
"basic", tuple(),
"lambda x: x", cp.dp(0, 1))

        self["s_tup"] = FunData(
"s_tup", 
"Single-argument version of suffix tuple", 
"basic", tuple(),
"lambda x: cp.s_tup(cp.pr_L(x), cp.pr_R(x))", cp.dp(0, 2))

        self["proj"]  = FunData(
"proj",
"Single-argument version of projection", 
"basic", tuple(),
"lambda x: cp.pr(cp.pr_L(x), cp.pr_R(x))", cp.dp(0, 3))

        self["add"]   = FunData(
"add",
"Addition x+y of the two components of input <x.y>", 
"basic", tuple(),
"lambda x: cp.pr_L(x) + cp.pr_R(x)", cp.dp(0, 4))

        self["mul"]   = FunData(
"mul",
"Multiplication x*y of the two components of input <x.y>",
"basic", tuple(),
"lambda x: cp.pr_L(x) * cp.pr_R(x)", cp.dp(0, 5))

        self["diff"]  = FunData(
"diff",
"Modified difference max(0, x-y) of the two components of input <x.y>",     
"basic", tuple(),
"lambda x: max(0, cp.pr_L(x) - cp.pr_R(x))", cp.dp(0, 6))

    def showgnums(self):
        for f in sorted(self, key = lambda x: cp.pr_R(self[x].index)):
            i = cp.pr_R(self[f].index)
            print(f"{i}: {self[f].fname}, {self[f].docst}, Goedel number <0.{i}> = {self[f].index}")

if __name__ == "__main__":
    BasicFun().showgnums()

