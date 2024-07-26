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

about = "\s*\.about(.*)\n"

pragma = "\s*\.pragma\s+(\w+):?\s+(\w+)\s*"

startdef = "\d+\s+define\:\s*"
group1_nick = "(\w+)\s+"
group2_comment = "\[\s*((\w|\s|[.,:;<>\)\(?\-+*]?)+)\]\s+" # add !, =, has group 4 (or is it 3?) inside
groups5_6_how_on_what = "((pair|comp|mu)\s+(([a-zA-Z_]\w*\s+)*))" # first parenth is group 4, args required not to start with a number

# ~ groups6_7_pair = "(((pair)\s+(\w+\s+\w+)\s+)"
# ~ groups9_10_comp = "|((comp)\s+(\w+\s+\w+)\s+)"
# ~ groups12_13_mu = "|((mu)\s+(\w+)\s+))"

define = (startdef +  
      group1_nick + 
      group2_comment + 
      groups5_6_how_on_what)

script = define + '|' + pragma + '|' + about

for thing in re_finditer(re_compile(script), stdin.read()):
	# ~ nick = thing.group(1)
	# ~ if comment := thing.group(2):
		# ~ comment = comment.strip()
	# ~ how = thing.group(5)
	# ~ if on_what := thing.group(6):
		# ~ on_what = tuple(on_what.split())
	# ~ print(str(how), str(on_what), str(nick), '/'+str(comment)+'/')
	# ~ if g7 := thing.group(7):
		# ~ print("in .about", g7)
	# ~ elif g8 := thing.group(8):
		# ~ print("in .pragma", g8, thing.group(9))
	print("thing seen, stripped:", "-" + thing.group(0).strip() + "-")
	for i, g in enumerate(thing.groups()):
		print("thing group", i+1, g) 



# ~ for thing in re_finditer(re_compile(about), stdin.read()):
	# ~ print("thing seen:", thing.group(0), thing.groups())

# ~ for thing in re_finditer(re_compile(script), stdin.read()):
	# ~ if g16 := thing.group(16):
		# ~ print("in .about", g16)
	# ~ elif g14 := thing.group(14):
		# ~ print("in .pragma", g14, thing.group(15))
	# ~ print("thing seen, stripped:", "-" + thing.group(0).strip() + "-")
	# ~ print("thing groups:", thing.groups())
	# ~ else:
		# ~ funct = thing
		# ~ how = "no-how"
		# ~ on_what = "no-on-what"
	
		# ~ nick = funct.group(1)
		# ~ comment = funct.group(2)
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

'''
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

===== try and get only one group with either pair or comp or mu (or...) and another group with the tuple of strings

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

=====

for funct in re_finditer(re_compile(p1), stdin.read()):
	nick = funct.group(2)
	comment = funct.group(3)
	if funct.group(7) is not None:
		"how becomes 'pair'"
		how = funct.group(7)
	if funct.group(10) is not None:
		how = funct.group(10)
	if funct.group(13) is not None:
		how = funct.group(13)
	if funct.group(8) is not None:
		on_what = tuple(funct.group(8).split())
	if funct.group(11) is not None:
		on_what = tuple(funct.group(11).split())
	if funct.group(14) is not None:
		on_what = tuple(funct.group(14).split())
	print(how.strip(), on_what, nick.strip(), '/'+comment.strip()+'/')
'''
