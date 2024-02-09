#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include <getopt.h>

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

void usage(const char* s) {
	fprintf(stderr,
"usage: %s [--matrix file] [--help]"	"\n"
"usage: %s [-m file] [-h]"				"\n"
""										"\n"
"    -m, --matrix file   use file as input"	"\n"
"                        if not given stdin is used instead"	"\n"
"    -h, --help          show this help and exit"				"\n"
""										"\n"
""										"\n",
		s, s);
	/* compile time options */
	//fprintf(stderr, "compiled with: %s %s\n\n", CC, CFLAGS_ALL);

	/* link time options */
	//fprintf(stderr, "linked with: %s %s\n\n", LD, LDFLAGS_ALL);

	//fprintf(stderr, "compiler specs: %s\n", COMPILERSPEC);
}

int main(int argc, char** argv) {
	static const struct option long_opts[] = {
		{ "matrix",	required_argument, NULL, 'm' },
		{ "help", no_argument, NULL, 'h' },
		{ NULL,	0, NULL, 0 }
	};

	char cpu_name[49] = {0};

	FILE* data_in = NULL;
	struct crs_matrix* m;
	struct vector* v, * r, * t;
	struct vector* (*mult_fn)(const struct crs_matrix*,
			const struct vector*,
			struct vector*);
	uint64_t (*time_function)(void) = (uint64_t(*)(void))NULL;
	uint64_t time_start, time_end;
	int opt;

	while((opt = getopt_long(argc, argv, "m:h", long_opts, NULL)) >= 0) {
		//printf("%c\n", opt);
		switch(opt) {
			case 'm':
				if(data_in) {
					fprintf(stderr, "closing previous file\n");
					fclose(data_in);
				}
				data_in = fopen(optarg, "r");
				if(data_in) {
					fprintf(stderr, "openend file %s\n", optarg);
				} else {
					perror("fopen()");
				}
				break;
			case 'h':
				/* fallthrough */
			default:
				usage(argv[0]);
				return opt != 'h' ? EXIT_FAILURE : EXIT_SUCCESS;
		}
	}


	/* CPU identification */
	fprintf(stdout, "Running on CPU: %s\n", get_cpu_name(cpu_name));

	/* compile time options */
	//fprintf(stdout, "compiled with: %s %s\n", CC, CFLAGS_ALL);

	/* link time options */
	//fprintf(stdout, "linked with: %s %s\n", LD, LDFLAGS_ALL);
	//fprintf(stdout, "compiler specs: %s\n", COMPILERSPEC);

	/* check for non-serializing read */
	if(cpu_has_rtdsc()) {
		time_function = rdtsc;
		//fprintf(stdout, "CPU supports the RTDSC instruction.\n");
	} else if(!time_function) {
		fprintf(stdout, "CPU does not support the RTDSC instruction. "
						"Using software-based timing.\n");
  		time_function = soft_timer;
	}

	if(!data_in) {
		fprintf(stderr, "fin is NULL\n");
		data_in = stdin;
	} else {
		//fprintf(stderr, "fin is NOT NULL\n");
	}

	/* load the crs_matrix */
	if(!(m = load_crs_matrix(data_in))) {
		fprintf(stdout, "no matrix loaded\n");
		return EXIT_FAILURE;
	}

	if(data_in != stdin) {
		//fprintf(stdout, "fin is not stdin\n");
		fclose(data_in);
	}

	if(crs_is_symmetric(m)) {
		mult_fn = crs_symm_vect_mult;
	} else {
		mult_fn = crs_vect_mult;
	}

	//fprintf(stdout, "Loaded crs_matrix\n");

//	dump_crs_matrix(stdout, m);

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

	//fprintf(stdout, "results:\n");
	//dump_vector(stdout, v);

	fprintf(stdout, "computational time: %lu\n", time_end - time_start);

	fprintf(stdout,"\n");

	destroy_crs_matrix(m);
	destroy_vector(v);
	destroy_vector(r);

	return EXIT_SUCCESS;
}
