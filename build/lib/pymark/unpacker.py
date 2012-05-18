""" Decompilers objects from the PyMark binary spec. """

from struct import *

INT     = 1
LONG    = 2
FLOAT   = 3
DOUBLE  = 4
BOOL    = 5
NONE    = 6
STRING  = 7
TUPLE   = 8
LIST    = 9
DICT    = 10 

VERSION = 1

def unpack_file(filename):

    f = open(filename, 'rb')
    o = unpack_stream(f)
    f.close()
    return o


def unpack_stream(f):
    
    magic = f.read(6)
    if magic != "PYMARK":
        raise StandardError("Badly formed PyMark file. Bad magic number.")
    
    version = ord(f.read(1))
    if version != VERSION:
        raise StandardError("Cannot load PyMark file version %i." % version)
    
    return unpack_object(f)
    
    
def unpack_object(f):
    
    type = unpack('B', f.read(1))[0]
    
    if type == INT: return unpack('i', f.read(4))[0]
    if type == LONG: return unpack('q', f.read(8))[0]
    if type == FLOAT: return unpack('f', f.read(4))[0]
    if type == DOUBLE: return unpack('d', f.read(8))[0]
    if type == NONE: return None
    if type == BOOL: return unpack('?', f.read(1))[0]
    if type == STRING:
        size = unpack('q', f.read(8))[0]
        return "".join([f.read(1) for i in range(0, size)])
    if type == TUPLE:
        size = unpack('q', f.read(8))[0]
        return tuple([unpack_object(f) for i in range(0, size)])
    if type == LIST:
        size = unpack('q', f.read(8))[0]
        return [unpack_object(f) for i in range(0, size)]
    if type == DICT:
        size = unpack('q', f.read(8))[0]
        pairs = [unpack_object(f) for i in range(0, size)]
        dict = {}
        for k, v in pairs: dict[k] = v
        return dict
    else:
        raise StandardError("Cannot decompile, badly formed filestream, unknown type id %i", type)
        
