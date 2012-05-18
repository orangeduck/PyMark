
class module(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        
    def __getattr__(self, attr):
        return self[attr]
    
class struct(module): pass
class properties(module): pass

class enum(module):
    def __init__(self, *args):
        for i, x in enumerate(args): self[x] = i
        
class flags(module):
    def __init__(self, *args):
        for i, x in enumerate(args): self[x] = 2**i

def modifiers(*args): return args
