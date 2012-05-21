#ifndef PyMark_h
#define PyMark_h

#include <stdint.h>

#include <iostream>
#include <fstream>
#include <string>

namespace PyMark {
	
	typedef char PyMarkType;
	
	const PyMarkType PyMarkIntType    = 1;
	const PyMarkType PyMarkLongType   = 2;
	const PyMarkType PyMarkFloatType  = 3;
	const PyMarkType PyMarkDoubleType = 4;
	const PyMarkType PyMarkBoolType   = 5;
	const PyMarkType PyMarkNoneType   = 6;
	const PyMarkType PyMarkStringType = 7;
	const PyMarkType PyMarkTupleType  = 8;
	const PyMarkType PyMarkListType   = 9;
	const PyMarkType PyMarkDictType   = 10;

	class PyMarkObject {
		
		private:

		PyMarkType m_type;
		
		union {
			/* Basic Types */
			int32_t m_int;
			int64_t m_long;
			float m_float;
			double m_double;
			bool m_bool;
			void* m_none;
			char* m_string;
			
			/* Collection Type */
			struct {
			  int64_t m_length;
			  PyMarkObject** m_items;
			} m_collection;
			
		} m_data;
		
		public:
		
		PyMarkObject(std::ifstream& f);
		~PyMarkObject();
		
		PyMarkType Type();
		
		int32_t AsInt();
		int32_t AsLong();
		float AsFloat();
		double AsDouble();
		bool AsBool();
		void* AsNone();
		char* AsString();
		
		bool IsCollection();
		int64_t Length();
		
		PyMarkObject* At(int i);
		PyMarkObject* Get(char* key);
		PyMarkObject* Get(const char* key);
		
		PyMarkObject* operator[](int i);
		PyMarkObject* operator[](char* key);
		PyMarkObject* operator[](const char* key);
		
	};
  
	PyMarkObject* Unpack(const char* filename);
	void Pack(const char* filename, PyMarkObject* o);

  PyMarkObject* UnpackObject(std::ifstream& f);
  void PackObject(std::ofstream& f, PyMarkObject* o);

};

#endif
