#include "matops.h"

#include "crs_matrix.h"
#include "tjds_matrix.h"
#include "vector.h"

struct vector* crs_vect_mult(
		const struct crs_matrix* op_1,
		const struct vector* op_2,
		struct vector* result) {

	const long double* val = get_crs_matrix_val_array(op_1);
	const size_t* col_ind = get_crs_matrix_column_array(op_1);
	const size_t* row_ptr = get_crs_matrix_row_array(op_1);
	const long double* vector_data = get_vector_data(op_2);
	size_t vect_size = get_vector_size(op_2);

#	ifdef _OPENMP
#	pragma omp parallel for
#	endif
	for(size_t i = 0; i < vect_size; i++) {
		long double t = 0;
		for(size_t j = row_ptr[i] - 1; j < row_ptr[i+1] - 1; j++) {
			t += val[j] * vector_data[col_ind[j]-1];
		}
#		ifdef TESTCASE
#		include <assert.h>
		assert(t == set_vector_value(result, i, t));
#		else
		set_vector_value(result, i, t);
#		endif
	}
	return result;
}

struct vector* crs_symm_vect_mult(
		const struct crs_matrix* op_1,
		const struct vector* op_2,
		struct vector* result) {
	
	const long double* val = get_crs_matrix_val_array(op_1);
	const size_t* col_ind = get_crs_matrix_column_array(op_1);
	const size_t* row_ptr = get_crs_matrix_row_array(op_1);
	const long double* vector_data = get_vector_data(op_2);
	long double* result_data = get_vector_data_rw(result);
	size_t vect_size = get_vector_size(op_2);

	clear_vector(result);

#	ifdef _OPENMP
#	pragma omp parallel for
#	endif
	for(size_t i = 0; i < vect_size; i++) {
		long double t = 0;
		for(size_t j = row_ptr[i] - 1; j < row_ptr[i+1] - 1; j++) {
			size_t k = col_ind[j] - 1;
			t += val[j] * vector_data[k];
		}
		result_data[i] = t;
	}

	/* not trivially paralelizable, only one thing in the loop */
	for(size_t i = 0; i < vect_size; i++) {
		for(size_t j = row_ptr[i] - 1; j < row_ptr[i+1] - 1; j++) {
			size_t k = col_ind[j] - 1;
			if(i != k) {
				result_data[k] += val[k] * vector_data[i];
			}
		}
	}

	return result;
}

struct vector* tjds_symm_vect_mult(
		const struct tjds_matrix* op_1,
		const struct vector* op_2,
		struct vector* result) {

	const long double* value_list = get_tjds_matrix_val_array(op_1);
	const size_t* row_indexes = get_tjds_matrix_row_array(op_1);
	const size_t* start_position = get_tjds_matrix_start_pos_array(op_1);
	const long double* vector_data = get_vector_data(op_2);
	long double* result_data = get_vector_data_rw(result);
	size_t jagged_diagonals = get_jagged_diagonals(op_1);

	clear_vector(result);

	/* diagonal */
#	ifdef _OPENMP
#	pragma omp parallel for
#	endif
	for(size_t j = 0; j < start_position[1] - 1; j++) {
		size_t p = row_indexes[j] - 1;

		result_data[p] = value_list[j] * vector_data[j];

		if(p != j) {
			result_data[j] += value_list[j] * vector_data[p];
		}
	}

	/* rest of the matrix, can't be trivially parallelized */
	for(size_t i = 1; i < jagged_diagonals; i++) {
		size_t k = 0;
		for(size_t j = start_position[i] - 1;
				j < start_position[i + 1] - 1;
				j++) {
		
			size_t p = row_indexes[j] - 1;
			
			result_data[p] += value_list[j] * vector_data[k];
			result_data[k] += value_list[j] * vector_data[p];
			
			k++;
		}
	}

	return result;
}

struct vector* tjds_vect_mult(
		const struct tjds_matrix* op_1,
		const struct vector* op_2,
		struct vector* result) {
	
	const long double* value_list = get_tjds_matrix_val_array(op_1);
	const size_t* row_indexes = get_tjds_matrix_row_array(op_1);
	const size_t* start_position = get_tjds_matrix_start_pos_array(op_1);
	const long double* vector_data = get_vector_data(op_2);
	long double* result_data = get_vector_data_rw(result);
	size_t jagged_diagonals = get_jagged_diagonals(op_1);

	clear_vector(result);

#	ifdef _OPENMP
#	pragma omp parallel for
#	endif
	for(size_t i = 0; i < jagged_diagonals; i++) {
		size_t k = 0;
		for(size_t j = start_position[i] - 1;
				j < start_position[i+1] - 1;
				j++) {
			size_t p = row_indexes[j] - 1;
#			ifdef _OPENMP
			/* multiple threads can be accessing result_data[p] */
#			pragma omp atomic
#			endif
			result_data[p] += value_list[j] * vector_data[k];
			k++;
		}
	}

	return result;
}

#ifdef TESTCASE
#include <assert.h>
#include <stdlib.h>
#include "ts_defs.h"

int main(void) {
	s_matrix* m = LOAD_MATRIX(stdin);
	mat_vect_mult_fn mat_mult_fn;

	assert(m != NULL);
	size_t col = GET_MATRIX_SIZE(m);
	struct vector* v = make_col_ones(col);
	struct vector* r = make_col_ones(col);
	struct vector* s __attribute__((unused)) = make_col_ones(col);
	struct vector* t;
	assert(v != NULL);
	assert(r != NULL);

	DUMP_MATRIX(stdout, m);
	if(SYM_CHECK(m)) {
		mat_mult_fn = MAT_MULT_SYMM;
	} else {
		mat_mult_fn = MAT_MULT;
	}

	dump_vector(stdout, v);
	dump_vector(stdout, r);

	for(size_t iter = 0; iter < 10; iter++) {
		//fprintf(stdout, "[+] iteration: %zu\n", iter);
		SWAP_FUNCTION(s, v, MAT_SHUFFLE_ARRAY(m));
		t = mat_mult_fn(m, v, r);
		assert(r == t);
		dump_vector(stdout, t);
		r = v;
		v = t;
	}

	DESTROY_MATRIX(m);
	destroy_vector(v);
	destroy_vector(r);
	destroy_vector(s);

	return EXIT_SUCCESS;
}

/* do not include main() from these files */
#undef TESTCASE

#ifdef CRS_TEST
#include "crs_matrix.c"
#else
#include "tjds_matrix.c"
#endif
#include "vector.c"
#endif
