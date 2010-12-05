import sys
import os
import re
import types
import Util
import Builder

class Compiler:
	"""
	Main Compiler class.
	
	Runs in three stages.
	
		~~ Import ~~
	
	First this class imports all of the .py files in the same directory.
	This means that all the modules must be well formed .py files without syntax errors.
	Any errors on import will give a warning but the process will continue to import the other files. 
	
		~~ Precompile ~~
		
	A few things happen here. First the module __dict__ is looked at and any objects of native data type are identified.
	These objects are loaded into a special "constants" dictionary for compilation later.
	
	The module object (an object with the same name as the file) is identified and excluded from this constants dictionary.
	The module object is then searched recurrsively for References, and these are constructed and checked with the eval() command.
	
		~~ Compile ~~
	
	Once we have identified the module object, this object is compiled into byte strings using the Builder class and output as a .pm file in the "Compiled" directory.
	
	"""
	def __init__(self):
		"""
		Inits path variables.
		Constructs "compiled" directory if it does not exist.
		"""
		self.path = sys.path[0]
		self.compile_path = self.path+"/Compiled"
		
		if not os.path.exists(self.compile_path):
			os.mkdir(self.compile_path)
		
		self.modules = {}
		self.module_objects = {}
		self.constants = {}
		
		self.num_imports = 0
		self.num_compiles = 0
		
		self.imported = 0
		self.references = 0
		self.compiled = 0

		self.import_errors = 0
		self.compile_errors = 0
		self.compile_warnings = 0		
		
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
		print "Importing Module \""+name+"\""
		
		try:
			module = __import__(name,[],locals())
			self.modules[name] = module
		except StandardError as error:
			errortext = str(error)
			print "ERROR: Could not import module \""+name+"\" :: "+errortext
			
			# Some friendly error messages.
			if re.match(r".*callable.*",errortext):
				print "Perhaps you're missing a ',' before a tuple?"
			if re.match(r".*subscriptable.*",errortext):
				print "Perhaps you're missing a ',' before a list?"
				
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
	
	def extractModuleObjects(self):
		
		for name in self.modules.keys():
			module = self.modules[name]
			import_dict = module.__dict__
			
			try:
				data = import_dict[name]
			except:
				print "ERROR: module \""+name+"\" contains no object called \""+name+"\" to compile!"
				self.compile_errors += 1
				return
			
			if not(Builder.isSupportedType(data)):
				print "ERROR: object \""+name+"\" is of type "+str(type(data.__name__))+". Module objects must be made up of the native types."
				self.compile_errors += 1
				return				
				
			self.module_objects[name] = data
		
	def compileModuleConstants(self,import_dict,name):
		"""
		Constants are native type objects in the module that are not the main object.
		These are stored in a special "constants" dictionary in case they need to be used later.
		Constants can be all the natively supported objects.
		"""	
		
		constantBlockList = ["REF_PREFIX"]
		
		try:
			constant_dict = {}
			for k, v in import_dict.iteritems():
				if Builder.isSupportedType(v) and not(Builder.isBuiltInString(k)) and k != name and not(k in constantBlockList) :
					constant_dict[k] = v
			
			if len(constant_dict) > 0:
				self.constants[name] = {}
				for k, v in constant_dict.iteritems():
					if k != name:
						self.constants[name][k] = v
		except StandardError as error:
			print "WARNING: could not build constants for object \""+name+"\" : "+str(error)
			self.compile_errors = self.compile_errors + 1
	
	def compileModule(self,name):
		"""
		Tries to compile a module.
		"""
		
		print "Compiling module \""+name+"\""
		
		import_dict = self.modules[name].__dict__
		self.compileModuleConstants(import_dict,name)
		
		data = self.module_objects[name]
		
		self.checkReferences(data,name)
		
		try:
			compilestring = Builder.compileObject(data)
		except StandardError as error:
			print "ERROR: could not compile object \""+name+"\" : "+str(error)
			self.compile_errors = self.compile_errors +1
			return
		
		try:
			f = open(self.compile_path+"/"+name+".pm",'wb')
			f.write(compilestring)
			f.close()
		except StandardError as error:
			print "ERROR: could not write to file \""+name+".pm\": "+str(error)
			self.compile_errors = self.compile_errors +1
			return
		
		self.compiled += 1
		
	def compileAllModules(self):
		"""
		Compiles all modules.
		"""
		
		print "Compiling Modules..."
		print ""
		
		self.extractModuleObjects()
		
		self.num_compiles = len(self.modules)
		
		keys = self.modules.keys()
		keys.reverse()
		for name in keys:
			self.compileModule(name)
		
		print ""		
		if self.compile_errors > 0:
			if self.compile_errors == 1:
				print str(self.compile_errors)+" Error with compilation!"
			else:
				print str(self.compile_errors)+" Errors with compilation!"
		
		if self.compile_warnings > 0:
			if self.compile_warnings == 1:
				print str(self.compile_warnings)+" Warning with compilation!"
			else:
				print str(self.compile_warnings)+" Warnings with compilation!"
		
		print ""
		#print "Checked "+str(self.references)+ " references."
		print "Compiled "+str(self.compiled)+" out of "+str(self.num_compiles)+" modules."
		
	def compileConstants(self):
		"""
		Tries to compile constants.
		"""
		
		print "Compiling Constants..."
		
		data = self.constants
		
		try:
			compilestring = Builder.compileObject(data)
		except StandardError as error:
			print "ERROR: could not compile constants : "+str(error)
			return
		
		try:
			f = open(self.compile_path+"/constants.pm",'wb')
			f.write(compilestring)
			f.close()
		except StandardError as error:
			print "ERROR: unable to open file constants.pm\" for writing: "+str(error)
			return
	
	def checkDictionaryKey(self,k,name):
		"""
		Dictionary keys shouldn't be character digit strings because the compiler will always interprit number references as actual numbers
		"""
		if k.isdigit():
			print "WARNING: character digit string used as key in dictionary in module \""+name+"\" - will be unreferenceable." 
			self.compile_warnings += 1
	
	def checkReferences(self,o,name):
		"""
		Recursively looks for references in an object and if it finds one, constucts a python statement and uses eval() to see if the reference exists.
		"""
		t = type(o)
		
		if t == types.ListType:
			map(lambda x : self.checkReferences(x,name),o)
		elif t == types.DictType:
			map(lambda x : self.checkReferences(x,name),o.values())
			map(lambda x: self.checkDictionaryKey(x,name), o.keys())
		elif t == types.TupleType:
			map(lambda x : self.checkReferences(x,name),o)
		
		elif t == types.StringType:
			
			if o.startswith(Util.REF_PREFIX):
				
				ref_string = o[len(Util.REF_PREFIX)::]
				ref_code = ref_string.split(".")
				# we assume that any numbers in this chain are actually numbers, not character digit strings.
				ref_lookup = ["self.module_objects"]
				for p in ref_code:
					if p.isdigit():
						ref_lookup.append(int(p))
					else:
						ref_lookup.append("\""+p+"\"")
				lookup = reduce(lambda x, y: x+"["+str(y)+"]" , ref_lookup)
				
				try:
					eval(lookup)
					self.references += 1
				except:
					print "WARNING: could not find reference \""+ref_string+"\" in module \""+name+"\""
					self.compile_warnings += 1
					return
		else:
			return	
	
	def clearCompileDirectory(self):
		"""
		Clears the Compiled directory of .pm files.
		"""
		
		file_strings = os.listdir(self.path+"/Compiled")
		for name in file_strings:
			if re.match(r"^.*\.pm$",name):
				os.remove(self.path+"/Compiled/"+name)
		
	def run(self,args):
		
		allModules = (args.modules == [])
		
		print ""
		print "______________________________"
		print ""
		print "Pymark beginning..."			
		print ""
		print "______________________________"
		print ""
		
		if allModules:
			self.importAllModules()
		else:
			modules = map(lambda x : os.path.splitext(x)[0], args.modules) # We don't mind if the args are supplied with or without .py extension
			for name in modules:
				self.importModule(name)
		
		print ""
		print "______________________________"
		print ""
		
		if allModules or args.wipe:
			self.clearCompileDirectory()
		
		self.compileAllModules()
		print ""
		if allModules or args.constants:
			self.compileConstants()
		print "______________________________"
		print ""
		print "            Done"
		print "______________________________"
		print ""