CC:=gcc
CFLAGS:=-fPIC -O3 -Wall -Wextra -Iinclude
LDFLAGS:=-shared
LIB=libpmu.so
PREFIX=/usr/local

SRC=$(wildcard src/*.c)
OBJ=$(SRC:.c=.o)

EXAMPLE_LDFLAGS=-Wl,-rpath,$(shell pwd) $(LIB)
EXAMPLES=$(patsubst %.c, %, $(wildcard examples/*.c))

all: build examples

build: $(OBJ)
	$(CC) -o $(LIB) $(OBJ) $(LDFLAGS)

examples: build $(EXAMPLES)

$(EXAMPLES): %: %.c
	$(CC) $< $(CFLAGS) -o $@ $(EXAMPLE_LDFLAGS)

src/%.o: src/%.c
	$(CC) -c $< -o $@ $(CFLAGS)

install: all
	cp $(LIB) $(PREFIX)/lib
	cp -r include $(PREFIX)/include/pmu

uninstall:
	rm -f $(PREFIX)/lib/$(LIB)
	rm -rf $(PREFIX)/include/pmu

kernel:
	modprobe msr
	make -C cr4
	insmod cr4/pceset.ko

clean:
	rm -rf $(OBJ) $(EXAMPLES) $(LIB)
