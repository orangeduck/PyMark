#include <string.h>
#include <stdlib.h>

#include "PyMark.hpp"

namespace PyMark {

	PyMarkObject::PyMarkObject(std::ifstream& f) {
		
		f.read((char*)&m_type, 1);
		
		int64_t str_len;
		
		switch(m_type) {
			case PyMarkIntType: f.read((char*)&m_data.m_int, 4); break;
			case PyMarkLongType: f.read((char*)&m_data.m_long, 8); break;
			case PyMarkFloatType: f.read((char*)&m_data.m_float, 4); break;
			case PyMarkDoubleType: f.read((char*)&m_data.m_double, 8); break;
			case PyMarkBoolType: f.read((char*)&m_data.m_bool, 1); break;
			case PyMarkNoneType: m_data.m_none = 0; break;
			
			case PyMarkStringType:
				f.read((char*)&str_len, 8);
				m_data.m_string = (char*)malloc(str_len + 1);
				f.read((char*)m_data.m_string, str_len);
				m_data.m_string[str_len] = '\0';
			break;
			
			case PyMarkTupleType:
			case PyMarkListType:
			case PyMarkDictType:
				f.read((char*)&m_data.m_collection.m_length, 8);
				m_data.m_collection.m_items = (PyMarkObject**)malloc(sizeof(PyMarkObject*) * m_data.m_collection.m_length);
				for(int64_t i = 0; i < m_data.m_collection.m_length; i++) {
					m_data.m_collection.m_items[i] = new PyMarkObject(f);
				}
			break;
		}
		
	}

	PyMarkObject::~PyMarkObject() {
		
		if (Type() == PyMarkStringType) {
			free(m_data.m_string);
		}
		
		if (IsCollection()) {
			for(int64_t i = 0; i < Length(); i++) {
				delete At(i);
			}
			free(m_data.m_collection.m_items);
		}

	}
		
	bool PyMarkObject::IsCollection() {
		if ((Type() == PyMarkTupleType) || 
			(Type() == PyMarkListType) ||
			(Type() == PyMarkDictType)) {
			return true;
		} else {
			return false;
		}
	}
		
	PyMarkType PyMarkObject::Type() {
		return m_type;
	}
		
	int32_t PyMarkObject::AsInt() {
		return m_data.m_int;
	}

	int32_t PyMarkObject::AsLong() {
		return m_data.m_long;
	}

	float PyMarkObject::AsFloat() {
		return m_data.m_float;
	}

	double PyMarkObject::AsDouble() {
		return m_data.m_double;
	}

	bool PyMarkObject::AsBool() {
		return m_data.m_bool;
	}
	
	void* PyMarkObject::AsNone() {
		return m_data.m_none;
	}

	char* PyMarkObject::AsString() {
		return m_data.m_string;
	}
		
	int64_t PyMarkObject::Length() {
		
		if (!IsCollection()) {
			return -1;
		}

		return m_data.m_collection.m_length;
	}

	PyMarkObject* PyMarkObject::At(int i) {

		if (!IsCollection()) {
			return 0;
		}
		
		if ((i < 0) || (i >= Length())) {
			return 0;
		}
		
		return m_data.m_collection.m_items[i];
	}
	
	PyMarkObject* PyMarkObject::Get(char* key) {
		
		if (Type() != PyMarkDictType) {
			return 0;
		}
		
    if (strlen(key) >= 511) {
      fprintf(stderr, "Error: PyMark dict key too long.\n");
      return 0;
    }
		
    char tokenize[512];
    strcpy(tokenize, key);
    
    char* token = strtok(tokenize, ".");
    char* next = strtok(NULL, ".");
		
		for(int64_t i = 0; i < Length(); i++) {

			PyMarkObject* pair = At(i);

			if ((pair->Type() != PyMarkTupleType) && 
				(pair->Length() != 2)) {
				return 0;
			}

			PyMarkObject* pair_key = pair->At(0);
			PyMarkObject* pair_value = pair->At(1);

			if (pair_key->Type() != PyMarkStringType) {
				return 0;
			}

			if (strcmp(pair_key->AsString(), token) == 0) {
        if (next == NULL) {
          return pair_value; 
        } else {
          return pair_value->Get(key + strlen(token) + 1);
        }
			}
		}

		return 0;
	}

	PyMarkObject* PyMarkObject::Get(const char* key) {
		return Get((char*)key);
	}
	
	PyMarkObject* PyMarkObject::operator[](int i) {
		return At(i);
	}

	PyMarkObject* PyMarkObject::operator[](char* key) {
		return Get(key);
	}
	
	PyMarkObject* PyMarkObject::operator[](const char* key) {
		return Get((char*)key);
	}
	
	PyMarkObject* UnpackObject(std::ifstream& f) {
	  return new PyMarkObject(f);
	}
	
	PyMarkObject* Unpack(const char* filename) {
		
		std::ifstream f;
		f.open(filename, std::ifstream::binary);
		
		char magic[7];
		f.read(magic, 6);
		magic[6] = '\0';
		if (strcmp(magic, "PYMARK") != 0) { return 0; }
		
		char version;
		f.read(&version, 1);
		if (version != 1) { return 0; }
		
		PyMarkObject* o = UnpackObject(f);
		
		f.close();
		
		return o;
	}
	
	void PackObject(std::ofstream& f, PyMarkObject* o) {
		
		PyMarkType type = o->Type();
		f.write((char*)&type, 1);
		
		int64_t str_len;
		
		switch(type) {
			case PyMarkIntType: {
				int32_t data = o->AsInt();
				f.write((char*)&data, 4);
			} break;
			case PyMarkLongType: {
				int64_t data = o->AsLong();
				f.write((char*)&data, 8);
			} break;
			case PyMarkFloatType: {
				float data = o->AsFloat();
				f.write((char*)&data, 4);
			} break;
			case PyMarkDoubleType: {
				double data = o->AsDouble();
				f.write((char*)&data, 4);
			} break;
			case PyMarkBoolType: {
				bool data = o->AsBool();
				f.write((char*)&data, 1);
			} break;
			case PyMarkNoneType: break;
			
			case PyMarkStringType: {
				char* data = o->AsString();
				str_len = strlen(data);
				f.write((char*)&str_len, 8);
				f.write(data, str_len);
			} break;
			
			case PyMarkTupleType:
			case PyMarkListType:
			case PyMarkDictType: {
				int64_t length = o->Length();
				f.write((char*)&length, 8);
				for(int64_t i = 0; i < length; i++) {
					PackObject(f, o->At(i));
				}
			} break;
		}
		
	}
	
	void Pack(const char* filename, PyMarkObject* o) {
		
		std::ofstream f;
		f.open(filename, std::ofstream::binary);
		
		f.write("PYMARK", 6);
		char version = 1;
		f.write(&version, 1);
		
		PackObject(f, o);
		
		f.close();
	}
	
}
