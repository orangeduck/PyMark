pymark ../examples/clothing.py
pymark ../examples/pets_one.py
pymark ../examples/pets_two.py

gcc --std=gnu99 -Wall -Werror test0.c ../parsers/PyMark.c -o test0
gcc --std=gnu99 -Wall -Werror test1.c ../parsers/PyMark.c -o test1
g++ --std=c++0x -Wall -Werror test2.cpp ../parsers/PyMark.cpp -o test2

./test0
./test1
./test2
