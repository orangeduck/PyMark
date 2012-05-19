#include <stdio.h>

#include "../parsers/PyMark.h"

int main(int argc, char** argv) {
  
  PyMarkObject* pets_mod = PyMark_Unpack("pets_two.pmk");
  PyMarkObject* pets = pets_mod->get(pets_mod, "pets");
  
  PyMarkObject* cath = pets->get(pets, "catherine");
  PyMarkObject* cath_color = cath->get(cath, "color");
  
  printf("TypeID: %i\n", cath->get(cath, "type")->as_int);
  printf("Name: %s\n", cath->get(cath, "name")->as_string);
  printf("Color: (%i, %i, %i)\n", cath_color->items[0]->as_int, 
                                cath_color->items[1]->as_int, 
                                cath_color->items[2]->as_int);
  
  PyMark_Delete(pets_mod);
  
  return 0;
}
