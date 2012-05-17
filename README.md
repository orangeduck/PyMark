PyMark
======

About
-----

When it comes to object markup, PyMark believes in a powerful frontend and a simple backend. It uses python as a front end and compiles to a binary format for fast serialisation into an application.

Why?
----

Using Python as a front end means syntax is checked at compile time and you have the whole power of a programming language behind your markup task. For a human writing markup this is very useful. Compiling to a simple binary format makes serialisation fast and easy and that it can be mapped to a target language's native types.

Having a focus on the front end has many benefits lacking in other object markup languages:
	
	* Bad syntax in markup wont causing runtime errors.
	* Lists, Tuples, Dictionaries are all first class. Not everything is a tree.
	* Structure manipulation/patching can be done at the front end.
	* Lightweight parser written in less than 200 lines of C.
	* Reads/Writes data extremely fast.
	
	
Basic Usage
-----------

