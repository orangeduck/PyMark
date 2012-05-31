""" Compiles and Decompilers objects from the PyMark binary spec. """

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
PyMarkMagic = "PYMARK"

def unpack_file(filename):
    f = open(filename, 'rb')
    
    magic = f.read(6)
    if magic != PyMarkMagic:
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
        return dict([unpack_object(f) for i in range(0, size)])
    else:
        raise IOError("Badly formed PyMark stream. Unknown type id %i", type)
    
    
def pack_file(filename, o):
    f = open(filename, 'wb')
    f.write(PyMarkMagic)
    f.write(pack("<B", PyMarkVersion))
    pack_object(f, o)
    f.close()

    
def pack_object(f, o):
    
    if isinstance(o, int): f.write(pack('<Bi', PyMarkInt, o))
    elif isinstance(o, long): f.write(pack('<Bq', PyMarkLong, o))
    elif isinstance(o, float): f.write(pack('<Bf', PyMarkFloat, o))
    elif o is None: f.write(pack('<B' , PyMarkNone))
    elif o is True: f.write(pack('<B?', PyMarkBool, True))
    elif o is False: f.write(pack('<B?', PyMarkBool, False))
    
    elif isinstance(o, str):
        f.write(pack('<Bq', PyMarkString, len(o)))
        f.write(o)
    elif isinstance(o, tuple):
        f.write(pack('<Bq', PyMarkTuple, len(o)))
        for x in o: pack_object(f, x)
    elif isinstance(o, list):
        f.write(pack('<Bq', PyMarkList, len(o)))
        for x in o: pack_object(f, x)
    elif isinstance(o, dict):
        f.write(pack('<Bq', PyMarkDict, len(o)))
        for x in o.items(): pack_object(f, x)
    else:
        f.write(pack('<B' , PyMarkNone))
        

""" Utilities for structuring and marking up data in PyMark """

class struct(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        
    def __getattr__(self, attr):
        return self[attr]
    
class module(struct): pass
class properties(struct): pass

class enum(struct):
    def __init__(self, *args):
        for i, x in enumerate(args): self[x] = i
        
class flags(struct):
    def __init__(self, *args):
        for i, x in enumerate(args): self[x] = 2**i

def modifiers(*args): return args
    