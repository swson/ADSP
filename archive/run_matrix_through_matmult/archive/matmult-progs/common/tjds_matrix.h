#ifndef TJDS_MATRIX_H__
#define TJDS_MATRIX_H__

#include <stdio.h>

struct tjds_matrix;

struct tjds_matrix* load_tjds_matrix(FILE* stream);
void dump_tjds_matrix(FILE* stream, const struct tjds_matrix* m);
struct tjds_matrix* destroy_tjds_matrix(struct tjds_matrix* m);
const long double* get_tjds_matrix_val_array(const struct tjds_matrix* m);
const size_t* get_tjds_permutation_array(const struct tjds_matrix* m);
const size_t* get_tjds_matrix_start_pos_array(const struct tjds_matrix* m);
const size_t* get_tjds_matrix_row_array(const struct tjds_matrix* m);
size_t get_jagged_diagonals(const struct tjds_matrix* m);

size_t get_tjds_matrix_size(const struct tjds_matrix* m);
size_t get_tjds_matrix_nz_elements(const struct tjds_matrix* m);
size_t get_tjds_perm_len(const struct tjds_matrix* m);
int tjds_is_symmetric(const struct tjds_matrix* m);
size_t get_tjds_matrix_size(const struct tjds_matrix* m);

#endif	/* TJDS_MATRIX_H__ */
