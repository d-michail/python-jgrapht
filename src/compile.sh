
# Compile 

#python3 setup.py build_ext --inplace

if [ ! -e 'jgrapht_nlib.so' ]; then
    ln -s jgrapht_nlib.so libjgrapht_nlib.so
fi

gcc -c -fpic pjgrapht.c -I.
gcc -shared pjgrapht.o -o libpjgrapht.so

gcc -o client client.c -L. -lpjgrapht -ljgrapht_nlib  -I.

swig -python pjgrapht.i
gcc -c -fpic pjgrapht_wrap.c -I/usr/include/python3.6m -I.
gcc -shared pjgrapht_wrap.o -L. -lpjgrapht -ljgrapht_nlib -o _pjgrapht.so
