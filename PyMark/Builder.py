import types
import Util
from struct import *

"""

This class is used to compile python objects to the PyMark specification.

"""

LIST 			= 1
LONG_LIST		= 2
DICT 			= 3
LONG_DICT		= 4
TUPLE 			= 5
LONG_TUPLE		= 6
STRING 			= 7
LONG_STRING 	= 8
INT 			= 9
LONG 			= 10
FLOAT 			= 11
DOUBLE			= 12
REFERENCE		= 13
NONE			= 14
	
def isSupportedType(o):
	t = type(o)
	return (t == types.ListType) or (t == types.DictType) or (t == types.TupleType) or (t == types.StringType) or (t == types.IntType) or (t == types.FloatType) or (t == types.LongType) or (t == types.NoneType)

def isBuiltInString(o):
	"""
	Checks if an object, at first is a string, and second, the first two chars of which are "__"
	Used for filtering out the __dict__ object you get from modules.
	"""
	try:
		if (o[0] == '_') and (o[1] == '_'):
			return True
		else:
			return False
	except:
		return False
	
def typeLookup(o):
	"""
	Looks up the type index of an object.
	If object is long enough then uses longer vesion.
	If not recognized throws an error.
	"""
	
	t = type(o)
	
	# hacked in
	if (t == types.StringType) and o.startswith(Util.REF_PREFIX): return REFERENCE
	
	# long versions of native types
	if (t == types.ListType) and (len(o) > 65536): return LONG_LIST
	if (t == types.DictType) and (len(o) > 65536): return LONG_DICT
	if (t == types.StringType) and (len(o) > 65536): return LONG_STRING
	if (t == types.TupleType) and (len(o) > 65536): return LONG_TUPLE
	
	# native types
	if t == types.ListType: 	return LIST
	if t == types.DictType: 	return DICT
	if t == types.TupleType: 	return TUPLE
	if t == types.StringType: 	return STRING
	if t == types.IntType:		return INT
	if t == types.FloatType:	return FLOAT
	if t == types.LongType:		return LONG
	if t == types.NoneType:		return NONE
	
	raise StandardError("Unrecognized object of type \""+str(t.__name__)+"\". I don't know how to compile this!")

def compileReference(o):
	"""
	References are compiled into something that resembles a list. First the prefix is removed, then they are exploded around "."
	Strings that look like digits are converted to ints and the whole thing is compiled like a list.
	"""
	
	ref_string = o[len(Util.REF_PREFIX)::]
	ref_code = ref_string.split(".")
	ref_lookup = []
	for p in ref_code:
		if p.isdigit():
			ref_lookup.append(int(p))
		else:
			ref_lookup.append(p)
	o = ref_lookup
	
	return compileList(o)
	
def compileList(o):
	
	if len(o) == 0:
		return pack('>H',0)
	else:
		return pack('>H',len(o)) + reduce(lambda x, y: x+y, map(lambda x: compileObject(x),o) )
	
def compileObject(o):
	"""
	Looks up the type of an object, and based on this decides how to compile it into bytes.
	The algorithm is fairly simple based on recursion for collection objects.
	
	The first thing that gets written is an index representing the type of the object being written (see constants defined at top)
	Then, For collections or objects of variable length, the size is then written.
	Then, For collections, the objects inside are written in turn.
	      For basic types such as int and float and string the object is simply written.
		
	The number of bytes used to store an item is variable. You can use the below table and the code below of size and how I've used the "pack" command.
	Almost everything should fit into 2 bytes, but just in case, larger versions are supported. For example it is unlikely, but isn't unreasonable, to expect a string of over size 65536.
	
	Everything is stored Big Endian and if you want more specifics then you can read the python documentation here: http://docs.python.org/library/struct.html
	
	  pack char : num bytes : max int storeable
	|----------------------------------------------|
		B : 1 : 255
		H : 2 : 65536
		L : 4 : 4294967296
		f : 4
		d : 8		
	|-----------------------------------------------|
	
	"""
	t = typeLookup(o)

	
	if t == LIST:
		return pack('>B',t) + compileList(o)
	elif t == LONG_LIST:
		return pack('>B',t) + compileList(o)
	elif t == DICT:
		return pack('>B',t) + compileList(o.items())
	elif t == LONG_DICT:
		return pack('>B',t) + compileList(o.items())
	elif t == TUPLE:
		return pack('>B',t) + compileList(o)
	elif t == LONG_TUPLE:
		return pack('>B',t) + compileList(o)
	elif t == STRING:
		return pack('>B',t) + pack('>H',len(o)) + o
	elif t == LONG_STRING:
		return pack('>B',t) + pack('>L',len(o)) + o
	elif t == INT:
		return pack('>B',t) + pack('>H',o)
	elif t == FLOAT:
		return pack('>B',t) + pack('>f',o)
	elif t == DOUBLE:
		return pack('>B',t) + pack('>d',o)
	elif t == REFERENCE:
		return pack('>B',t) + compileReference(o)
	elif t == NONE:
		return pack('>B',t)
	