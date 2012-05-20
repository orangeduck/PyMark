""" My Favourite Pets - Another example """

from pymark.util import enum, module, struct

""" Constants """

Types = enum("Dog", "Horse", "Cat")
Toys = enum("String", "Mouse", "Brush", "Bone", "Ball")

Colors = struct(
    Brown = (94, 83, 51),
    White = (255, 255, 255),
    Ginger = (237, 133, 14),
)

""" Module """

pets = module(
  
  benny = struct(
    type = Types.Dog,
    name = "Benny Boos",
    color = Colors.Brown,
    toys = [Toys.Bone, Toys.Ball]
  ),

  roger = struct(
    type = Types.Horse,
    name = "Roger Horse",
    color = Colors.White,
    toys = [Toys.Brush, Toys.String]
  ),
  
  catherine = struct(
    type = Types.Cat,
    name = "Catherine",
    color = Colors.Ginger, 
    toys = [Toys.String, Toys.Mouse]
  )

)
