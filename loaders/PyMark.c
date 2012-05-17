#include "PyMark.h"

static PyMarkObject* PyMark_UnPackObject(FILE* f) {
  
  PyMarkObject* out = malloc(sizeof(PyMarkObject));
  fread(&out.type, 1, 1, f);
  
  switch(out.type) {
    
    case PyMarkIntType: fread(&out.as_int, 4, 1, f); break;
    case PyMarkLongType: fread(&out.as_long, 8, 1, f); break;
    case PyMarkFloatType: fread(&out.as_float, 4, 1, f); break;
    case PyMarkDoubleType: fread(&out.as_double, 8, 1, f); break;
    case PyMarkNoneType: out.as_none = NULL; break;
    
    case PyMarkStringType:
      long long len;
      fread(&len, 8, 1, f);
      out.as_string = malloc(sizeof(len) + 1);
      fread(out.as_string, len, 1, f);
      out.as_string[len] = '\0'
    break;
      
    case PyMarkTupleType:
      fread(out.as_tuple.size, 8, 1, f);
      out.as_tuple.items = malloc(sizeof(PyMarkObject*) * out.as_tuple.size);
      for (int i = 0; i < out.as_tuple.size; i++) {
        out.as_tuple.items[i] = PyMark_UnPackObject(f);
      }
    break;
      
    case PyMarkListType:
      fread(out.as_list.size, 8, 1, f);
      out.as_list.items = malloc(sizeof(PyMarkObject*) * out.as_list.size);
      for (int i = 0; i < out.as_list.size; i++) {
        out.as_list.items[i] = PyMark_UnPackObject(f);
      }
    break;
      
    case PyMarkDictType:
      fread(out.as_dict.size, 8, 1, f);
      out.as_dict.pairs = malloc(sizeof(PyMarkObject*) * out.as_dict.size);
      for (int i = 0; i < out.as_dict.size; i++) {
        out.as_dict.pairs[i] = PyMark_UnPackObject(f);
      }
      out.as_dict.items = PyMarkDict_Items;
    break;
      
    default: return NULL;
  }
  
  return out;
  
}

PyMarkObject* PyMarkDict_Items(PyMarkDict* self, char* key) {
  
  for(int i = 0; i < self.size; i++) {
    PyMarkObject* pair = self.pairs[i];
    if ((pair.type != PyMarkTupleType) && 
        (pair.as_tuple.size != 2))
      return NULL;
    }
    
    PyMarkObject* pair_key = pair.as_tuple.items[0];
    PyMarkObject* pair_value = pair.as_tuple.items[1];
    
    if (pair_key.type != PyMarkStringType) {
      return NULL;
    }
    
    if (strcmp(pair_key.as_string, key) == 0) {
      return pair_value;
    }
  }
  
  return NULL;
}

PyMarkObject* PyMark_Unpack(char* filename) {
  
  FILE* f = fopen(filename, 'rb');
  char magic[7];
  fread(magic, 6, 1, f);
  magic[6] = '\0'
  if (strcmp(magic, "PYMARK") != 0) { return NULL; }
  
  PyMarkObject* o = PyMark_UnPackObject(f);
  
  fclose(f);
  
  return o;
  
}

static void PyMark_PackObject(FILE* f, PyMarkObject* o) {

}

void PyMark_Pack(char* filename, PyMarkObject* o) {
  
  
  
}

void PyMark_Delete(PyMarkObject* o) {
  
  switch(o.type) {
    case PyMarkIntType: free(o); break;
    case PyMarkLongType: free(o); break;
    case PyMarkFloatType: free(o); break;
    case PyMarkDoubleType: free(o); break;
    case PyMarkNoneType: free(o); break;
    
    case PyMarkStringType:
      free(o.as_string);
      free(o);
    break;
      
    case PyMarkTupleType:
      for(int i = 0; i < o.as_tuple.size; i++) {
        PyMark_Delete(o.as_tuple.items[i]);
      }
      free(o);
    break;
      
    case PyMarkListType:
      for(int i = 0; i < o.as_list.size; i++) {
        PyMark_Delete(o.as_list.items[i]);
      }
      free(o);
    break;
      
    case PyMarkDictType:
      for(int i = 0; i < o.as_dict.size; i++) {
        PyMark_Delete(o.as_dict.pairs[i]);
      }
      free(o);
    break;
    
  }
  
}
