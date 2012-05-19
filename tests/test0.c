#include <stdio.h>

#include "../parsers/PyMark.h"

int main(int argc, char** argv) {
  
  PyMarkObject* clothing = PyMark_Unpack("clothing.pmk");
  PyMarkObject* pegleg = clothing->get(clothing, "pegleg");
  
  printf("Pegleg cost: %i\n", pegleg->items[4]->get(pegleg->items[4], "cost")->as_int);
  printf("Pegleg protection: %f\n", pegleg->items[4]->get(pegleg->items[4], "weight")->as_float);
  
  PyMark_Delete(clothing);
  
  return 0;
}
