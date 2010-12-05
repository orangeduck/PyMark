import subprocess
import os
import types
from struct import *

"""
I have no idea why you might want to load .pm objects when you can just load the objects using an import...but it isn't my job to ask questions.
In fact I actually do use this with a certain communication thing of mine.

TODO!!!! At the moment tuples are converted to lists. Perhaps this needs changing?!!

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

def isInt(n):
	try:
		int(n)
		return True
	except:
		return False

class PyMarkLoader:

	def __init__(self,_path):
	
		self.path = _path
		self.modules = {}
		
		self.moduleNames = []
		self.reloadModuleNames()
		
		self.clearLog()
		self.logMsg("PyMarkLoader Constructed")
	
	def logMsg(self,msg):
		f = open(self.path+"/Logs/py_loader.log",'a')
		f.write(msg+"\n")
		f.close()
	
	def clearLog(self):
		f = open(self.path+"/Logs/py_loader.log",'w')
		f.write("")
		f.close()
	
	def compile(self):
		self.logMsg("Compiling all modules...")
		
		output = subprocess.check_output(["python", self.path+"\PyMark.py"])
		output = output.replace("\n","")
		
		self.logMsg("<<<<<<")
		self.logMsg(output)
		self.logMsg("<<<<<<")
	
	def compileModules(self,names,flagstring):
		modulestring = " "
		for name in names:
			modulestring += (name+" ")
		
		self.logMsg("Compiling modules "+modulestring)
		
		output = subprocess.check_output(["python", self.path+"PyMark.py",modulestring,flagstring])
		output = output.replace("\n","")
		
		self.logMsg("\n<<<<<<")
		self.logMsg(output)
		self.logMsg("<<<<<<\n")
		
	def reloadModuleNames(self):	
		
		file_strings = os.listdir(self.path+"/Compiled")
		file_pairs = map(lambda x: os.path.splitext(x), file_strings )
		file_pairs = filter(lambda x: (x[1] == ".pm"), file_pairs)
		file_list = map(lambda x: x[0], file_pairs )
		
		self.moduleNames = file_list
		
	def load(self):
		self.logMsg("Loading all Modules...")
		for name in self.moduleNames:
			self.loadModule(name)
		
	def loadModule(self,name):
		self.logMsg("Loading Module "+name)
		
		stream = open(self.path+"/Compiled/"+name+".pm",'rb')
		
		self.modules[name] = self.buildObject(stream)
		
		stream.close()
	
	def buildObject(self,stream):
		type = self.readShort(stream)
		
		if type == LIST:
		
			ret = []
			len = self.readInt(stream)
			for i in range(0,len):
				ret.append(buildObject(stream))
				
			return ret
		
		elif type == LONG_LIST:
			
			ret = []
			len = self.readLong(stream)
			for i in range(0,len):
				ret.append(self.buildObject(stream))
			return ret
			
		elif type == DICT:
			
			ret = {}
			len = self.readInt(stream)
			
			for i in range(0,len):
				pair = self.buildObject(stream)
				ret[pair[0]] = pair[1]
			
			return ret
				
		elif type == LONG_DICT:
		
			ret = {}
			len = self.readLong(stream)
			
			for i in range(0,len):
				pair = self.buildObject(stream)
				ret[pair[0]] = pair[1]
				
			return ret
		
		elif type == TUPLE:
		
			ret = []
			len = self.readInt(stream)
			for i in range(0,len):
				ret.append(self.buildObject(stream))
				
			return ret
		
		elif type == LONG_TUPLE:
		
			ret = []
			len = self.readLong(stream)
			for i in range(0,len):
				ret.append(self.buildObject(stream))
			return ret			
		
		elif type == INT:
			
			return self.readInt(stream)
			
		elif type == LONG:
		
			return self.readLong(stream)
		
		elif type == FLOAT:
		
			return self.readFloat(stream)
		
		elif type == DOUBLE:
		
			return self.readDouble(stream)
		
		elif type == STRING:
		
			return self.readString(stream)
		
		elif type == LONG_STRING:
		
			return self.readLongString(stream)
		
		elif type == REFERENCE:
		
			ret = ""
			len = self.readInt(stream)
			for i in range(0,len):
				ret += str(self.buildObject(stream))
				if i != (len-1):
					ret += "."
			return ret
		
		elif type == NONE:
			return None
		else:
			raise Exception("Unknown type index "+str(type)+", perhaps a badly formed .pm file?")
			return None
	
	def get(self,reference):
		return self.getDom(reference,self.modules)
	
	def getDom(self,reference,domain):
		refList = reference.split(".")
		linkList = []
		for item in refList:
			if isInt(item):
				linkList.append(int(item))
			else:
				linkList.append(item)
		
		return self.getFromList(linkList,domain)
	
	def getFromList(self,linkList,domain):
		key = linkList.pop(0)
		obj = domain[key]
		
		if len(linkList) == 0:
			return obj
		else:
			return self.getFromList(linkList,obj)
		
	def set(self,reference,value):
		self.setDom(reference,value,self.modules)
		
	def setDom(self,reference,value,domain):
		refList = reference.split(".")
		linkList = []
		for item in refList:
			if isInt(item):
				linkList.append(int(item))
			else:
				linkList.append(item)
		
		self.setFromList(linkList,value,domain)
	
	def setFromList(self,linkList,value,domain):
		key = linkList.pop(0)
		
		if len(linkList) == 0:
				domain[key] = value
		else:
			obj = domain[key]
			self.setFromList(linkList,value,obj)
		
		# TODO - replace the rest of these with unpack commands.
	def readShort(self,stream):
		ret = ord(stream.read(1))
		return ret
		
	def readInt(self,stream):
		p1 = ord(stream.read(1))
		p2 = ord(stream.read(1))
		return int((p1 << 8) + (p2))
		
	def readLong(self,stream):
		p1 = ord(stream.read(1))
		p2 = ord(stream.read(1))
		p3 = ord(stream.read(1))
		p4 = ord(stream.read(1))
		return long((p1 << 24) + (p2 << 16) + (p3 << 8) + p4)
		
	def readString(self,stream):
		len = self.readInt(stream)
		ret = ""
		for i in range(0,len):
			ret += chr(self.readShort(stream))
		return ret
		
	def readLongString(self,stream):
		len = self.readLong(stream)
		ret = ""
		for i in range(0,len):
			ret += chr(self.readShort(stream))
		return ret
		
	def readFloat(self,stream):
		bytes = stream.read(4)
		return unpack('>f',bytes)
		
	def readDouble(self,stream):
		byes = stream.read(8)
		return unpack('>d',bytes)