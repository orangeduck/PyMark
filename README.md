PyMark
======


About
-----

PyMark is a lightweight and powerful object markup solution which uses Python as a frontend and compiles data to a simple binary format for use in an application.

Having a focus on a powerful frontend has many benefits missing from other object markup techniques:

* Bad syntax is caught at compile time.
* A whole programming language to help you.
* Lists, Tuples, Dictionaries are all first class structures.
* Structure manipulation/patching can be done easily and early.

And having a simple backend has some benefits too.

* A parser in less than 250 lines of C.
* Reads/Writes/Streams data quickly.


Drawbacks
---------

Having so much happen in the frontend makes the system somewhat one-directional.

While the human readable source can be reconstructed in some sense, data such as comments are lost in the compilation. PyMark is best used for human written object description for use in an application, not for marking up documents or sharing rich information.

Usage
-----

The first task is to actually enter your data. For this you simply create a python module. All native objects at the top level other than the builtins dictionary will be exported. You can structure this how you please. If you are a JSON fan you might write something like this:

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

""" Constants """

Types = enum("Dog", "Horse", "Cat")
Toys = enum("String", "Mouse", "Brush", "Bone", "Ball")

Colors = struct(
    Brown = (94, 83, 51),
    White = (255, 255, 255),
    Ginger = (237, 133, 14),
)

""" Module """

pets = module(
  
  benny = struct(
    type = Types.Dog,
    name = "Benny Boos",
    color = Colors.Brown,
    toys = [Toys.Bone, Toys.Ball]
  ),

  roger = struct(
    type = Types.Horse,
    name = "Roger Horse",
    color = Colors.White,
    toys = [Toys.Brush, Toys.String]
  ),
  
  catherine = struct(
    type = Types.Cat,
    name = "Catherine",
    color = Colors.Ginger, 
    toys = [Toys.String, Toys.Mouse]
  )

)
```

Perhaps the above example looks like a bit of a mess, but it does show off some of the potential. I have no real preference for either style but in using Python you have the option to adapt your markup depending on preference or domain.


Application
-----------

Once you have written the module just feed it into pymark.

```bash
pymark pets_two.py > pets_two.pmk
```

For access in an application I have tried to make the API fairly simplistic and clear.

Loading data at runtime and making it easy to access in a type safe language is always going to be horrible. It is one of the major issues with doing object markup in a separate language and there is little way around it. Saying that it doesn't have to be as obtuse as some XML or highly structured APIs.

Feedback is more than welcome on any of these.

C
-

In C you can do something like this.

```c
#include <stdio.h>

#include "../pymark/parsers/PyMark.h"

int main(int argc, char** argv) {
  
  PyMarkObject* pets_two = PyMark_Unpack("pets_two.pmk");
  
  printf("TypeID: %i\n", pets_two->get(pets_two, "pets.catherine.type")->as_int);
  printf("Name: %s\n", pets_two->get(pets_two, "pets.catherine.name")->as_string);
  
  PyMarkObject* color = pets_two->get(pets_two, "pets.catherine.color");
  printf("Color: (%i, %i, %i)\n", color->items[0]->as_int, 
                                  color->items[1]->as_int, 
                                  color->items[2]->as_int);
  
  PyMark_Delete(pets_two);
  
  return 0;
}
```

C++
---

In C++ the parser has somewhat nicer syntax as you don't have to pass in the implicit self. This means you can chain together accesses nicely E.G ``` pets_two->Get("pets")->Get("catherine")->Get("type");  ```, or you can still use the dotted syntax and the function will tokenize the components for you.

```c++
#include <stdio.h>

#include "../pymark/parsers/PyMark.hpp"

int main(int argc, char** argv) {
  
  PyMark::PyMarkObject* pets_two = PyMark::Unpack("pets_two.pmk");
  
  printf("TypeID: %i\n", pets_two->Get("pets.catherine.type")->AsInt());
  printf("Name: %s\n", pets_two->Get("pets.catherine.name")->AsString());
  
  PyMark::PyMarkObject* color = pets_two->Get("pets.catherine.color");
  printf("Color: (%i, %i, %i)\n", color->At(0)->AsInt(), 
                                  color->At(1)->AsInt(), 
                                  color->At(2)->AsInt());
  
  delete pets_two;
  
  return 0;
}
```

Python
------

Access is nicest in Python as the objects more or less go in and out unchanged.

```python
import pymark.unpacker

pets_mod = pymark.unpacker.unpack_file("pets_two.pmk")

print "TypeID: %i" % pets_mod["pets"]["catherine"]["type"]
print "Name: %s" % pets_mod["pets"]["catherine"]["name"]
print "Color: (%i, %i, %i)" % pets_mod["pets"]["catherine"]["color"]
```

Java
----

```java
import java.io.IOException;

class test4 {
  
  public static void main(String[] args) throws IOException {
    
    PyMarkObject pets_two = PyMarkObject.Unpack("pets_two.pmk");
    
    System.out.printf("TypeID: %d\n", pets_two.get("pets.catherine.type").asInt()); 
    System.out.printf("Name: %s\n", pets_two.get("pets.catherine.name").asString());
    
    PyMarkObject color = pets_two.get("pets.catherine.color");
    System.out.printf("Color: (%d, %d, %d)\n", color.at(0).asInt(),
                                               color.at(1).asInt(),
                                               color.at(2).asInt());
    
  }

}
```

