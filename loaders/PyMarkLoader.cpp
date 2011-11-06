#include "StdAfx.h"
#include "PyMarkLoader.hpp"

/*

PyMark Loader class.

So there are a couple of things to note about the C++ implementation. Namely some of the limitations.

	1. No Load() function or ModuleNames list.
		
		The only reason for this is that there isn't a standard way in C++ to list directory contents (although boost is becoming standard enough).
		So I decided not to implement it one way or the other. I'll let the user do this with whatever filesystem library they are using.
		There is just a LoadModules() function which takes a list of strings. And this should work fine.

	2. No BuildReferences().
		
		Because in this implementation we're throwing around void* - there isn't a way to tell if this is a List or a Dict or what.
		So it isn't possible to traverse recurrsively looking for references.
		Instead references are stored in their string form, and it's up to the user to use the Get() function on these when its needed.

	3. Dictionaries keys are strings only.
		
		Again, because we can't get the type from a void*, the only way to know how to look up a reference is if the current key in the chain is an "int" or a "string".
		Also C++ doesn't supply the generalized mapping of any object as in some other languages.

Other than that it should be your implementation as standard.
There are a couple of "System" objects which I'll try to remove in time and replace with only std stuff.

*/

/* Constructors and Destructors */

PyMarkLoader::PyMarkLoader(string _path)
{
	path = new string(_path);
	modules = new Dict;

	ClearLog();

	LogMsg("PyMarkLoader constructed");
}

PyMarkLoader::~PyMarkLoader()
{
	delete path;
	delete modules;
}

/* Getters and Setters */

Dict* PyMarkLoader::GetModules()
{
	return modules;
}

string* PyMarkLoader::GetPath()
{
	return path;
}

/* Methods */

#define LOGPATH "\\Logs\\Cpp_loader.log"

void PyMarkLoader::LogMsg(string msg)
{
	string logPath = (*path)+LOGPATH;

	ofstream logFile;
	logFile.open(logPath.c_str(),ios::app);
	logFile << msg+"\n";
	logFile.close();
}

void PyMarkLoader::ClearLog(void)
{
	string logPath = (*path)+LOGPATH;

	ofstream logFile;
	logFile.open(logPath.c_str());
	logFile << "";
	logFile.close();
}

void PyMarkLoader::Compile(void)
{
	LogMsg("Compiling all modules...");

	char   psBuffer[128];
	FILE   *pPipe;

	string command =  "python \""+(*path)+"\\PyMark.py\"";

	if( (pPipe = _popen( command.c_str(), "r" )) == NULL )
	  exit( 1 );

	/* Read pipe until end of file. */
	string result = "";

	while( !feof( pPipe ) )
	{
	  if( fgets( psBuffer, 128, pPipe ) != NULL )
		 result += psBuffer;
	}
	
	LogMsg("\n>>>>>");

	LogMsg(result);

	LogMsg(">>>>>\n");
}

void PyMarkLoader::CompileModules(vector<string> names,string flags)
{
	string namesList = "";
	
	for (unsigned int i=0;i<names.size();i++)
	{
		namesList += (names[i] + " ");
	}

	LogMsg("Compiling modules "+namesList);

	char   psBuffer[128];
	FILE   *pPipe;

	string command =  "python \""+(*path)+"\\PyMark.py\" "+namesList+" "+flags;

	if( (pPipe = _popen( command.c_str(), "r" )) == NULL )
	  exit( 1 );

	/* Read pipe until end of file. */
	string result = "";

	while( !feof( pPipe ) )
	{
	  if( fgets( psBuffer, 128, pPipe ) != NULL )
		 result += psBuffer;
	}
	
	LogMsg("\n>>>>>");

	LogMsg(result);

	LogMsg(">>>>>\n");
}

void PyMarkLoader::LoadModules(vector<string> names)
{
	for (unsigned int i=0;i<names.size();i++)
	{
		string* name = new string(names[i]);
		
		LogMsg("Loading Module \""+(*name)+"\"...");
		
		string file_path = (*path)+"\\Compiled\\"+(*name)+".pm";

		ifstream stream;
		stream.open(file_path.c_str(), ios::in | ios::binary);

		modules->operator [](name->c_str()) = BuildObject(&stream);
		
		stream.close();
	}
}

void* PyMarkLoader::BuildObject(ifstream* stream)
{
	short type = ReadShort(stream);

	if (type == NONE)
	{
		return NULL;
	}
	else if ((type == LIST) || (type == TUPLE))
	{
		List* ret = new List(); 
		
		int len = ReadInt(stream);
		for (int i=0;i<len;i++)
		{
			ret->push_back(BuildObject(stream));
		}
		return ret;
	}
	else if ((type == LONG_LIST) || (type == LONG_TUPLE))
	{
		List* ret = new List(); 
		
		long len = ReadLong(stream);
		for (long i=0;i<len;i++)
		{
			ret->push_back(BuildObject(stream));
		}
		return ret;
	}
	else if (type == DICT)
	{
		/* For now lets just assume the hash is a string. We can add an assertion later. Otherwise things just get too complicated in C++ >_< */
		Dict* ret = new Dict();

		int len = ReadInt(stream);
		for (int i=0;i<len;i++)
		{
			short tupleType = ReadShort(stream); // Ignore the type info. We know it is a tuple.
			int tupleLength = ReadInt(stream); // Ignore the length, we know its 2;
			short stringType = ReadShort(stream); // Ingore again, we know its a string.

			string* key = new string(ReadString(stream));
			void* obj = BuildObject(stream);

			ret->operator [](key->c_str()) = obj;
		}

		return ret;
	}
	else if (type == LONG_DICT)
	{
		/* For now lets just assume the hash is a string. We can add an assertion later. Otherwise things just get too complicated in C++ >_< */
		Dict* ret = new Dict();

		long len = ReadInt(stream);
		for (long i=0;i<len;i++)
		{
			short tupleType = ReadShort(stream); // Ignore the type info. We know it is a tuple.
			int tupleLength = ReadInt(stream); // Ignore the length, we know its 2;
			short stringType = ReadShort(stream); // Ingore again, we know its a string.

			string* key = new string(ReadString(stream));
			void* obj = BuildObject(stream);
			ret->operator [](key->c_str()) = obj;
		}

		return ret;
	}
	else if (type == INT)
	{
		int* val = new int(ReadInt(stream));
		return val;
	}
	else if (type == LONG)
	{
		long* val = new long(ReadLong(stream));
		return val;
	}
	else if (type == FLOAT)
	{
		float* val = new float(ReadFloat(stream));
		return val;
	}
	else if (type == DOUBLE)
	{
		double* val = new double(ReadDouble(stream));
		return val;
	}
	else if (type == STRING)
	{
		string* val = new string(ReadString(stream));
		return val;
	}
	else if (type == LONG_STRING)
	{
		string* val = new string(ReadLongString(stream));
		return val;
	}
	else if (type == REFERENCE)
	{
		string* ref = new string("");

		int len = ReadInt(stream);
		for (int i=0;i<len;i++)
		{
			short type = ReadShort(stream);
			if (type == STRING)
			{
				string val = string(ReadString(stream));
				ref->operator +=(val.c_str());
			}
			else if (type == INT)
			{
				int i = ReadInt(stream);
				std::string s;
				std::stringstream out;
				out << i;
				s = out.str();
				ref->operator +=(s.c_str());
			}
			
			if (i!=(len-1))
			{
				ref->operator +=(".");
			}
		}
		return ref;
	}
	else
	{
		throw "ERROR: Unknown type index \""+type.ToString()+"\", perhaps a badly formed .pm file?";
		return NULL;
	}

}


void* PyMarkLoader::Get(string reference)
{
	return Get(reference,modules);
}

void* PyMarkLoader::Get(string reference,void* domain)
{
	List linkList = List();
	string* buffer = new string();
	for (unsigned int i=0;i<reference.length();i++)
	{
		char c = reference[i];
		if (c == '.')
		{
			string* add = new string(*buffer);
			linkList.push_back(add);
			buffer->clear();
		}
		else
		{
			buffer->operator +=(c);
		}
	}
	string* add = new string(*buffer);
	linkList.push_back(add); // String wont end in a . so pushing back the buffer again.

	delete buffer; // aaannndd we shouldn't need this anymore.

	return Get(linkList,domain);
}

void* PyMarkLoader::Get(List linkList,void* domain)
{
	/* Because in C++ we've decided dictionaries can only be referenced with strings. We just test if this is a string or if we should cast to int */
	string* nextKeyPtr = (string*)linkList[0];

	int index = 0;
	bool isList = true;
	
	System::String^ testString = gcnew System::String(nextKeyPtr->c_str());
	try
	{
		index = int::Parse(testString);
	}
	catch (...)
	{
		isList = false;
	}
	delete testString;

	void* nextObject;
	if (isList)
	{
		nextObject = ((List*)domain)->operator [](index);
	}
	else
	{
		nextObject = ((Dict*)domain)->operator [](nextKeyPtr->c_str());
	}
	

	if (linkList.size()-1 == 0) /* Minus 1 because we haven't "popped" it off yet. I.E Shrunk the list. */
	{
		delete linkList[0];		
		return nextObject;
	}
	else
	{
		List newList = List();
		for (unsigned int i=1;i < linkList.size();i++)
		{
			void* item = linkList[i];
			newList.push_back(item);
		}

		delete linkList[0];
		return Get(newList,nextObject);
	}

}

/* Functions for reading bytes in */

short PyMarkLoader::ReadShort(ifstream* stream)
{
	char p1;
	stream->read(&p1,1);

	return (short)p1;
}

int PyMarkLoader::ReadInt(ifstream* stream)
{
	char p1;
	stream->read(&p1,1);
	char p2;
	stream->read(&p2,1);

	int retVal = ((short)p1 << 8) + ((short)p2);
	
	return retVal;
}

long PyMarkLoader::ReadLong(ifstream* stream)
{
	char p1;
	stream->read(&p1,1);
	char p2;
	stream->read(&p2,1);
	char p3;
	stream->read(&p3,1);
	char p4;
	stream->read(&p4,1);

	long retVal = ((short)p1 << 24) + ((short)p2 << 16) + ((short)p3 << 8) + ((short)p4);
	
	return retVal;
}

string PyMarkLoader::ReadString(ifstream *stream)
{
	int len = ReadInt(stream);

	string retString = "";
	for(int i=0;i<len;i++)
	{
		char p1;
		stream->read(&p1,1);
		retString += p1;
	}

	return retString;
}

string PyMarkLoader::ReadLongString(ifstream *stream)
{
	long len = ReadLong(stream);

	string retString = "";
	for(long i=0;i<len;i++)
	{
		char p1;
		stream->read(&p1,1);
		retString += p1;
	}

	return retString;
}

float PyMarkLoader::ReadFloat(ifstream *stream)
{
	char p1;
	stream->read(&p1,1);
	char p2;
	stream->read(&p2,1);
	char p3;
	stream->read(&p3,1);
	char p4;
	stream->read(&p4,1);

	char arr[4] = {p4,p3,p2,p1};
	
	float ret;
	memcpy(&ret,&arr,4);

	return ret;
}

double PyMarkLoader::ReadDouble(ifstream *stream)
{
	char p1;
	stream->read(&p1,1);
	char p2;
	stream->read(&p2,1);
	char p3;
	stream->read(&p3,1);
	char p4;
	stream->read(&p4,1);
	char p5;
	stream->read(&p5,1);
	char p6;
	stream->read(&p6,1);
	char p7;
	stream->read(&p7,1);
	char p8;
	stream->read(&p8,1);


	char arr[8] = {p8,p7,p6,p5,p4,p3,p2,p1};
	
	double ret;
	memcpy(&ret,&arr,8);

	return ret;
}