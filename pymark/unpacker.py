""" Decompilers objects from the PyMark binary spec. """

from struct import *

PyMarkInt     = 1
PyMarkLong    = 2
PyMarkFloat   = 3
PyMarkDouble  = 4
PyMarkBool    = 5
PyMarkNone    = 6
PyMarkString  = 7
PyMarkTuple   = 8
PyMarkList    = 9
PyMarkDict    = 10

PyMarkVersion = 1


def unpack_file(filename):
    f = open(filename, 'rb')
    
    magic = f.read(6)
    if magic != "PYMARK":
        raise IOError("Badly formed PyMark stream. Bad magic number.")
    
    version = ord(f.read(1))
    if version != PyMarkVersion:
        raise IOError("Cannot load PyMark file version %i. Only version %i supported." % (version, PyMarkVersion))
    
    o = unpack_object(f)
    
    f.close()
    return o
    
    
def unpack_object(f):
    
    type = unpack('B', f.read(1))[0]
    
    if type == PyMarkInt: return unpack('i', f.read(4))[0]
    if type == PyMarkLong: return unpack('q', f.read(8))[0]
    if type == PyMarkFloat: return unpack('f', f.read(4))[0]
    if type == PyMarkDouble: return unpack('d', f.read(8))[0]
    if type == PyMarkBool: return unpack('?', f.read(1))[0]
    if type == PyMarkNone: return None
    if type == PyMarkString:
        size = unpack('q', f.read(8))[0]
        return "".join([f.read(1) for i in range(0, size)])
    if type == PyMarkTuple:
        size = unpack('q', f.read(8))[0]
        return tuple([unpack_object(f) for i in range(0, size)])
    if type == PyMarkList:
        size = unpack('q', f.read(8))[0]
        return [unpack_object(f) for i in range(0, size)]
    if type == PyMarkDict:
        size = unpack('q', f.read(8))[0]
        pairs = [unpack_object(f) for i in range(0, size)]
        dict = {}
        for k, v in pairs: dict[k] = v
        return dict
    else:
        raise IOError("Badly formed PyMark stream. Unknown type id %i", type)
        
