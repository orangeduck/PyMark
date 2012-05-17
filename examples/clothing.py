""" Clothing Objects for Game """

from pymark.util import flags, enum, module, properties, modifiers

Merchandise, Reward, Bonus = flags(3)
BodyArmor, Helmets, Gloves, Boots = enum(4)

clothing = module (

	explorer_jacket = ["Explorer Jacket", "greatcoat_new",  Merchandise | Reward, BodyArmor, 
	                   properties(cost = 214, weight = 5, protection = 11), modifiers("old", "ragged", "torn") ],
	                   
	chaps 	   	    = ["Chaps", "chaps",  Merchandise | Bonus, Boots, 
	                   properties(cost = 23, weight = 1, protection = 2), modifiers("wrapped", "posh", "battered") ],
	                    	
	sailor_shirt    = ["Sailor Shirt", "sailor_shirt", Merchandise, BodyArmor, 
	                   properties(cost = 112, weight = 3, protection = 4), modifiers("wet") ],
	
	pegleg 	        = ["Peg Leg", "peg_leg_m", None, Boots, 
	                   properties(cost = 321, weight = 7, protection = 4), modifiers("wonky", "new") ]

)
