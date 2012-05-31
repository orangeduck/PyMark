#include <stdio.h>

#include "../parsers/PyMark.hpp"

int main(int argc, char** argv) {
  
  PyMark::PyMarkObject* pets_two = PyMark::Unpack("pets_two.pmk");
  
  printf("TypeID: %i\n", pets_two->Get("pets.catherine.type")->AsInt());
  printf("Name: %s\n", pets_two->Get("pets.catherine.name")->AsString());
  
  PyMark::PyMarkObject* color = pets_two->Get("pets.catherine.color");
  printf("Color: (%i, %i, %i)\n", color->At(0)->AsInt(), 
                                  color->At(1)->AsInt(), 
                                  color->At(2)->AsInt());
  
  delete pets_two;
  
  return 0;
}
