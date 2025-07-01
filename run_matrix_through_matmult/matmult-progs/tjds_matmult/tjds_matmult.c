#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

#include <tjds_matrix.h>
#include <vector.h>
#include <cpu.h>
#include <timeaux.h>
#include <matops.h>

#ifdef _OPENMP
#define CFLAGS_ALL CFLAGS " -fopenmp"
#define LDFLAGS_ALL LDFLAGS " -fopenmp"
#else
#define CFLAGS_ALL CFLAGS
#define LDFLAGS_ALL LDFLAGS
#endif

int main(void) {
	struct tjds_matrix* m;
	struct vector* v, * r, * t, * s;
	const size_t* perm_array;
	
	uint64_t (*time_function)(void) = (uint64_t(*)(void))NULL;
	struct vector* (*mat_mult_fn)(const struct tjds_matrix*,
			const struct vector*,
			struct vector*);

	uint64_t time_start, time_end;

	puts("do not use!");
	exit(1);

	/* CPU identification */
	fprintf(stdout, "Running on CPU: %s\n", get_cpu_name());

	/* compile time options */
	fprintf(stdout, "compiled with: %s %s\n", CC, CFLAGS_ALL);

	/* link time options */
	fprintf(stdout, "linked with: %s %s\n", LD, LDFLAGS_ALL);

	fprintf(stdout, "compiler specs: %s\n", COMPILERSPEC);

	/* serializing timestamp counter read check */
	if(cpu_has_rtdscp()) {
		time_function = rdtscp;
	}
	fprintf(stdout, "CPU %s the RTDSCP instruction.\n",
				time_function ? "supports" : "does not support");
	
	/* check for non-serializing read */
	if(!time_function && cpu_has_rtdsc()) {
		time_function = rdtsc;
		fprintf(stdout, "CPU supports the RTDSC instruction.\n");
	} else if(!time_function) {
		fprintf(stdout, "CPU does not have built-in timing mechanism."
						"Using software solution.\n");
		time_function = soft_timer;
	}

	/* load the matrix */
	if(!(m = load_tjds_matrix(stdin))) {
		perror("load_matrix()");
		return EXIT_FAILURE;
	}

	fprintf(stdout, "Loaded matrix\n");
	dump_tjds_matrix(stdout, m);
	if(tjds_is_symmetric(m)) {
		mat_mult_fn = tjds_symm_vect_mult;
	} else {
		mat_mult_fn = tjds_vect_mult;
	}

	/* prepare the original vector */
	if(!(v = make_col_ones(get_tjds_matrix_size(m)))) {
		perror("make_col_ones()");
		return EXIT_FAILURE;
	}

	/* prepare the results vector */
	if(!(r = make_col_ones(get_tjds_matrix_size(m)))) {
		perror("make_col_ones()");
		return EXIT_FAILURE;
	}

	/* prepare mix vector */
	if(!(s = make_col_ones(get_tjds_matrix_size(m)))) {
		perror("make_col_ones()");
		return EXIT_FAILURE;
	}

	perm_array = get_tjds_permutation_array(m);
	/* perform y = A^n x */
	time_start = time_function();
	for(int i = 0; i < 1000; i++) {
		scramble_and_swap_vector(s, v, perm_array);
		t = mat_mult_fn(m, v, r);
		r = v;
		v = t;
	}
	time_end = time_function();

	fprintf(stdout, "results:\n");
	dump_vector(stdout, v);

	fprintf(stdout, "computational time: %lu\n", time_end - time_start);

	destroy_vector(s);
	destroy_vector(r);
	destroy_vector(v);
	destroy_tjds_matrix(m);

	return EXIT_SUCCESS;
}
