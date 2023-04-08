import scaff.cantorpairs as cp
from prefscript import PReFScript
my_fs = PReFScript()
my_fs.load("script000.prfs")
my_fs.load("script002.prfs")
my_fs.list()
d = my_fs.to_python("div")
print(d(cp.dp(14, 5)))
print(d(cp.dp(15, 5)))
