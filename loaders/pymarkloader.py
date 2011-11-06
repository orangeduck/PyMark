import subprocess
import os
import types
from struct import *

def is_int(n):
	try:
		int(n)
		return True
	except:
		return False

class PyMarkLoader:
	"""
	This is a class for loading and using pymark data as .pm files. Basic usage looks something like this:
		
	>>> import pymarkloader
	>>> pmloader = pymarkloader.PyMarkLoader("../")
	>>> pmloader.compile()
	>>> pmloader.load()
	>>> pmloader.modules["example_module"]["explorer_jacket"]
		('Explorer Jacket', 'greatcoat_new', 3, 0, 214, {'protection': 11, 'weight': 5}, ('old', 'ragged', 'torn'))
	>>> pmloader.get("example_module.sailor_shirt.4")
		112
	"""

	def __init__(self, path = "./"):
	
		self.path = path
		self.modules = {}
		
		self.module_names = []
		self.reload_module_names()
		
		self.clear_log()
		self.log_msg("PyMarkLoader Constructed")
	
	def log_msg(self, msg):
		f = open(self.path+"/Logs/py_loader.log",'a')
		f.write(msg+"\n")
		f.close()
	
	def clear_log(self):
		f = open(self.path+"/Logs/py_loader.log",'w')
		f.write("")
		f.close()
	
	def compile(self):
		"""
		Compiles all the modules to .pm files.
		"""
		self.log_msg("Compiling all modules...")
		
		output = subprocess.check_output(["python", self.path+"\PyMark.py"])
		output = output.replace("\n","")
		
		self.log_msg("<<<<<<")
		self.log_msg(output)
		self.log_msg("<<<<<<")
	
	def compile_modules(self,names,flagstring):
		"""
		Recompiles a certain module to a .pm file
		"""
		modulestring = " "
		for name in names:
			modulestring += (name+" ")
		
		self.log_msg("Compiling modules "+modulestring)
		
		output = subprocess.check_output(["python", self.path+"PyMark.py",modulestring,flagstring])
		output = output.replace("\n","")
		
		self.log_msg("\n<<<<<<")
		self.log_msg(output)
		self.log_msg("<<<<<<\n")
		
	def reload_module_names(self):	
		"""
		Refreshes the list of potential loadable module names.
		"""
		
		file_strings = os.listdir(self.path+"/Compiled")
		file_pairs = map(lambda x: os.path.splitext(x), file_strings )
		file_pairs = filter(lambda x: (x[1] == ".pm"), file_pairs)
		file_list = map(lambda x: x[0], file_pairs )
		
		self.module_names = file_list
		
	def load(self):
		
		self.log_msg("Loading all Modules...")
		for name in self.module_names:
			self.load_module(name)
		
	def load_module(self,name):
	
		self.log_msg("Loading Module "+name)
		
		stream = open(self.path+"/Compiled/"+name+".pm",'rb')
		
		self.modules[name] = self.read_object(stream)
		
		stream.close()
	
	def get(self, reference):
		"""
		Get an object via a pymark style reference.
		"""
		return self.get_in_domain(reference,self.modules)
	
	def get_in_domain(self, reference, domain):
		"""
		Given a certain object (domain), gets an object via pymark style reference
		"""
		refList = reference.split(".")
		link_list = []
		for item in refList:
			if is_int(item):
				link_list.append(int(item))
			else:
				link_list.append(item)
		
		return self.get_from_list(link_list,domain)
	
	def get_from_list(self, link_list, domain):
		key = link_list.pop(0)
		obj = domain[key]
		
		if len(link_list) == 0:
			return obj
		else:
			return self.get_from_list(link_list,obj)
		
	def set(self, reference, value):
		"""
		Sets a certain object to a value given a pymark style reference
		"""
		self.set_in_domain(reference, value, self.modules)
		
	def set_in_domain(self,reference,value,domain):
		"""
		Given a certain object (domain), sets an object value via pymark style reference
		"""
		refList = reference.split(".")
		link_list = []
		for item in refList:
			if is_int(item):
				link_list.append(int(item))
			else:
				link_list.append(item)
		
		self.set_from_list(link_list,value,domain)
	
	def set_from_list(self,link_list,value,domain):
		key = link_list.pop(0)
		
		if len(link_list) == 0:
				domain[key] = value
		else:
			obj = domain[key]
			self.set_from_list(link_list,value,obj)
		
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
		
	def read_object(self,stream):
		type = self.read_short(stream)
		
		if type == PyMarkLoader.LIST:
			ret = []
			len = self.read_int(stream)
			for i in range(0,len):
				ret.append(read_object(stream))
				
			return ret
		
		elif type == PyMarkLoader.LONG_LIST:
			ret = []
			len = self.read_long(stream)
			for i in range(0,len):
				ret.append(self.read_object(stream))
			return ret
			
		elif type == PyMarkLoader.DICT:
			ret = {}
			len = self.read_int(stream)
			
			for i in range(0,len):
				pair = self.read_object(stream)
				ret[pair[0]] = pair[1]
			
			return ret
				
		elif type == PyMarkLoader.LONG_DICT:
			ret = {}
			len = self.read_long(stream)
			
			for i in range(0,len):
				pair = self.read_object(stream)
				ret[pair[0]] = pair[1]
				
			return ret
		
		elif type == PyMarkLoader.TUPLE:
			ret = []
			len = self.read_int(stream)
			for i in range(0,len):
				ret.append(self.read_object(stream))
				
			return tuple(ret)
		
		elif type == PyMarkLoader.LONG_TUPLE:
			ret = []
			len = self.read_long(stream)
			for i in range(0,len):
				ret.append(self.read_object(stream))
			return ret			
		
		elif type == PyMarkLoader.INT:
			return self.read_int(stream)
			
		elif type == PyMarkLoader.LONG:
			return self.read_long(stream)
		
		elif type == PyMarkLoader.FLOAT:
			return self.read_float(stream)
		
		elif type == PyMarkLoader.DOUBLE:
			return self.read_double(stream)
		
		elif type == PyMarkLoader.STRING:
			return self.read_string(stream)
			
		elif type == PyMarkLoader.LONG_STRING:
			return self.read_long_string(stream)
			
		elif type == PyMarkLoader.REFERENCE:
			ret = ""
			len = self.read_int(stream)
			for i in range(0,len):
				ret += str(self.read_object(stream))
				if i != (len-1):
					ret += "."
			return ret
		elif type == PyMarkLoader.NONE:
			return None
		else:
			raise Exception("Unknown type index "+str(type)+", perhaps a badly formed .pm file?")
			return None
		
		# TODO - replace the rest of these with unpack commands.
	def read_short(self,stream):
		ret = ord(stream.read(1))
		return ret
		
	def read_int(self,stream):
		p1 = ord(stream.read(1))
		p2 = ord(stream.read(1))
		return int((p1 << 8) + (p2))
		
	def read_long(self,stream):
		p1 = ord(stream.read(1))
		p2 = ord(stream.read(1))
		p3 = ord(stream.read(1))
		p4 = ord(stream.read(1))
		return long((p1 << 24) + (p2 << 16) + (p3 << 8) + p4)
		
	def read_string(self,stream):
		len = self.read_int(stream)
		ret = ""
		for i in range(0,len):
			ret += chr(self.read_short(stream))
		return ret
		
	def read_long_string(self,stream):
		len = self.read_long(stream)
		ret = ""
		for i in range(0,len):
			ret += chr(self.read_short(stream))
		return ret
		
	def read_float(self,stream):
		bytes = stream.read(4)
		return unpack('>f',bytes)
		
	def read_double(self,stream):
		byes = stream.read(8)
		return unpack('>d',bytes)