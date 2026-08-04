class SyntErr:
    "handle syntactic errors in the script - VERY PRIMITIVE for the time being"

    def __init__(self):
        from sys import stderr
        self.e = stderr

    def report(self, nonfatal = False, info = ''):
        "return value to be given to the valid field / alt: fatal here and nonvalid at script"
        p = 'Nonf' if nonfatal else 'F'
        print(p + 'atal error in PReFScript:', info, sep = '\n  ', file = self.e)
        return nonfatal

