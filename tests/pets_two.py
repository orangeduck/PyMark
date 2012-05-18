""" My Favourite Pets - Another example """

from pymark.util import enum, module, struct

""" Functions """

def pet(**kwargs): return kwargs
def color(r, g, b): return (r, g, b)

""" Constants """

Types = enum("Dog", "Horse", "Cat")
Toys = enum("String", "Mouse", "Brush", "Bone", "Ball")

Colors = struct(
    Brown = color(94, 83, 51),
    White = color(255, 255, 255),
    Ginger = color(237, 133, 14),
)

""" Module """

pets_two = module(
  
  benny = pet(
    type = Types.Dog,
    name = "Benny Boos",
    color = Colors.Brown,
    toys = [Toys.Bone, Toys.Ball]
  ),

  roger = pet(
    type = Types.Horse,
    name = "Roger Horse",
    color = Colors.White,
    toys = [Toys.Brush, Toys.String]
  ),
  
  catherine = pet(
    type = Types.Cat,
    name = "Catherine",
    color = Colors.Ginger, 
    toys = [Toys.String, Toys.Mouse]
  )

)
