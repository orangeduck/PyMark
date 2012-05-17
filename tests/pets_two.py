""" My Favourite Pets - Another example """

from pymark.util import enum, module

""" Functions """

def pet(**kwargs): return kwargs
def color(r, g, b): return (r, g, b)

""" Constants """

Dog, Horse, Cat = enum(3)
String, Mouse, Brush, Bone, Ball = enum(5)

Brown = color(94, 83, 51)
White = color(255, 255, 255)
Ginger = color(237, 133, 14)

""" Module """

pets_two = module(
  
  benny = pet(
    type = Dog,
    name = "Benny Boos",
    color = Brown,
    toys = [Bone, Ball]
  ),

  roger = pet(
    type = Horse,
    name = "Roger Horse",
    color = White,
    toys = [Brush, String]
  ),
  
  catherine = pet(
    type = Cat,
    name = "Catherine",
    color = Ginger, 
    toys = [String, Mouse]
  )

)
