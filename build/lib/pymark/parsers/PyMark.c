#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "PyMark.h"

static PyMarkObject* PyMarkList_At(PyMarkObject* self, int64_t i) {
  
  if ((self->type != PyMarkListType) || 
      (self->type != PyMarkTupleType) || 
      (self->type != PyMarkDictType)) {
    return NULL;
  }  
  
  if ((i < 0) || (i >= self->length)) {
    return NULL;
  }
  
  return self->items[i];
  
}

static PyMarkObject* PyMarkDict_Get(PyMarkObject* self, char* key) {
  
  if (strlen(key) >= 511) {
    fprintf(stderr, "Error: PyMark dict key too long.\n");
    return NULL;
  }
  
  char tokenize[512];
  strcpy(tokenize, key);
  
  char* token = strtok(tokenize, ".");
  char* next = strtok(NULL, ".");
  
  if (self->type != PyMarkDictType) {
    return NULL;
  }
  
  for(int64_t i = 0; i < self->length; i++) {
    
    PyMarkObject* pair = self->items[i];
    
    if ((pair->type != PyMarkTupleType) && 
        (pair->length != 2)) {
      return NULL;
    }
    
    PyMarkObject* pair_key = pair->items[0];
    PyMarkObject* pair_value = pair->items[1];
    
    if (pair_key->type != PyMarkStringType) {
      return NULL;
    }
    
    if (strcmp(pair_key->as_string, token) == 0) {
      if (next == NULL) {
        return pair_value; 
      } else {
        return PyMarkDict_Get(pair_value, key + strlen(token) + 1);
      }
    }
    
  }
  
  return NULL;
}

PyMarkObject* PyMark_UnPackObject(FILE* f) {
  
  PyMarkObject* out = malloc(sizeof(PyMarkObject));
  if (out == NULL) {
    fprintf(stderr, "Error: PyMark out of memory.\n");
    return NULL;
  }
  
  fread(&out->type, 1, 1, f);
  
  int64_t str_len;
  
  switch(out->type) {
    
    case PyMarkIntType: fread(&out->as_int, 4, 1, f); break;
    case PyMarkLongType: fread(&out->as_long, 8, 1, f); break;
    case PyMarkFloatType: fread(&out->as_float, 4, 1, f); break;
    case PyMarkDoubleType: fread(&out->as_double, 8, 1, f); break;
    case PyMarkBoolType: fread(&out->as_bool, 1, 1, f); break;
    case PyMarkNoneType: out->as_none = NULL; break;
    
    case PyMarkStringType:
      fread(&str_len, 8, 1, f);
      out->as_string = malloc(str_len + 1);
      fread(out->as_string, str_len, 1, f);
      out->as_string[str_len] = '\0';
    break;
      
    case PyMarkTupleType:
    case PyMarkListType:
      fread(&out->length, 8, 1, f);
      out->items = malloc(sizeof(PyMarkObject*) * out->length);
      for (int64_t i = 0; i < out->length; i++) {
        out->items[i] = PyMark_UnPackObject(f);
      }
      out->at = PyMarkList_At;
    break;
      
    case PyMarkDictType:
      fread(&out->length, 8, 1, f);
      out->items = malloc(sizeof(PyMarkObject*) * out->length);
      for (int64_t i = 0; i < out->length; i++) {
        out->items[i] = PyMark_UnPackObject(f);
      }
      out->at = PyMarkList_At;
      out->get = PyMarkDict_Get;
    break;
    
    default:
      fprintf(stderr, "Error: Unknown PyMark Type id %i\n", out->type);
      return NULL;
  }
  
  return out;
  
}

PyMarkObject* PyMark_Unpack(char* filename) {
  
  FILE* f = fopen(filename, "rb");
  if (f == NULL) { return NULL; }
  
  char magic[7];
  fread(magic, 6, 1, f);
  magic[6] = '\0';
  if (strcmp(magic, "PYMARK") != 0) {
    fprintf(stderr, "PyMark Error: Bad Magic number for file '%s'\n", filename);
    return NULL;
  }
  
  unsigned char version;
  fread(&version, 1, 1, f);
  if (version != 1) {
    fprintf(stderr, "PyMark Error: Bad Version number %i for file '%s'\n", version, filename);
    return NULL;
  }
  
  PyMarkObject* o = PyMark_UnPackObject(f);
  
  fclose(f);
  
  return o;
  
}

void PyMark_PackObject(FILE* f, PyMarkObject* o) {
  
  fwrite(&o->type, 1, 1, f);
  
  int64_t str_len;
  
  switch(o->type) {
    case PyMarkIntType: fwrite(&o->as_int, 4, 1, f); break;
    case PyMarkLongType: fwrite(&o->as_long, 8, 1, f); break;
    case PyMarkFloatType: fwrite(&o->as_float, 4, 1, f); break;
    case PyMarkDoubleType: fwrite(&o->as_double, 8, 1, f); break;
    case PyMarkBoolType: fwrite(&o->as_bool, 1, 1, f); break;
    case PyMarkNoneType: break;
    
    case PyMarkStringType:
      str_len = strlen(o->as_string);
      fwrite(&str_len, 8, 1, f);
      fwrite(o->as_string, str_len, 1, f);
    break;
    
    case PyMarkTupleType:
    case PyMarkListType:
    case PyMarkDictType:
      fwrite(&o->length, 8, 1, f);
      for (int64_t i = 0; i < o->length; o++) {
        PyMark_PackObject(f, o->items[i]);
      }
    break;
    
  }
  
}

void PyMark_Pack(char* filename, PyMarkObject* o) {
  
  FILE* f = fopen(filename, "wb");
  fwrite("PYMARK", 6, 1, f);
  
  char version = 1;
  fwrite(&version, 1, 1, f);
  
  PyMark_PackObject(f, o);
  
  fclose(f);
  
}

void PyMark_Delete(PyMarkObject* o) {
  
  switch(o->type) {
  
    case PyMarkIntType: free(o); break;
    case PyMarkLongType: free(o); break;
    case PyMarkFloatType: free(o); break;
    case PyMarkDoubleType: free(o); break;
    case PyMarkBoolType: free(o); break;
    case PyMarkNoneType: free(o); break;
    
    case PyMarkStringType:
      free(o->as_string);
      free(o);
    break;
      
    case PyMarkTupleType:
    case PyMarkListType:
    case PyMarkDictType:
      for(int64_t i = 0; i < o->length; i++) {
        PyMark_Delete(o->items[i]);
      }
      free(o->items);
      free(o);
    break;
    
  }
  
}
