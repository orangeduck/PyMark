from pymark.util import flags, enum

merchandise, reward, bonus = flags(3)
body_armor, helmets, gloves, boots = enum(4)

def modifiers(*args): return args;
def cost(x): return x

example_module = {
	"explorer_jacket" : ( "Explorer Jacket", "greatcoat_new", merchandise|reward, body_armor, cost(214), {"weight" : 5, "protection" : 11}, modifiers("old", "ragged", "torn") ),
	"chaps" 	   	  : ( "Chaps", "chaps", merchandise|bonus, boots, cost(23), {"weight" : 1, "protection" : 2}, modifiers("wrapped", "posh", "battered") ),	
	"sailor_shirt"    : ( "Sailor Shirt", "sailor_shirt", merchandise, body_armor, cost(112), {"weight" : 3, "protection" : 4}, modifiers("wet") ),
	"pegleg" 	      : ( "Peg Leg", "peg_leg_m", None, boots, cost(321), {"weight" : 7, "protection" : 4}, modifiers("wonky", "new") ),	
}
