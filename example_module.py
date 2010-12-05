from PyMark.Util import *

awesome, red, dog_shaped = Flags(3)

OVERCAST, SUNNY, RAINY = Enum(3)

example_module = {
	"first_entry":(
		"Some propery",
		"Another property",
		"A third property",
		awesome|red,
		OVERCAST,
		None
		),
		
	"second_entry":(
		"Boobs",
		"are",
		"booby",
		dog_shaped,
		RAINY,
		Ref("example_module.first_entry.0")
		),
	
	"third_entry":(
		"This is some ascii",
		"Ohter String",
		"Blahhh",
		red|dog_shaped|awesome,
		15.25,
		Ref("example_module.second_entry")
		),
}
