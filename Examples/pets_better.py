from PyMark.Util import *

# The "animal" field isn't really looking for a String - it's looking for a type. So we can use this Enum instead. Much better.
Dog, Cat, Elephant, Sparrow = Enum(4)

# Lots of the personality traits are shared, perhaps we can use Flags instead! Makes a lot more sense than a list of Strings.
Cute, Funny, Friendly, Vain, Speedy = Flags(5)

# It'd be nicer to represent color as a tuple rather than a string, we can do it with this quick function definition.
# This adds more expressive power, and we can even ensure that the outputs are floats.
def Color(r,g,b):
	return (float(r),float(g),float(b))

# We can define some constants to help us with the colors. That way we can reuse them.
BROWN = Color(156,137,61)
GINGER = Color(247,172,32)
GREY = Color(128,128,128)

# If you're worried about detecting these flags, enums or constants afterwards don't be. All constants are compiled to a special "constants" module, so it should be no problem!

# Finally lets consider the "toys" field. If in fact we consider a toy as another object and if we have toys module defined, then we can use the reference function to express this link!

# Overall I think this is much nicer. We've reduced the instances of Strings to just the parts which actually are strings, and dramatically increased the expressiveness of the data!
# Also without all those strings I think it is much easier to read.
# I'm not saying that all of these things are the "correct" way to structure the data.
# I believe you should structure your data to best suite the task in hand, not by some set of global rules.
# Having extra constructs just allows for that a little more easily :)

pets = [

	{"name":	"John",
	"animal":	Dog,
	"legs":		4,
	"age":		10,
	"toys":		[Ref("toys.squeezy"),
				 Ref("toys.bone")],
	"traits":	Cute|Funny|Friendly
	"color":	BROWN},
	
	{"name":	"Benni",
	"animal":	Cat,
	"legs":		4,
	"age":		8,
	"toys":		[Ref("toys.mouse_ball"),
				 Ref("toys.string")],
	"traits":	Cute|Vain
	"color":	GINGER},
	
	{"name":	"Leeroy",
	"animal":	Elephant,
	"legs":		4.5,
	"age":		102,
	"toys":		[Ref("toys.peanuts")],
	"traits":	Friendly
	"color":	GREY},
	
	{"name":	"Tophat",
	"animal":	Sparrow,
	"legs":		2,
	"age":		1,
	"toys":		None,
	"traits":	Vain|Speedy,
	"color":	BROWN},

]