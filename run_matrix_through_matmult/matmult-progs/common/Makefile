SRC := $(wildcard *.c)
OBJ := $(SRC:%.c=%.o)

TEST := $(addsuffix _test,$(OBJ:%.o=%))

CC = gcc
LD = gcc
RM = rm -f

CFLAGS += \
	-O3 \
	-Wall \
	-Wextra \
	-ffunction-sections \
	-fdata-sections \
	-std=gnu11

LDFLAGS += -Wl,--gc-sections

.PHONY: all testsuite clean

all: $(OBJ)

openmp: CFLAGS += -fopenmp
openmp: LDFLAGS += -fopenmp
openmp: all

testsuite: CFLAGS += -DTESTCASE -g
testsuite: $(TEST)

omp_testsuite: CFLAGS += -fopenmp
omp_testsuite: LDFLAGS += -fopenmp
omp_testsuite: testsuite

clean:
	@echo "  RM $(OBJ) $(TEST) $(addsuffix .o,$(TEST))"
	@-$(RM) $(OBJ) $(TEST) $(addsuffix .o,$(TEST))


%.o: %.c
	@echo "  CC $<"
	@$(CC) $(CFLAGS) -c $< -o $@

%_test: %.c
	@echo "  CC $<"
	@$(CC) $(CFLAGS) -c $< -o $@.o
	@echo "  LD $@"
	@$(LD) $(LDFLAGS) -o $@ $@.o
