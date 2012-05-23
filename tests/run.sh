pymark clothing.py clothing.pmk
pymark pets_one.py pets_one.pmk
pymark pets_two.py pets_two.pmk

rm test0 test1 test2 test5
rm test0.exe test1.exe test2.exe test5.exe
rm test4.class
rm test5.hi test5.o

gcc --std=gnu99 -Wall -Werror -g test0.c ../pymark/parsers/PyMark.c -o test0
gcc --std=gnu99 -Wall -Werror -g test1.c ../pymark/parsers/PyMark.c -o test1
g++ --std=c++0x -Wall -Werror -g test2.cpp ../pymark/parsers/PyMark.cpp -o test2
javac ../pymark/parsers/PyMarkObject.java
javac -classpath ../pymark/parsers test4.java
ghc -i../pymark/parsers test5.hs -o test5 

./test0
./test1
./test2
python test3.py
java -classpath ./:../pymark/parsers/ test4
./test5
