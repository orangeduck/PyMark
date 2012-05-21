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
