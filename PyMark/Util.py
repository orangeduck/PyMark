"""
List of some Utilities for PyMark including References, Flags etc.
"""

REF_PREFIX = "*PYMARK-REFERENCE*"

def R(string): return Reference(string)
def Ref(string): return Reference(string)
def Reference(string):
	"""
	It isn't smart but I never said it was. Just appends some prefix to the front of a string for identification later.
	No user strings should be using that particular prefix...at least I hope not.
	"""
	return REF_PREFIX+string

def F(size): return Flagset(size)
def Flags(size): return Flagset(size)	
def Flagset(size):
	"""
	Returns list of powers of two - for binary encoded flags. These flags are possible to pull out again using the constants file.
	"""
	list = []
	i = 0
	while i < size:
		list.append(Flag(i))
		i += 1
	return list

def Flag(index):
	if not(isInt(index)) or (index < 0):
		print "WARNING: Cannot create flag for "+index+" - indicies must be integers that are greater than or equal to 0."
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
	

# Other unimportant functions below ...	

def isInt(n):
	try:
		int(n)
		return True
	except:
		return False