'''
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Class for PReFScript dicts.
'''

class FunData(dict):

    def __init__(self):
        dict.__init__(self)
        self["nick"] = None
        self["comment"] = None
        self["how_def"] = None
        self["def_on"] = None

    def __str__(self):
        s = self["nick"] + "\n "
        s += self["comment"] 
        return s
