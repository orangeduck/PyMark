from Util import *

awesome, red, dog_shaped = Flags(3)

RED, BLUE, GREEN = Enum(3)

tests = {
	"first entry":(
		"Material1",
		"Material2",
		"Material3",
		awesome|red,
		RED,
		R("examples.example1")
		),
		
	"second entry":(
		"Boobs",
		"are",
		"booby",
		dog_shaped,
		60,
		R("examples.example1")
		),
	
	"third entry":(
		"This is some ascii",
		"Ohter String",
		"Blahhh",
		red|dog_shaped|awesome,
		GREEN,
		R("examples.example1")
		),
}
