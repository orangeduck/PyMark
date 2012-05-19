import pymark.unpacker

pets_mod = pymark.unpacker.unpack_file("pets_two.pmk")

print "TypeID: %i" % pets_mod["pets"]["catherine"]["type"]
print "Name: %s" % pets_mod["pets"]["catherine"]["name"]
print "Color: (%i, %i, %i)" % pets_mod["pets"]["catherine"]["color"]
