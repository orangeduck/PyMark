""" Clothing Objects for Game """

from pymark import flags, enum, module, properties, modifiers

Avaliable = flags("Merchandise", "Reward", "Bonus", "Secret")
Location = enum("BodyArmor", "Helmets", "Gloves", "Boots")

jacket = ["Explorer Jacket", "greatcoat_new",
          Avaliable.Merchandise | Avaliable.Reward, Location.BodyArmor, 
	      properties(cost = 214, weight = 5.7, protection = 11, full_body = True), 
          modifiers("Old", "Ragged", "Torn")]

chaps  = ["Chaps", "chaps",
          Avaliable.Merchandise | Avaliable.Bonus, Location.Boots, 
	      properties(cost = 23, weight = 1.1, protection = 2, full_body = False),
          modifiers("Wrapped", "Posh", "Battered")]

shirt  = ["Sailor Shirt", "sailor_shirt",
          Avaliable.Merchandise, Location.BodyArmor, 
	      properties(cost = 112, weight = 3.1, protection = 4, full_body = False),
          modifiers("Wet")]
	
pegleg = ["Peg Leg", "peg_leg_m",
          Avaliable.Secret, Location.Boots, 
	      properties(cost = 321, weight = 7.2, protection = 4, full_body = False),
          modifiers("Wonky", "New")]