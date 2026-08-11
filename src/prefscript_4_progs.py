#! /usr/bin/python3
'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version mid Thermidor 2026:
prefscript.py: temporary main program

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''


__version__ = "2.0"

from parser import prfsparser, ScriptMaker
from script import PReFScript
    

programs = { 

0: '''
main: id
''',

1: '''
main: f
f: h
h: comp add add
''',

2: '''
main: f
f: h
h: comp add add
g: comp g g
''',

3: '''
main: f
f: comp comp g h comp h g
g: comp g g
h: comp add add
''',

4: '''
main: f
h: comp add add
'''

}

# add(39) = add(<2.6>) = 8
# (add add) (39) = add(add(39)) = add(8) = add(<1.2>) = 3 
# (add add) (8295) = add(add(8295)) = add(add(<32.90>)) = add(128) = add(<7.8>) = 15 
# (add add) (545) = add(add(545)) = add(add(<16.16>)) = add(32) = add(<3.4>) = 7 

while p := input("Program choice (0-4): "):
    ast = prfsparser(programs[int(p)])
    print(ast.pretty())
    scrmk = ScriptMaker(PReFScript())
    scr = scrmk.transform(ast)
    # ~ scr.list(w_code = 2)
    scr.to_python('main')
    mainf = scr.pycode['main']
    # ~ if not scr.valid:
        # ~ break
    print("\nTests:")
    while n := input():
        n = int(n)
        print(mainf(n))
