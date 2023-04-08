import scaff.cantorpairs as cp
from prefscript import PReFScript
my_fs = PReFScript()
# ~ my_fs = PReFScript("Store Gödel numbers")
my_fs.load("script000.prfs")
my_fs.list(w_code = 1)
my_fs.load("script002.prfs")
my_fs.list()
d = my_fs.to_python("div")
print(d(cp.dp(14, 5)))
print(d(cp.dp(15, 5)))
my_fs.list("swap", w_code = 1)
my_fs.list("sign", w_code = 2)
