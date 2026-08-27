'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version Fructidor 2026:
PraPrePro: pragma pre-processor, handles some CLI options from source.

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

from re import compile as re_compile, finditer as re_finditer, MULTILINE

class PraPrePro:
    '''
    The PRAgma PRE-PROcessor.
    an re-based mini-parser to pre-process pragmas before
    sending the source to the Lark-based PReFScript parser.
    '''

    def __init__(self):
        "group names require Python >= 3.11"
        # ~ from re import compile as re_compile, finditer as re_finditer
        pragma = r"^#pragma\s+(?P<which>\w+):\s*(?P<what>[\.\w]+)\s*$"
        self.process = re_compile(pragma, MULTILINE)

    def parse(self, source):
        for thing in re_finditer(self.process, source):
            things = thing.groupdict(default = '')
            if which := things['which']:
                yield which, things['what']


if __name__ == "__main__":
    prprpr = PraPrePro()
    cnt = 0
    t = '''
# Hello World with output ascii and input none pragmas
#pragma read: nothing
#pragma write: ascii 

main: ascii_const "Hello, World!"
'''
    print(t)
    for a, b in prprpr.parse(t):
        print(cnt, a, b)
        cnt += 1
    print(cnt)
