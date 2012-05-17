pymark ../examples/clothing.py

gcc --std=gnu99 -Wall -Werror test0.c ../parsers/PyMark.c -o test0

./test0
