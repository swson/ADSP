#ifndef TS_DEFS_H__
#define TS_DEFS_H__

#ifndef TESTCASE
#error "This file is part of the testsuite only!"
#endif

#ifdef CRS_TEST
/* CRS Matrix format */
#define LOAD_MATRIX(stream)		load_crs_matrix(stream)
#define SYM_CHECK(m_)			crs_is_symmetric(m_)
#define DUMP_MATRIX(stream, m_)	dump_crs_matrix(stream, m_)
#define MAT_MULT_SYMM			crs_symm_vect_mult
#define MAT_MULT				crs_vect_mult
#define GET_MATRIX_SIZE(m)		get_crs_matrix_size(m)
#define DESTROY_MATRIX(m)		destroy_crs_matrix(m)
#define SWAP_FUNCTION(d, s, p)
#define MAT_SHUFFLE_ARRAY(m)

typedef struct crs_matrix	s_matrix;
typedef struct vector* (*mat_vect_mult_fn)(const struct crs_matrix*,
		const struct vector*,
		struct vector*);
#else
/* TJDS Matrix format */
#define LOAD_MATRIX(stream)		load_tjds_matrix(stream)
#define SYM_CHECK(m_)			tjds_is_symmetric(m_)
#define DUMP_MATRIX(stream, m_)	dump_tjds_matrix(stream, m_)
#define MAT_MULT_SYMM			tjds_symm_vect_mult
#define MAT_MULT				tjds_vect_mult
#define GET_MATRIX_SIZE(m)		get_tjds_matrix_size(m)
#define DESTROY_MATRIX(m)		destroy_tjds_matrix(m)
#define SWAP_FUNCTION(d, s, p)	scramble_and_swap_vector(d, s, p)
#define MAT_SHUFFLE_ARRAY(m)	get_tjds_permutation_array(m)

typedef struct tjds_matrix	s_matrix;
typedef struct vector* (*mat_vect_mult_fn)(const struct tjds_matrix*,
		const struct vector*,
		struct vector*);

#endif

#endif
