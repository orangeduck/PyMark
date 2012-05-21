#ifndef PyMark_h
#define PyMark_h

#include <stdint.h>
#include <stdbool.h>

#define PyMarkIntType     1
#define PyMarkLongType    2
#define PyMarkFloatType   3
#define PyMarkDoubleType  4
#define PyMarkBoolType    5
#define PyMarkNoneType    6
#define PyMarkStringType  7
#define PyMarkTupleType   8
#define PyMarkListType    9
#define PyMarkDictType    10

typedef char PyMarkType;

typedef struct PyMarkObject {
  
  PyMarkType type;
  
  union {
  
    /* Basic Types */
    int32_t as_int;
    int64_t as_long;
    float as_float;
    double as_double;
    bool as_bool;
    void* as_none;
    char* as_string;
    
    /* Collection Type */
    struct {
      int64_t length;
      struct PyMarkObject** items;
      struct PyMarkObject* (*at)(struct PyMarkObject* self, int64_t index);
      struct PyMarkObject* (*get)(struct PyMarkObject* self, char* key);
    };
    
  };

} PyMarkObject;

PyMarkObject* PyMark_Unpack(char* filename);
void PyMark_Pack(char* filename, PyMarkObject* o);

PyMarkObject* PyMark_UnPackObject(FILE* f);
void PyMark_PackObject(FILE* f, PyMarkObject* o);

void PyMark_Delete(PyMarkObject* o);

#endif
