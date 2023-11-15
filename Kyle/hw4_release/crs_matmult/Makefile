ELF := crs_matmult

SRC := new_crs_matmult.c
COMMON := cpu matops crs_matrix timeaux vector

SRC += $(addprefix ../common/,$(addsuffix .c,$(COMMON)))

OBJ := $(SRC:%.c=%.o)

CC = gcc
LD = gcc
RM = rm -f

CFLAGS += \
	-I../common \
	-O3 \
	-Wall \
	-Wextra \
	-Werror \
	-march=native \
	-mtune=native \
	-ffunction-sections \
	-fdata-sections \
	-std=gnu11

LDFLAGS += -Wl,--gc-sections
LIBS =

GCC_SPEC = $(shell gcc -v 2>&1 | grep Configured | cut -d ':' -f 2-)

CFLAGS := $(CFLAGS) -DCC="\"$(CC)\"" \
		-DCFLAGS="\"$(CFLAGS)\"" \
		-DLD="\"$(LD)\"" \
		-DLDFLAGS="\"$(LDFLAGS) $(LIBS)\"" \
		-DCOMPILERSPEC="\"$(GCC_SPEC)\""

.PHONY: all clean


all: $(ELF)

debug: CFLAGS += -g -O0
debug: all

openmp: CFLAGS += -fopenmp
openmp: LDFLAGS += -fopenmp
openmp: ELF := $(ELF)_omp
openmp: all

$(ELF): $(OBJ)
	@echo "  LD $(ELF)"
	@$(LD) $(LDFLAGS) -o $(ELF) $(OBJ) $(LIBS)

clean:
	@echo "  RM $(OBJ) $(ELF) $(ELF)_omp"
	@-$(RM) $(OBJ) $(ELF) $(ELF)_omp


%.o: %.c
	@echo "  CC $<"
	@$(CC) $(CFLAGS) -c $< -o $@

