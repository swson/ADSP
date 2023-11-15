#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

#include <crs_matrix.h>
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
	struct crs_matrix* m;
	struct vector* v, * r, * t;
	struct vector* (*mult_fn)(const struct crs_matrix*,
			const struct vector*,
			struct vector*);
	uint64_t (*time_function)(void) = (uint64_t(*)(void))NULL;
	uint64_t time_start, time_end;
	
	
	FILE *fptr; // Kyle edit
	
	/*Going to do this because c can't do strings and I don't feel like declaring a character array right now
	
	baseline_file_path = "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/mat_cache/crs/494_bus.crs"
	
	corrupted_file_path = "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/corrupted_matricies/crs/non_zero/494_bus_gauss_0p01_0p01_sym_nonzero.crs"
	
	
	494_bus_gauss_0p01_0p01_sym_nonzero.crs
	
	*/
	

	
	fptr = fopen( "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/corrupted_matricies/crs/non_zero/494_bus_gauss_0p01_0p01_sym_nonzero.crs","r");	// Kyle edit REPLACE FIRST STRING WITH THE PATH TO THE CRS FILE YOU WANT TO RUN
	if(!fptr) {
		perror("fopen():");
		return -1;
	}
	
	fprintf(stdout,"Kyle made changes to this file on 10-6-23");
	
	

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

	/* load the crs_matrix */
	if(!(m = load_crs_matrix(fptr))) {		// Kyle edit. stdin was the original argument to load_crs_matrix()
		perror("load_crs_matrix()");
		return EXIT_FAILURE;
	}

	if(crs_is_symmetric(m)) {
		mult_fn = crs_symm_vect_mult;
	} else {
		mult_fn = crs_vect_mult;
	}

	fprintf(stdout, "Loaded crs_matrix\n");
	dump_crs_matrix(stdout, m);									//kyle made edit to this: 10-9-23


	/* prepare the original vector */
	if(!(v = make_col_ones(get_crs_matrix_size(m)))) {
		perror("make_col_ones()");
		return EXIT_FAILURE;
	}

	/* prepare the results vector */
	if(!(r = make_col_ones(get_crs_matrix_size(m)))) {
		perror("make_col_ones()");
		return EXIT_FAILURE;
	}

	/* perform y = A^n x */
	time_start = time_function();
	for(int i = 0; i < 1000; i++) {
		t = mult_fn(m, v, r);
		r = v;
		v = t;
	}
	time_end = time_function();

	fprintf(stdout, "results:\n");
	//dump_vector(stdout, v);									//kyle made edit to this: 10-9-23

	fprintf(stdout, "computational time: %lu\n", time_end - time_start);

	destroy_crs_matrix(m);
	destroy_vector(v);
	destroy_vector(r);
	
	fclose(fptr);	// Kyle edit

	return EXIT_SUCCESS;
}
