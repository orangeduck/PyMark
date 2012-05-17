#ifndef PyMark_h
#define PyMark_h

typedef unsigned char PyMarkType;

static PyMarkType PyMarkIntType     = 1
static PyMarkType PyMarkLongType    = 2
static PyMarkType PyMarkFloatType   = 3
static PyMarkType PyMarkDoubleType  = 4
static PyMarkType PyMarkNoneType    = 5
static PyMarkType PyMarkStringType  = 6
static PyMarkType PyMarkTupleType   = 7
static PyMarkType PyMarkListType    = 8
static PyMarkType PyMarkDictType    = 9 

typedef struct {
  PyMarkObject** items;
  long long size;
} PyMarkTuple;

typedef struct {
  PyMarkObject** items;
  long long size;
} PyMarkList;

typedef struct {
  PyMarkObject* (*items)(PyMarkDict* self, char* key);
  PyMarkObject** pairs;
  long long size;
} PyMarkDict;

PyMarkObject* PyMarkDict_Items(PyMarkDict* self, char* key);

typedef union {
  PyMarkType type;
  int as_int;
  long long as_long;
  float as_float;
  double as_double;
  void* as_none;
  char* as_string;
  PyMarkList as_list;
  PyMarkTuple as_tuple;
  PyMarkDict as_dict;
} PyMarkObject;

PyMarkObject* PyMark_Unpack(char* filename);
void PyMark_Pack(char* filename, PyMarkObject* o);
void PyMark_Delete(PyMarkObject* o);

#endif