'''
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

'''

class FunData(dict):
	'Simple class for PReFScript functions data - moved to main file'

    def __init__(self):
        dict.__init__(self)
        self["nick"] = None
        self["comment"] = None
        self["how_def"] = None
        self["def_on"] = None

    def __str__(self):
        return self["nick"] + "\n " + self["comment"] 

    def how_def(self):
        return " " + self["how_def"] + ": " + str(self["def_on"]
