'''
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

from prefscript import PReFScript
my_fs = PReFScript() # to store my functions for this session
# ~ my_fs.list()
my_fs.define("pair", ("k_1", "k_1"), "const_pair_1", "The constant <1.1> function")
my_fs.define("comp", ("add", "const_pair_1"), "k_2", "The constant 2 function")
my_fs.list()
# ~ my_fs.list("k_2")
f = my_fs.to_python("k_2")
print("f(8) = k_2(8) =", f(8))
