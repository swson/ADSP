#ifndef CRS_MATRIX_H__
#define CRS_MATRIX_H__

#include <stdio.h>

struct crs_matrix;

struct crs_matrix* load_crs_matrix(FILE* stream);
void dump_crs_matrix(FILE* stream, struct crs_matrix* m);
struct crs_matrix* destroy_crs_matrix(struct crs_matrix* m);
const long double* get_crs_matrix_val_array(const struct crs_matrix* m);
const size_t* get_crs_matrix_column_array(const struct crs_matrix* m);
const size_t* get_crs_matrix_row_array(const struct crs_matrix* m);
size_t get_crs_matrix_size(const struct crs_matrix* m);
size_t get_crs_matrix_nz_elements(const struct crs_matrix* m);
int crs_is_symmetric(const struct crs_matrix* m);

#endif
