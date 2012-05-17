PyMark
======

About
-----

PyMark provides a powerful Python frontend and a simple binary backend. It uses Python as a front end and compiles to a binary format for fast serialisation into an application.


Advantages
----------

Using Python as a front end means syntax is checked at compile time and you have the whole power of a programming language behind your markup task. For human written markup this is very useful. Compiling to a simple binary format makes serialisation fast and easy and can be mapped to a target language in a few lines of code.

Having a focus on a powerful front end has many benefits lacking in other object markup techniques:
	
* Bad syntax in markup is caught at compile time.
* Lists, Tuples, Dictionaries are all first class structures.
* Not everything has to be a tree of strings.
* More expression and freedom using better syntax.
* Structure manipulation/patching can be done easily and early.
* Lightweight parser written in less than 200 lines of C.
* Reads/Writes/Streams data quickly.
* If required, obfuscation is possible.

	
Disadvantages
-------------

Having so much happen in the front end makes the system somewhat one-directional.

While the human readable source can be reconstructed in some sense, data such as comments and other markup is lost in the compilation. For distribution and collaboration it is important to also share the source files.


Usage 
-----

First write a python module with an object the same name as the file. You can do this how you please. If you are a JSON fan you might write something like this:

```python
""" My Favourite Pets - A basic example """

pets_one = {

  "benny" : {
    "type"  : "Dog",
    "name"  : "Benny Boos",
    "color" : "Brown",
    "toys"  : ["Bone", "Ball"]
  },
  
  "roger" : {
    "type"  : "Horse",
    "name"  : "Roger Horse",
    "color" : "White",
    "toys"  : ["Brush", "String"]
  },

  "catherine" : {
    "type"  : "Cat",
    "name"  : "Catherine",
    "color" : "Ginger",
    "toys"  : ["String", "Mouse"]
  }

}
```

But having Python allows you to be much more expressive if you wish. You can adjust the data entry in many different ways to make it simpler, more explicit, or more aesthetic.

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

I have no real preference for either but in using Python it allows you to adapt your markup depending on your preference or domain.

Once you have the module written just feed it into pymark.

```bash
pymark pets_two.py > pets_good.pmk
```

Loading data at runtime and making it easy to access in a typesafe language is always going to be horrible. It is one of the major issues with doing object markup in a separate language and there is little way around it. Saying this I've tried to do my best to make the APIs fairly simplistic and clear. In C you can do something like this.

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

The C++ syntax is a little more sane though the implementation not much cleaner.

```

#include <stdio.h>

#include "PyMark.hpp"

int main(int argc, char** argv) {
  
  PyMark::PyMarkObject* pets = PyMark::Unpack("pets_two.pmk");
  PyMark::PyMarkObject* cath = pets->Get("catherine");
  
  printf("Test2\n");
  printf("-----\n");
  printf("TypeID: %i\n", cath->Get("type")->AsInt());
  printf("Name: %s\n", cath->Get("name")->AsString());
  printf("Color: (%i, %i, %i)\n", cath->Get("color")->At(0)->AsInt(), 
                                  cath->Get("color")->At(1)->AsInt(), 
                                  cath->Get("color")->At(2)->AsInt());
  
  delete pets;
  
  return 0;
}

```

Hopefully more languages supported soon.

