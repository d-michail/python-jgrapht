
%module pjgrapht

%{
#define SWIG_FILE_WITH_INIT
#include "pjgrapht.h"
%}

void pjgrapht_thread_create();
void pjgrapht_thread_destroy();
int pjgrapht_get_errno();
void pjgrapht_clear_errno();
