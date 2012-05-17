#include <stdio.h>

#include "../parsers/PyMark.h"

int main(int argc, char** argv) {
  
  PyMarkObject* clothing = PyMark_Unpack("clothing.pmk");
  PyMarkObject* pegleg_prop = clothing->get(clothing, "pegleg")->items[4];
  
  printf("Test0\n");
  printf("-----\n");
  printf("Pegleg cost: %i\n", pegleg_prop->get(pegleg_prop, "cost")->as_int);
  printf("Pegleg protection: %f\n", pegleg_prop->get(pegleg_prop, "weight")->as_float);
  printf("\n");
  
  PyMark_Delete(clothing);
  
  return 0;
}
