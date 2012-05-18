""" Compiles objects to the PyMark binary spec. """

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

def pack_file(filename, o):
    f = open(filename, 'wb')
    pack_stream(f, o)
    f.close()


def pack_stream(f, o):
    f.write("PYMARK")
    f.write(pack("<B", 1))
    pack_object(f, o)
    
    
def pack_object(f, o):
    
    import sys
    
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
        pass
    
    
    
