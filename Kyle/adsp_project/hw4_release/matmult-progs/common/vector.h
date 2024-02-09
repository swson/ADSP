#ifndef VECTOR_H__
#define VECTOR_H__

#include <stdio.h>

struct vector;

enum shape {
	VECT_COLUMN = 0,
	VECT_ROW
};

struct vector* make_col_ones(size_t rows);
void dump_vector(FILE* stream, const struct vector* v);
struct vector* destroy_vector(struct vector* v);
long double get_vector_value(const struct vector* v, size_t offset);
size_t get_vector_size(const struct vector* v);
enum shape get_vector_shape(const struct vector* v);
const char* get_vector_type(const struct vector* v);
long double set_vector_value(struct vector* vect,
		size_t index,
		long double val);
const long double* get_vector_data(const struct vector* v);
long double* get_vector_data_rw(const struct vector* v);
struct vector* scramble_and_swap_vector(struct vector* restrict dest,
		struct vector* restrict src, const size_t* restrict p);
int scramble_vector(struct vector* v, const size_t* restrict p);
struct vector* clear_vector(struct vector* v);


#endif
