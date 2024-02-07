#include <stdlib.h>

#include "crs_matrix.h"

struct crs_matrix {
	long double* a;
	size_t* ia;
	size_t* ja;
	size_t data_len;
	size_t rows;
	char type;
};

enum input_states {
	MATRIX_TYPE = 0,
	VALUE_LIST_LEN,
	ROW_LIST_LEN,
	DATA_NUMBER,
	DATA_COLS,
	DATA_ROWS
};

struct crs_matrix* load_crs_matrix(FILE* stream) {
	struct crs_matrix* ret;
	char* read_data = (char*)NULL;

	size_t counter = 0;
	enum input_states state = MATRIX_TYPE;

	if(!(ret = (struct crs_matrix*)calloc(1, sizeof(*ret)))) {
		return (struct crs_matrix*)NULL;
	}

	while(fscanf(stream, "%ms", &read_data) != EOF) {
		switch(state) {
			long double d;
			size_t t;
			char c;
			case MATRIX_TYPE:
				if(sscanf(read_data, "%c", &c) == EOF) {
					goto err_no_a;
				}
				if(!(c == 's' || c == 'g')) {
					goto err_no_a;
				}
				ret->type = c;
				state = VALUE_LIST_LEN;
				break;
			case VALUE_LIST_LEN:
				if(sscanf(read_data, "%zd", &(ret->data_len)) == EOF) {
					goto err_no_a;
				}
				ret->a =
					(long double*)calloc(ret->data_len, sizeof(long double));
				if(!(ret->a)) {
					goto err_no_a;
				}
				ret->ja = (size_t*)calloc(ret->data_len, sizeof(size_t));
				if(!(ret->ja)) {
					goto err_no_ja;
				}
				state = ROW_LIST_LEN;
				break;
			case ROW_LIST_LEN:
				if(sscanf(read_data, "%zd", &(ret->rows)) == EOF) {
					goto err_no_ja;
				}
				ret->ia =
					(size_t*)calloc(ret->rows, sizeof(size_t));
				if(!(ret->ia)) {
					goto err_no_ia;
				}
				state = DATA_NUMBER;
				break;
			case DATA_NUMBER:
				if(sscanf(read_data, "%Lf", &d) == EOF) {
					goto err_parse;
				}
				ret->a[counter++] = d;
				if(counter == ret->data_len) {
					counter = 0;
					state = DATA_COLS;
				}
				break;
			case DATA_COLS:
			case DATA_ROWS:
				if(sscanf(read_data, "%zd", &t) == EOF) {
					goto err_parse;
				}
				if(counter == ret->rows && state == DATA_ROWS) {
					goto err_parse;
				}
				((state == DATA_COLS) ? ret->ja : ret->ia)[counter++] = t;
				if(counter == ret->data_len && state == DATA_COLS) {
					counter = 0;
					state = DATA_ROWS;
				}
		}
		free(read_data);
	}

	if(!ret->data_len || !ret->ja || !ret->ia) {
		goto err_no_mtx;
	}

	return ret;

err_parse:
	free(ret->ja);
err_no_ja:
	free(ret->ia);
err_no_ia:
	free(ret->a);
err_no_a:
	free(read_data);
err_no_mtx:
	free(ret);
	return (struct crs_matrix*)NULL;

}

void dump_crs_matrix(FILE* stream, struct crs_matrix* m) {
	fprintf(stream, "CRS Matrix: (%c)\n", m->type);
	fprintf(stream, "a: ");
	for(size_t i = 0; i < m->data_len; i++) {
		fprintf(stream, "%Lf ", m->a[i]);
	}
	fprintf(stream, "\nia: ");

	for(size_t i = 0; i < m->rows; i++) {
		fprintf(stream, "%zd ", m->ia[i]);
	}
	
	fprintf(stream, "\nja: ");
	for(size_t i = 0; i < m->data_len; i++) {
		fprintf(stream, "%zd ", m->ja[i]);
	}

	fprintf(stream, "\n");
}

struct crs_matrix* destroy_crs_matrix(struct crs_matrix* m) {
	free(m->a);
	free(m->ia);
	free(m->ja);
	free(m);

	return (struct crs_matrix*)NULL;
}

const long double* get_crs_matrix_val_array(const struct crs_matrix* m) {
	return m->a;
}

const size_t* get_crs_matrix_column_array(const struct crs_matrix* m) {
	return m->ja;
}

const size_t* get_crs_matrix_row_array(const struct crs_matrix* m) {
	return m->ia;
}

size_t get_crs_matrix_size(const struct crs_matrix* m) {
	return m->rows - 1;
}

size_t get_crs_matrix_row_arr_len(const struct crs_matrix* m) {
	return m->rows;
}

size_t get_crs_matrix_nz_elements(const struct crs_matrix* m) {
	return m->data_len;
}

int crs_is_symmetric(const struct crs_matrix* m) {
	return m->type == 's';
}

#ifdef TESTCASE
#include <assert.h>

int main(void) {
	struct crs_matrix* m = load_crs_matrix(stdin);
	assert(m != NULL);
	dump_crs_matrix(stdout, m);
	destroy_crs_matrix(m);
}
#endif
