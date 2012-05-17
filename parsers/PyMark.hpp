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
	const PyMarkType PyMarkNoneType   = 5;
	const PyMarkType PyMarkStringType = 6;
	const PyMarkType PyMarkTupleType  = 7;
	const PyMarkType PyMarkListType   = 8;
	const PyMarkType PyMarkDictType   = 9;

	class PyMarkObject {
		
		private:

		PyMarkType m_type;
		
		union {
			/* Basic Types */
			int32_t m_int;
			int64_t m_long;
			float m_float;
			double m_double;
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

};

#endif