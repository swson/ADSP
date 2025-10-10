#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "vector.h"

struct vector {
	long double* data;
	size_t data_len;
	enum shape vect_shape;
};

const char* const vect_type[] = {
		"column vector",
		"row vector"
	};

struct vector* make_col_ones(size_t rows) {
	struct vector* ret;

	/* allocate base structure */
	if(!(ret = (struct vector*)malloc(sizeof(*ret)))) {
		return (struct vector*)NULL;
	}

	/* allocate data array */
	if(!(ret->data = (long double*)malloc(rows * sizeof(*(ret->data))))) {
		free(ret);
		return (struct vector*)NULL;
	}

	/* populate data structure */
	ret->data_len = rows;
	ret->vect_shape = VECT_COLUMN;
	while(rows) {
		ret->data[--rows] = 1.0;
	}

	return ret;
}

void dump_vector(FILE* stream, const struct vector* v) {
	size_t data_len = v->data_len;
	fprintf(stream, "%s\n", get_vector_type(v));
	for(size_t i = 0; i < data_len; i++) {
		fprintf(stream, "%Lf\n", v->data[i]);
	}
}

struct vector* destroy_vector(struct vector* v) {
	free(v->data);
	free(v);

	return (struct vector*)NULL;
}

long double get_vector_value(const struct vector* v, size_t offset) {
	return v->data[offset];
}

size_t get_vector_size(const struct vector* v) {
	return v->data_len;
}

enum shape get_vector_shape(const struct vector* v) {
	return v->vect_shape;
}

const char* get_vector_type(const struct vector* v) {
	return vect_type[get_vector_shape(v)];
}

long double set_vector_value(
		struct vector* vect,
		size_t index,
		long double val) {
	return vect->data[index] = val;
}

const long double* get_vector_data(const struct vector* v) {
	return v->data;
}

long double* get_vector_data_rw(const struct vector* v) {
	return v->data;
}

struct vector* clear_vector(struct vector* v) {
#	ifdef _OPENMP
#	pragma omp parallel for
#	endif
	for(size_t i = 0; i < v->data_len; i++) {
		v->data[i] = 0;
	}
	return v;
}

struct vector* scramble_and_swap_vector(struct vector* restrict dest,
		struct vector* restrict src, const size_t* restrict p) {

	long double* t;;

	/* shuffle */
#	ifdef _OPENMP
#	pragma omp parallel for
#	endif
	for(size_t i = 0; i < src->data_len; i++) {
		dest->data[i] = src->data[p[i] - 1];
	}

	/* and swap */
	t = src->data;
	src->data = dest->data;
	dest->data = t;

	return src;
}

int scramble_vector(struct vector* v, const size_t* restrict p) {
	long double* pv_data;

	if(!(pv_data = (long double*)malloc(sizeof(long double) * v->data_len))) {
		return -1;
	}
	
#	ifdef _OPENMP
#	pragma omp parallel for
#	endif
	for(size_t i = 0; i < v->data_len; i++) {
		pv_data[i] = v->data[p[i]-1];
	}

	free(v->data);
	v->data = pv_data;

	return 0;
}

#ifdef TESTCASE
#include <assert.h>

int main(void) {
	struct vector* v;
	v = make_col_ones(32);

	assert(v != NULL);
	dump_vector(stdout, v);

	destroy_vector(v);
	return EXIT_SUCCESS;
}

#endif
