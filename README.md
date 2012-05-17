PyMark
======

About
-----

When it comes to object markup, PyMark believes in a powerful frontend and a simple backend. It uses python as a front end and compiles to a binary format for fast serialisation into an application.


Advantages
----------

Using Python as a front end means syntax is checked at compile time and you have the whole power of a programming language behind your markup task. For a human writing markup this is very useful. Compiling to a simple binary format makes serialisation fast and easy and that it can be mapped to a target language's native types.

Having a focus on the front end has many benefits lacking in other object markup languages:
	
	* Bad syntax in markup caught at compile time.
	* Lists, Tuples, Dictionaries are all first class objects.
	* Not everything is a tree of strings.
	* More expression and freedom with less syntax.
	* Structure manipulation/patching can be done at the front end easily.
	* Lightweight parser written in less than 200 lines of C.
	* Reads/Writes data extremely fast.
	* If required, obfuscation is easy.
	
	
Disadvantages
-------------

The system is somewhat one way. While the human readable source can be reconstructed in some sense, data such as comments and other markup is lost in the compilation. For distribution and collaboration it is important to also share the source files.


The Front End
-------------

First write a python module with an object the same name as the file. You can do this how you please. If you are a JSON fan you might write something like this:

```python
""" My Favourite Pets - A basic example """

pets_one = {

  "benny" : {
    "type"  : "Dog",
    "name"  : "Benny Boos",
    "color" : "Brown",
    "toys"  : { "0" : "Bone", "1" : "Ball" }
  },
  
  "roger" : {
    "type"  : "Horse",
    "name"  : "Roger Horse",
    "color" : "White",
    "toys"  : { "0" : "Brush", "1" : "String" }
  },

  "catherine" : {
    "type"  : "Cat",
    "name"  : "Catherine",
    "color" : "Ginger",
    "toys"  : { "0" : "String", "1" : "Mouse" }
  }

}
```

But having Python allows you to be much more expressive if you want.

```python
""" My Favourite Pets - Another example """

from pymark.util import enum, module

""" Functions """

def pet(**kwargs): return kwargs
def color(r, g, b): return (r, g, b)

""" Constants """

Dog, Horse, Cat = enum(3)
String, Mouse, Brush, Bone, Ball = enum(5)

Brown = color(94, 83, 51)
White = color(255, 255, 255)
Ginger = color(237, 133, 14)

""" Module """

pets_two = module(
  
  benny = pet(
    type = Dog,
    name = "Benny Boos",
    color = Brown,
    toys = [Bone, Ball]
  ),

  roger = pet(
    type = Horse,
    name = "Roger Horse",
    color = White,
    toys = [Brush, String]
  ),
  
  catherine = pet(
    type = Cat,
    name = "Catherine",
    color = Ginger, 
    toys = [String, Mouse]
  )

)
```

The choice is up to you and I don't really have a dogma one way or the other. The nice thing about using Python is that it allows you to adapt your markup depending on your preference or domain. Once you have this file just feed it into pymark.

```bash
pymark pets_two.py
```

This will produce a file ```pets_good.pmk```.

Loading runtime data at runtime and making it easy to access in a typesafe language is always horrible. Saying this I've tried to do my best to make the APIs fairly simplistic and clear. In C you can do something like this.

```
#include <stdio.h>

#include "PyMark.h"

int main(int argc, char** argv) {
  
  PyMarkObject* pets = PyMark_Unpack("pets_two.pmk");
  PyMarkObject* cath = pets->get(pets, "catherine");
  
  PyMarkObject* cath_color = cath->get(cath, "color");
  PyMarkObject* cath_toys = cath->get(cath, "toys");
  
  printf("TypeID: %i\n", cath->get(cath, "type")->as_int);
  printf("Name: %s\n", cath->get(cath, "name")->as_string);
  printf("Color: (%i, %i, %i)", cath_color->items[0].as_int, 
                                cath_color->items[1].as_int, 
                                cath_color->items[2].as_int);
  
  printf("ToyIDs: ");
  for(int i = 0; i < cath_toys->length; i++) {
    printf("%i, ", cath_toys->items[i]->as_int);
  }
  printf("\n");
  
  PyMark_Delete(pets);
  
  return 0;
}
```

And hopefully it should output:

```
TypeID: 4
Name: Catherine
Color: (237, 133, 14)
ToyIDs: 1, 2, 
```



