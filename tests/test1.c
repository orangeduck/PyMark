#include <stdio.h>

#include "../pymark/parsers/PyMark.h"

int main(int argc, char** argv) {
  
  PyMarkObject* pets_two = PyMark_Unpack("pets_two.pmk");
  
  printf("TypeID: %i\n", pets_two->get(pets_two, "pets.catherine.type")->as_int);
  printf("Name: %s\n", pets_two->get(pets_two, "pets.catherine.name")->as_string);
  
  PyMarkObject* color = pets_two->get(pets_two, "pets.catherine.color");
  printf("Color: (%i, %i, %i)\n", color->items[0]->as_int, 
                                  color->items[1]->as_int, 
                                  color->items[2]->as_int);
  
  PyMark_Delete(pets_two);
  
  return 0;
}
