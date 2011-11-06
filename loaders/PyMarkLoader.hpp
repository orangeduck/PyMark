#pragma once
#include <string>
#include <map>
#include <vector>
#include <queue>
#include <list>
#include <fstream>
#include <iostream>
#include <sstream>
#include <cctype>
#include <intrin.h>

using namespace stdext;
using namespace std;

struct ltstr
{
  bool operator()(const char* s1, const char* s2) const
  {
    return strcmp(s1, s2) < 0;
  }
};

typedef map<const char*,void*,ltstr> Dict;
typedef vector<void*> List;

ref class PyMarkLoader
{
public:
	/* Constructors and Destructors */
	PyMarkLoader(string);
	~PyMarkLoader(void);

	/* Getters and Setters */
	string* GetPath();
	Dict* GetModules();

	/* Methods */
	void Compile(void);
	void CompileModules(vector<string>,string);
	void LoadModules(vector<string>);
	
	void* Get(string);
	void* Get(string, void*);
	void* Get(List, void*);
	
	/* Constants */
    const static short LIST 		= 1;
    const static short LONG_LIST    = 2;
    const static short DICT         = 3;
    const static short LONG_DICT    = 4;
    const static short TUPLE        = 5;
    const static short LONG_TUPLE   = 6;
    const static short STRING       = 7;
    const static short LONG_STRING  = 8;
    const static short INT          = 9;
    const static short LONG         = 10;
    const static short FLOAT        = 11;
    const static short DOUBLE       = 12;
    const static short REFERENCE    = 13;
    const static short NONE         = 14;
	
private:
	/* Properties */
	string* path;
	Dict* modules;

	/* Methods */

	void LogMsg(string);
	void ClearLog(void);

	void* BuildObject(ifstream* stream);

	/* methods for reading bytes */

	short ReadShort(ifstream* stream);
	int ReadInt(ifstream* stream);
	long ReadLong(ifstream* stream);
	string ReadString(ifstream* stream);
	string ReadLongString(ifstream* stream);
	float ReadFloat(ifstream* stream);
	double ReadDouble(ifstream* stream);
};