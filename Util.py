"""
List of some Utilities for PyMark including References, Flags etc.
"""

def R(string): return Reference(string)
def Ref(string): return Reference(string)
def Reference(string):
	"""
	It isn't smart but I never said it was. Just appends \x01 and a * to the front of a string for identification later.
	No user strings should be using \x01 - at least I hope..
	"""
	return "\x01*"+string

def F(size): return Flagset(size)
def Flags(size): return Flagset(size)	
def Flagset(size):
	list = []
	i = 0
	while i < size:
		list.append(Flag(i))
		i += 1
	return list

def Flag(index):
	if not(isInt(index)):
		print "WARNING: Cannot create flag for "+index+" - indicies must be integers."
		index = 0
	if (index < 0):
		print "WARNING: Cannot create flag for "+index+" - indicies must be greater than or equal to 0"
		index = 0
	return 2**index

def E(size): return Enum(size)
def Enum(size):
	list = []
	i = 0;
	while i < size:
		list.append(i)
		i += 1
	return list
	
	
def isInt(n):
	try:
		int(n)
		return True
	except:
		return False