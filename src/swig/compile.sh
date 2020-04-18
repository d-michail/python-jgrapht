
# Compile 

swig -python jgrapht.i
gcc -c -fpic jgrapht_wrap.c -I/usr/include/python3.6m -I.
gcc -shared jgrapht_wrap.o -L. -lgrapht_nlib -o _jgrapht.so
