
class S:
    "1-shot snippet to reinterpret the earliest scripts"

    def __init__(self):
        self.n = 0
        self.output = open("script.prf", "w")

    def define(self, how, on_what, nick, comment):
        print(self.n, "|", nick, "|", comment, "|", 
              how, "|", " ".join(on_what), "|", file = self.output)
        self.n += 1

    def bye(self):
        self.output.close()
