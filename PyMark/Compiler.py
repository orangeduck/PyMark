import sys
import os
import re
import types
import util
import builder

class Compiler:
	"""
	Main Compiler class.
	
	Runs in three stages.
	
		~~ Import ~~
	
	First this class imports all of the .py files in the working directory.
	This means that all the modules must be well formed .py files without syntax errors.
	Any errors on import will give a warning but the process will continue to import the other files. 
	
		~~ Precompile ~~
		
	A few things happen here. First the module __dict__ is looked at and any top level objects of native data type are identified.
	These objects are loaded into a special "constants" dictionary for compilation later.
	
	The module object (an object with the same name as the file) is identified and excluded from this constants dictionary.
	The module object is then searched recurrsively for References, and these are constructed and checked with the eval() command.
	
		~~ Compile ~~
	
	Once we have identified the module object, this object is compiled into byte strings using the builder and output as a .pm file in the "compiled" directory.
	
	"""
	def __init__(self):
		"""
		Inits path variables.
		Constructs "compiled" directory if it does not exist.
		"""
		
		self.path = sys.path[0]
		self.compile_path = self.path+"/compiled"
		
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
		
	def reload_module_names(self):
		"""
		Searches the current directory for .py files which are not in the block list.
		"""
		
		block_list = ["pymark"]
		file_strings = os.listdir(self.path)
		file_pairs = map(lambda x: os.path.splitext(x), file_strings )
		file_pairs = filter(lambda x: (x[1] == ".py") and not(x[0] in block_list ) , file_pairs)
		file_list = map(lambda x: x[0], file_pairs )
		
		self.module_names = file_list
		
	def import_module(self,name):
		
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
				
			self.import_errors += 1
			return
			
		self.imported += 1
	
	def import_all_modules(self):
		
		print "Importing modules..."
		print ""
		
		self.reload_module_names()
		self.num_imports = len(self.module_names)
		
		for file_name in self.module_names:
			self.import_module(file_name)
		
		if self.import_errors > 0:
			if self.import_errors == 1:
				print str(self.import_errors)+" Error with import!"
			else:
				print str(self.import_errors)+" Errors with import!"
		
		print ""
		print "Imported "+str(self.imported)+" out of "+str(self.num_imports)+" modules."
	
	def extract_module_objects(self):
		
		for name in self.modules.keys():
			module = self.modules[name]
			import_dict = module.__dict__
			
			try:
				data = import_dict[name]
			except:
				print "ERROR: module \""+name+"\" contains no object called \""+name+"\" to compile!"
				self.compile_errors += 1
				return
			
			if not builder.is_supported_type(data):
				print "ERROR: object \""+name+"\" is of type "+str(type(data.__name__))+". Module objects must be made up of the native types."
				self.compile_errors += 1
				return				
				
			self.module_objects[name] = data
		
	def compile_module_constants(self,import_dict,name):
		"""
		Constants are native type objects in the module that are not the main object.
		These are stored in a special "constants" dictionary in case they need to be used later.
		Constants can be all the natively supported objects.
		"""	
		
		constants_block_list = ["REF_PREFIX"]
		
		try:
			constant_dict = {}
			for k, v in import_dict.iteritems():
				if builder.is_supported_type(v) and not builder.is_builtin_string(k) and k != name and not(k in constants_block_list) :
					constant_dict[k] = v
			
			if len(constant_dict) > 0:
				self.constants[name] = {}
				for k, v in constant_dict.iteritems():
					if k != name:
						self.constants[name][k] = v
		except StandardError as error:
			print "WARNING: could not build constants for object \""+name+"\" : "+str(error)
			self.compile_errors = self.compile_errors + 1
	
	def compile_module(self,name):
		
		print "Compiling module \""+name+"\""
		
		import_dict = self.modules[name].__dict__
		self.compile_module_constants(import_dict,name)
		
		data = self.module_objects[name]
		
		self.check_references(data,name)
		
		try:
			compilestring = builder.compile_object(data)
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
		
	def compile_all_modules(self):
		
		print "Compiling Modules..."
		print ""
		
		self.extract_module_objects()
		
		self.num_compiles = len(self.modules)
		
		keys = self.modules.keys()
		keys.reverse()
		for name in keys:
			self.compile_module(name)
		
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
		
	def compile_constants(self):
		
		print "Compiling Constants..."
		
		data = self.constants
		
		try:
			compilestring = builder.compile_object(data)
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
	
	def check_dictionary_key(self,k,name):
		"""
		Dictionary keys shouldn't be character digit strings because the compiler will always interpret number references as actual numbers.
		"""
		if k.isdigit():
			print "WARNING: character digit string used as key in dictionary in module \""+name+"\" - will be unreferenceable." 
			self.compile_warnings += 1
	
	def check_references(self,o,name):
		"""
		Recursively looks for references in an object and if it finds one, constucts a python statement and uses eval() to see if the reference exists.
		"""
		t = type(o)
		
		if t == types.ListType:
			map(lambda x : self.check_references(x,name),o)
		elif t == types.DictType:
			map(lambda x : self.check_references(x,name),o.values())
			map(lambda x: self.check_dictionary_key(x,name), o.keys())
		elif t == types.TupleType:
			map(lambda x : self.check_references(x,name),o)
		
		elif t == types.StringType:
			
			if o.startswith(util.REF_PREFIX):
				
				ref_string = o[len(util.REF_PREFIX)::]
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
	
	def clear_compile_dictionary(self):
		
		file_strings = os.listdir(self.path+"/compiled")
		for name in file_strings:
			if re.match(r"^.*\.pm$",name):
				os.remove(self.path+"/compiled/"+name)
		
	def run(self,args):
		
		all_modules = (args.modules == [])
		
		print ""
		print "______________________________"
		print ""
		print "Pymark beginning..."			
		print ""
		print "______________________________"
		print ""
		
		if all_modules:
			self.import_all_modules()
		else: # We don't mind if the args are supplied with or without .py extension
			modules = map(lambda x : os.path.splitext(x)[0], args.modules)
			for name in modules:
				self.import_module(name)
		
		print ""
		print "______________________________"
		print ""
		
		if all_modules or args.wipe:
			self.clear_compile_dictionary()
		
		self.compile_all_modules()
		print ""
		if all_modules or args.constants:
			self.compile_constants()
		print "______________________________"
		print ""
		print "            Done"
		print "______________________________"
		print ""