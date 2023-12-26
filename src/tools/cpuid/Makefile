SRC := pycpuid.c

OBJ := $(SRC:%.c=%.o)
OBJ := $(OBJ:%.cpp=%.o)
OBJ += cpuid-aux.c.o cpuid-aux.s.o

CC := gcc
AS := gcc
LD := gcc

CFLAGS :=	-Wall -Werror \
			-O2 -march=native \
			-fpic \
			-ffunction-sections \
			-fdata-sections

ASFLAGS := $(CFLAGS)

LDFLAGS := -shared -fpic

CFLAGS += $(shell pkg-config --cflags python3)
LIBS := $(shell pkg-config --libs python3)

LIB := pycpuid.so

.PHONY: all clean

all: $(LIB)

clean:
	-rm -f $(LIB) $(OBJ)

$(LIB): $(OBJ)
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

cpuid-aux.c.o: cpuid-aux.S
	$(CC) -x c $(CFLAGS) -c -o $@ $<

cpuid-aux.s.o: cpuid-aux.S
	$(AS) $(ASFLAGS) -c -o $@ $<
