
TARGET=_jgrapht.so
SOURCES=jgrapht.c
CC=gcc
CFLAGS=-c -fpic -Wall -Wextra -O3 #-D__debug__
LDFLAGS=-Wall -O3 -shared

SWIG=swig
SWIGFLAGS=-python
INCLUDES=-I/usr/include/python3.6 -I.

WRAPPER=$(SOURCES:.c=.py) $(SOURCES:.c=)_wrap.c
OBJECTS=$(SOURCES:.c=.o) $(WRAPPER:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS) $(WRAPPER)
	$(CC) $(LDFLAGS) $(filter-out $(SOURCES:.c=.py),$(OBJECTS)) -o $@

debug: $(SOURCES:.c=.o) $(DEBUG)
	$(CC) $(LDFLAGS:-shared=) $(SOURCES:.c=.o) $(DEBUG) -o $@

%_wrap.c: %.i
	$(SWIG) $(SWIGFLAGS) $(SOURCES:.c=.i)

%.py: %_wrap.c
	@

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $<

clean:
	rm -f $(DEBUG:.c=.o) $(filter-out $(SOURCES:.c=.py),$(OBJECTS)) $(WRAPPER) $(TARGET) debug

rebuild: clean all

