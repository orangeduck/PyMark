#include <stdio.h>

#include "../parsers/PyMark.hpp"

int main(int argc, char** argv) {
  
  PyMark::PyMarkObject* pets_mod = PyMark::Unpack("pets_two.pmk");
  PyMark::PyMarkObject* cath = pets_mod->Get("pets")->Get("catherine");
  
  printf("TypeID: %i\n", cath->Get("type")->AsInt());
  printf("Name: %s\n", cath->Get("name")->AsString());
  printf("Color: (%i, %i, %i)\n", cath->Get("color")->At(0)->AsInt(), 
                                  cath->Get("color")->At(1)->AsInt(), 
                                  cath->Get("color")->At(2)->AsInt());
  
  delete pets_mod;
  
  return 0;
}
