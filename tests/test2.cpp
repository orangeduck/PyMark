#include <stdio.h>

#include "../parsers/PyMark.hpp"

int main(int argc, char** argv) {
  
  PyMark::PyMarkObject* pets = PyMark::Unpack("pets_two.pmk");
  PyMark::PyMarkObject* cath = pets->Get("catherine");
  
  printf("Test2\n");
  printf("-----\n");
  printf("TypeID: %i\n", cath->Get("type")->AsInt());
  printf("Name: %s\n", cath->Get("name")->AsString());
  printf("Color: (%i, %i, %i)\n", cath->Get("color")->At(0)->AsInt(), 
                                  cath->Get("color")->At(1)->AsInt(), 
                                  cath->Get("color")->At(2)->AsInt());
  
  delete pets;
  
  return 0;
}
