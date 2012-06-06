require "struct"
package.path = package.path .. ";../parsers/PyMark.lua"
require "PyMark"

pets_two = pymark_unpack("pets_two.pmk")

print(string.format("TypeID: %d", pets_two.pets.catherine.type))
print(string.format("Name: %s", pets_two.pets.catherine.name))

color = pets_two.pets.catherine.color
print(string.format("Color: (%d, %d, %d)", color[1], color[2], color[3]))