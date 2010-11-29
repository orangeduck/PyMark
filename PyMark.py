import sys
import os
import re
import types
from struct import *
import argparse

"""
These constants are the indicies for the types supported by PyMark.
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

def typeLookup(o):
	"""
	Looks up the type index of an object.
	If object is long enough then uses longer vesion.
	If not recognized throws an error.
	"""
	
	t = type(o)
	
	if (t == types.ListType) and (len(o) > 65536): return LONG_LIST
	if (t == types.DictType) and (len(o) > 65536): return LONG_DICT
	if (t == types.StringType) and (len(o) > 65536): return LONG_STRING
	if (t == types.TupleType) and (len(o) > 65536): return LONG_TUPLE
	
	if t == types.ListType: 	return LIST
	if t == types.DictType: 	return DICT
	if t == types.TupleType: 	return TUPLE
	if t == types.StringType: 	return STRING
	if t == types.IntType:		return INT
	if t == types.FloatType:	return FLOAT
	if t == types.LongType:		return LONG
	
	raise StandardError("Unrecognized object of type \""+str(t.__name__)+"\". I don't know how to compile this!")
	
def compileObject(o):
	"""
	Looks up the type of an object, and based on this decides how to compile it into bytes.
	The algorithm is fairly simple based on recursion for larger objects.
	
	The first thing that gets written is the type of the object being written
	For lists or objects of variable length, the size is then written
	
	Then, for collections, the objects inside are written in turn.
		for basic types such as int and float and string the object is simply written.
		
	The number of bytes used to store an item is variable. You can use the below table and the code below of size.
	
	TODO: Improve this information.
	
	  pack char : num bytes : max number storeable
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
		return pack('>B',t) + pack('>H',len(o)) + reduce(lambda x, y: x+y, map(lambda x: compileObject(x),o) )
	elif t == LONG_LIST:
		return pack('>B',t) + pack('>L',len(o)) + reduce(lambda x, y: x+y, map(lambda x: compileObject(x),o) )
	elif t == DICT:
		return pack('>B',t) + pack('>H',len(o)) + reduce(lambda x, y: x+y, map(lambda x: compileObject(x),o.items() ) )
	elif t == LONG_DICT:
		return pack('>B',t) + pack('>L',len(o)) + reduce(lambda x, y: x+y, map(lambda x: compileObject(x),o.items() ) )
	elif t == TUPLE:
		return pack('>B',t) + pack('>H',len(o)) + reduce(lambda x, y: x+y, map(lambda x: compileObject(x),o) )
	elif t == LONG_TUPLE:
		return pack('>B',t) + pack('>L',len(o)) + reduce(lambda x, y: x+y, map(lambda x: compileObject(x),o) )
	elif t == STRING:
		return pack('>B',t) + pack('>H',len(o.encode("ascii"))) + o.encode("ascii")
	elif t == LONG_STRING:
		return pack('>B',t) + pack('>L',len(o.encode("ascii"))) + o.encode("ascii")
	elif t == INT:
		return pack('>B',t) + pack('>H',o)
	elif t == FLOAT:
		return pack('>B',t) + pack('>f',o)
	elif t == DOUBLE:
		return pack('>B',t) + pack('>d',o)


class PyMark:
	"""
	Main PyMark class.
	
	Runs in two stages.
	
		~~ Import ~~
	
	First this class imports all of the .py files in the same directory.
	This means that all the modules must be well formed .py files without syntax errors.
	Any errors on import will give a warning but the process will continue to import the other files. 
	
		~~ Compile ~~
	
	Within each imported module the script looks for a object with the same name as the file.
	This object is compiled into byte strings using compileObject() and output as a .pm file in the "compiled" directory.
	
	"""
	def __init__(self):
		"""
		Inits path variables.
		Constructs "compiled" directory if it does not exist.
		"""
		self.path = os.getcwd()
		self.compile_path = self.path+"/Compiled"
		
		if not os.path.exists(self.compile_path):
			os.mkdir(self.compile_path)
		
		self.modules = {}
		
		self.num_imports = 0
		self.num_compiles = 0
		
		self.imported = 0
		self.compiled = 0
		
		self.import_errors = 0
		self.compile_errors = 0
		
		self.module_names = []
		
	def reloadModuleNames(self):
		"""
		Searches the current directory for .py files which are not in the block list.
		
		TODO: Allow user regular expression for blocking files.
		"""
		
		block_list = ["PyMark"]
		file_strings = os.listdir(self.path)
		file_pairs = map(lambda x: os.path.splitext(x), file_strings )
		file_pairs = filter(lambda x: (x[1] == ".py") and not(x[0] in block_list ) , file_pairs)
		file_list = map(lambda x: x[0], file_pairs )
		
		self.module_names = file_list
		
	def importModule(self,name):
		"""
		Tries to import a module of a given name.
		"""
		print "Importing Module \""+name+"\" ..."
		
		try:
			module = __import__(name)
			self.modules[name] = module
		except StandardError as error:
			print "ERROR: Could not import module \""+name+"\" :: "+str(error)
			self.import_errors = self.import_errors +1
			return
	
		self.imported += 1
	
	def importAllModules(self):
		"""
		Loads module names and attempts to import all of them.
		"""
		
		print "Importing modules..."
		print ""
		
		self.reloadModuleNames()
		self.num_imports = len(self.module_names)
		
		for file_name in self.module_names:
			self.importModule(file_name)
		
		if self.import_errors > 0:
			if self.import_errors == 1:
				print str(self.import_errors)+" Error with import!"
			else:
				print str(self.import_errors)+" Errors with import!"
		
		print ""
		print "Imported "+str(self.imported)+" out of "+str(self.num_imports)+" modules."
		
	def compileModule(self,name):
		"""
		Tries to compile a module.
		"""
		
		module = self.modules[name]
		print "Compiling Module \""+name+"\" ..."
		
		try:
			data = module.__dict__[name]
		except:
			print "ERROR: module \""+name+"\" contains no object called \""+name+"\" to compile!"
			self.compile_errors = self.compile_errors + 1
			return
		
		first_order_types = [types.ListType,types.DictType,types.TupleType]
		if not(type(data) in first_order_types):
			print "ERROR: object \""+name+"\" is of type "+str(type(data.__name__))+". Module objects must be of type List, Dict or Tuple."
			self.compile_errors = self.compile_errors +1
			return
		
		try:
			compilestring = compileObject(data)
		except StandardError as error:
			print "ERROR: could not compile object \""+name+"\" : "+str(error)
			self.compile_errors = self.compile_errors +1
			return
		
		try:
			f = open(self.compile_path+"/"+name+".pm",'w')
			f.write(compilestring)
			f.close()
		except StandardError as error:
			print "ERROR: unable to open file \""+name+".pm\" for writing: "+str(error)
			self.compile_errors = self.compile_errors +1
			return
		
		self.compiled += 1
		
	def compileAllModules(self):
		"""
		Compiles all modules.
		"""
		
		print "Compiling Modules..."
		print ""
		
		self.num_compiles = len(self.modules)
		
		keys = self.modules.keys()
		keys.reverse()
		for name in keys:
			self.compileModule(name)
		
		if self.compile_errors > 0:
			if self.compile_errors == 1:
				print str(self.compile_errors)+" Error with compilation!"
			else:
				print str(self.compile_errors)+" Errors with compilation!"		
		
		print ""
		print "Compiled "+str(self.compiled)+" out of "+str(self.num_compiles)+" modules."
		
	def run(self,modules):
		
		print ""
		print "______________________________"
		print ""
		print "Pymark beginning..."			
		print ""
		print "______________________________"
		print ""
		
		if modules == []:
			self.importAllModules()
		else:
			modules = map(lambda x : os.path.splitext(x)[0], modules) # We don't mind if the args are supplied with or without .py extension
			for name in modules:
				self.importModule(name)
		
		print ""
		print "______________________________"
		print ""
		self.compileAllModules()


"""
Parsing the args here

Can be supplied with a list of modules. Otherwise if given blank list then just compiles all.
"""

parser = argparse.ArgumentParser(description='Compile .py files using PyMark')
parser.add_argument('modules', metavar='M', nargs='*',help='A list of modules to compile')
args = parser.parse_args(sys.argv[1::])

pymark = PyMark()
pymark.run(args.modules)
