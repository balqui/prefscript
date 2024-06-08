'''
Playing with ideas for a clearer, easier to extend parser.

Original pattern:
(\d|\s)*define\:\s*(\w+)\s+\[\s*((\w|\s|[.,:;<>\)\(?\-+*]?)+)\]\s+(((pair)\s+(\w*\s+\w+)\s+)|((comp)\s+(\w*\s+\w+)\s+)|((mu)\s+(\w*)\s+))

Recall:
\d matches decimal digits
\s matches white space
\w matches word characters: underscore and alnum

'''

from re import compile as re_compile, finditer as re_finditer

from sys import stdin

p0 = "(\d|\s)*define\:\s*(\w+)\s+\[\s*((\w|\s|[.,:;<>\)\(?\-+*]?)+)\]\s+(((pair)\s+(\w*\s+\w+)\s+)|((comp)\s+(\w*\s+\w+)\s+)|((mu)\s+(\w*)\s+))"

start = "\d+\s+define\:\s*"
group1_nick = "(\w+)\s+"
group2_comment = "\[\s*((\w|\s|[.,:;<>\)\(?\-+*]?)+)\]\s+" # add !, =, has group 4 inside
groups6_7_pair = "(((pair)\s+(\w+\s+\w+)\s+)"
groups9_10_comp = "|((comp)\s+(\w+\s+\w+)\s+)"
groups12_13_mu = "|((mu)\s+(\w+)\s+))"

p1 = (start +  
      group1_nick + 
      group2_comment + 
      groups6_7_pair + 
      groups9_10_comp + 
      groups12_13_mu)

# try and get only one group with either pair or comp or mu (or...) and another group with the tuple of strings

groups5_6_how_on_what = "((pair|comp|mu)\s+(([a-zA-Z_]\w*\s+)*))" # first parenth is group 4, args required not to start with a number

p2 = (start +  
      group1_nick + 
      group2_comment + 
      groups5_6_how_on_what)

for funct in re_finditer(re_compile(p2), stdin.read()):
	nick = funct.group(1)
	comment = funct.group(2)
	how = funct.group(5)
	on_what = tuple(funct.group(6).split())
	print(how.strip(), on_what, nick.strip(), '/'+comment.strip()+'/')


# ~ for funct in re_finditer(re_compile(p1), stdin.read()):
	# ~ nick = funct.group(2)
	# ~ comment = funct.group(3)
	# ~ if funct.group(7) is not None:
		# ~ "how becomes 'pair'"
		# ~ how = funct.group(7)
	# ~ if funct.group(10) is not None:
		# ~ how = funct.group(10)
	# ~ if funct.group(13) is not None:
		# ~ how = funct.group(13)
	# ~ if funct.group(8) is not None:
		# ~ on_what = tuple(funct.group(8).split())
	# ~ if funct.group(11) is not None:
		# ~ on_what = tuple(funct.group(11).split())
	# ~ if funct.group(14) is not None:
		# ~ on_what = tuple(funct.group(14).split())
	# ~ print(how.strip(), on_what, nick.strip(), '/'+comment.strip()+'/')
