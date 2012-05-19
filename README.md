PyMark
======


About
-----

PyMark is a lightweight and powerful object markup solution which uses Python as a frontend to and compiles data to a simple binary format for use in an application.

Having a focus on a powerful frontend has many benefits missing from other object markup techniques:

* Bad syntax is caught at compile time.
* A whole programming language to help you.
* Lists, Tuples, Dictionaries are all first class structures.
* Structure manipulation/patching can be done easily and early.

And having a simple backend has some benefits too.

* A parser in less than 200 lines of C.
* Reads/Writes/Streams data quickly.


Drawbacks
---------

Having so much happen in the frontend makes the system somewhat one-directional.

While the human readable source can be reconstructed in some sense, data such as comments are lost in the compilation. PyMark is best used for human written object description for use in an application.

Usage
-----

The first task is to actually enter your data. For this you simply create a python module. All native objects at the top level other than the builtins dict will be exported. You can structure this how you please. If you are a JSON fan you might write something like this:

```python
""" My Favourite Pets - A basic example """

benny = {
  "type"  : "Dog",
  "name"  : "Benny Boos",
  "color" : "Brown",
  "toys"  : ["Bone", "Ball"]
}
  
roger = {
  "type"  : "Horse",
  "name"  : "Roger Horse",
  "color" : "White",
  "toys"  : ["Brush", "String"]
}

catherine = {
  "type"  : "Cat",
  "name"  : "Catherine",
  "color" : "Ginger",
  "toys"  : ["String", "Mouse"]
}
```

But having Python allows you to be much more expressive. You can adjust the data entry in many different ways to make it simpler, more explicit, or more aesthetic.

```python
""" My Favourite Pets - Another example """

from pymark.util import enum, module, struct

""" Functions """

def pet(**kwargs): return kwargs
def color(r, g, b): return (r, g, b)

""" Constants """

Types = enum("Dog", "Horse", "Cat")
Toys = enum("String", "Mouse", "Brush", "Bone", "Ball")

Colors = struct(
    Brown = color(94, 83, 51),
    White = color(255, 255, 255),
    Ginger = color(237, 133, 14),
)

""" Module """

pets = module(
  
  benny = pet(
    type = Types.Dog,
    name = "Benny Boos",
    color = Colors.Brown,
    toys = [Toys.Bone, Toys.Ball]
  ),

  roger = pet(
    type = Types.Horse,
    name = "Roger Horse",
    color = Colors.White,
    toys = [Toys.Brush, Toys.String]
  ),
  
  catherine = pet(
    type = Types.Cat,
    name = "Catherine",
    color = Colors.Ginger, 
    toys = [Toys.String, Toys.Mouse]
  )

)
```

Perhaps the above example looks like a bit of a mess, but it does show off some of the potential. I have no real preference for either style but in using Python you have the option to adapt your markup depending on preference or domain.


Compiling
---------

Once you have the module written just feed it into pymark.

```sh
pymark pets_two.py > pets_two.pmk
```


Application
-----------

I have tried to make the API fairly simplistic and clear.

Loading data at runtime and making it easy to access in a type safe language is always going to be horrible. It is one of the major issues with doing object markup in a separate language and there is little way around it.

C
-

In C you can do something like this.

```c
#include <stdio.h>

#include "../parsers/PyMark.h"

int main(int argc, char** argv) {
  
  PyMarkObject* pets_mod = PyMark_Unpack("pets_two.pmk");
  PyMarkObject* pets = pets_mod->get(pets_mod, "pets");
  
  PyMarkObject* cath = pets->get(pets, "catherine");
  PyMarkObject* cath_color = cath->get(cath, "color");
  
  printf("TypeID: %i\n", cath->get(cath, "type")->as_int);
  printf("Name: %s\n", cath->get(cath, "name")->as_string);
  printf("Color: (%i, %i, %i)\n", cath_color->items[0]->as_int, 
                                cath_color->items[1]->as_int, 
                                cath_color->items[2]->as_int);
  
  PyMark_Delete(pets_mod);
  
  return 0;
}
```

C++
---

The C++ parser which has somewhat nicer syntax.

```c++
#include <stdio.h>

#include "../parsers/PyMark.hpp"

int main(int argc, char** argv) {
  
  PyMark::PyMarkObject* pets_mod = PyMark::Unpack("pets_two.pmk");
  PyMark::PyMarkObject* cath = pets_mod->Get("pets")->Get("catherine");
  
  printf("TypeID: %i\n", cath->Get("type")->AsInt());
  printf("Name: %s\n", cath->Get("name")->AsString());
  printf("Color: (%i, %i, %i)\n", cath->Get("color")->At(0)->AsInt(), 
                                  cath->Get("color")->At(1)->AsInt(), 
                                  cath->Get("color")->At(2)->AsInt());
  
  delete pets_mod;
  
  return 0;
}
```

Python
------

As clearly nicest in Python as the objects more or less go in and out unchanged.

```python
import pymark.unpacker

pets_mod = pymark.unpacker.unpack_file("pets_two.pmk")

print "TypeID: %i" % pets_mod["pets"]["catherine"]["type"]
print "Name: %s" % pets_mod["pets"]["catherine"]["name"]
print "Color: (%i, %i, %i)" % pets_mod["pets"]["catherine"]["color"]
```



