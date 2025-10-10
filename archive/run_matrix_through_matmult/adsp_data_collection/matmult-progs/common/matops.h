#ifndef MATOPTS_H__
#define MATOPTS_H__

#include "crs_matrix.h"
#include "tjds_matrix.h"
#include "vector.h"

struct vector* crs_vect_mult(
		const struct crs_matrix* op_1,
		const struct vector* op_2,
		struct vector* result
	);

struct vector* crs_symm_vect_mult(
		const struct crs_matrix* op_1,
		const struct vector* op_2,
		struct vector* result);

struct vector* tjds_vect_mult(
		const struct tjds_matrix* op_1,
		const struct vector* op_2,
		struct vector* result);

struct vector* tjds_symm_vect_mult(
		const struct tjds_matrix* op_1,
		const struct vector* op_2,
		struct vector* result);
#endif
