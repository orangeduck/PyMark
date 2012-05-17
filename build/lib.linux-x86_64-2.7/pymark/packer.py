""" Compiles objects to the PyMark binary spec. """

from types import *
from struct import *

INT     = 1
LONG    = 2
FLOAT   = 3
DOUBLE  = 4
NONE    = 5
STRING  = 6
TUPLE   = 7
LIST    = 8
DICT    = 9 

VERSION = 1

def pack_file(filename, o):
    
    f = open(filename, 'wb')
    f.write("PYMARK")
    f.write(pack(">B", VERSION))
    f.write(pack_object(o))
    f.close()
    
    
def pack_object(o):
	
    t = type(o)

    if t == IntType:     return pack('<Bi', INT, o)
    elif t == LongType:  return pack('<Bq', LONG, o)
    elif t == FloatType: return pack('<Bf', FLOAT, o)
    elif t == NoneType:  return pack('<B' , NONE)
    elif t == StringType:return pack('<Bq', STRING, len(o)) + o
    elif t == TupleType: return pack('<Bq', TUPLE, len(o)) + "".join([pack_object(x) for x in o])
    elif t == ListType:  return pack('<Bq', LIST, len(o)) + "".join([pack_object(x) for x in o])
    elif t == DictType:  return pack('<Bq', DICT, len(o)) + "".join([pack_object(x) for x in o.items()])
    else: raise StandardError("Cannot compile object of type '%s'" % t.__name__)
