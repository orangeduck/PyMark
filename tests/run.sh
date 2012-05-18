pymark clothing.py > clothing.pmk
pymark pets_one.py > pets_one.pmk
pymark pets_two.py > pets_two.pmk

gcc --std=gnu99 -Wall -Werror -g test0.c ../parsers/PyMark.c -o test0
gcc --std=gnu99 -Wall -Werror -g test1.c ../parsers/PyMark.c -o test1
g++ --std=c++0x -Wall -Werror -g test2.cpp ../parsers/PyMark.cpp -o test2

./test0
./test1
./test2
