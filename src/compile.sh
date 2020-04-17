
# Compile 

#gcc -c -fpic libjgrapht_wrap.c -I/usr/include/python3.6m -I.
#gcc -shared libjgrapht_wrap.o -o _libjgrapht.so

#swig -python libjgrapht.i
#python3 setup.py build_ext --inplace

if [ ! -e 'jgrapht_nlib.so' ]; then
    ln -s jgrapht_nlib.so libjgrapht_nlib.so
fi

gcc -c -fpic pjgrapht.c -I.
gcc -shared pjgrapht.o -o libpjgrapht.so

gcc -o client client.c -L. -lpjgrapht -ljgrapht_nlib  -I.

