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
    pack_stream(f, o)
    f.close()


def pack_stream(f, o):
    f.write("PYMARK")
    f.write(pack(">B", VERSION))
    pack_object(f, o)
    
    
def pack_object(f, o):
	  
    t = type(o)

    if t == IntType:      f.write(pack('<Bi', INT, o))
    elif t == LongType:   f.write(pack('<Bq', LONG, o))
    elif t == FloatType:  f.write(pack('<Bf', FLOAT, o))
    elif t == NoneType:   f.write(pack('<B' , NONE))
    elif t == StringType:
        f.write(pack('<Bq', STRING, len(o)))
        f.write(o)
    elif t == TupleType:
        f.write(pack('<Bq', TUPLE, len(o)))
        for x in o: pack_object(f, x)
    elif t == ListType:
        f.write(pack('<Bq', LIST, len(o)))
        for x in o: pack_object(f, x)
    elif t == DictType: 
        f.write(pack('<Bq', DICT, len(o)))
        for x in o.items(): pack_object(f, x)
    else:
        raise StandardError("Cannot compile object of type '%s'" % t.__name__)
    
    
    
