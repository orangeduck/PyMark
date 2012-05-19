""" Clothing Objects for Game """

from pymark.util import flags, enum, module, properties, modifiers


Avaliable = flags("Merchandise", "Reward", "Bonus", "Secret")
Location = enum("BodyArmor", "Helmets", "Gloves", "Boots")


explorer_jacket = ["Explorer Jacket", "greatcoat_new",  Avaliable.Merchandise | Avaliable.Reward, Location.BodyArmor, 
	                   properties(cost = 214, weight = 5.7, protection = 11), modifiers("old", "ragged", "torn") ],
	                   
chaps 	   	    = ["Chaps", "chaps",  Avaliable.Merchandise | Avaliable.Bonus, Location.Boots, 
	                   properties(cost = 23, weight = 1.1, protection = 2), modifiers("wrapped", "posh", "battered") ],
	                    	
sailor_shirt    = ["Sailor Shirt", "sailor_shirt", Avaliable.Merchandise, Location.BodyArmor, 
	                   properties(cost = 112, weight = 3.1, protection = 4), modifiers("wet") ],
	
pegleg 	        = ["Peg Leg", "peg_leg_m", Avaliable.Secret, Location.Boots, 
	                   properties(cost = 321, weight = 7.2, protection = 4), modifiers("wonky", "new") ]
