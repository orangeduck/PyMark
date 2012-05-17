#ifndef PyMark_h
#define PyMark_h

#include <stdint.h>

#define PyMarkIntType     1
#define PyMarkLongType    2
#define PyMarkFloatType   3
#define PyMarkDoubleType  4
#define PyMarkNoneType    5
#define PyMarkStringType  6
#define PyMarkTupleType   7
#define PyMarkListType    8
#define PyMarkDictType    9

typedef struct PyMarkObject {
  
  char type;
  
  union {
  
    /* Basic Types */
    int32_t as_int;
    int64_t as_long;
    float as_float;
    double as_double;
    void* as_none;
    char* as_string;
    
    /* Collection Type */
    struct {
      int64_t length;
      struct PyMarkObject** items;
      struct PyMarkObject* (*at)(struct PyMarkObject* self, int index);
      struct PyMarkObject* (*get)(struct PyMarkObject* self, char* key);
    };
  };

} PyMarkObject;

PyMarkObject* PyMark_Unpack(char* filename);
void PyMark_Pack(char* filename, PyMarkObject* o);

void PyMark_Delete(PyMarkObject* o);

#endif
