#include <stdlib.h>

#include "tjds_matrix.h"

struct tjds_matrix {
	long double* value_list;
	size_t* row_indexes;
	size_t* start_position;
	size_t* perm_array;
	size_t value_list_len;
	size_t start_position_len;
	size_t perm_array_len;
	size_t jagged_diagonals;
	size_t number_cols;
	char type;
};

enum tjds_input_states {
	MATRIX_TYPE = 0,
	MATRIX_GET_COLS,
	MATRIX_VALUE_LIST_LEN,
	NUMBER_JAGGED_DIAGS,
	POS_ARRAY_LEN,
	PERM_ARRAY_LEN,
	DATA_VALUES,
	DATA_ROWS,
	DATA_PERM_LIST,
	DATA_START_POS
};

struct tjds_matrix* load_tjds_matrix(FILE* stream) {
	struct tjds_matrix* ret;
	char* read_data = (char*)NULL;

	size_t counter = 0;
	enum tjds_input_states state = MATRIX_TYPE;

	if(!(ret = (struct tjds_matrix*)malloc(sizeof(*ret)))) {
		return (struct tjds_matrix*)NULL;
	}


	/* expected format:
	 *  - first line is the type of matrix
	 *	- second line is the number of non-zero elements
	 *	- third line is the number of elements in the position array
	 *  - fourth line is the number of jagged diagonals
	 *	- rest of input is data for the matrix:
	 *		- first the numbers for the matrix
	 *		- then the row index for each number
	 * 		- then the permutation
	 *		- then the start position
	 */
	while(fscanf(stream, "%ms", &read_data) != EOF) {
		switch(state) {
			long double d;
			size_t t;
			char c;
			case MATRIX_TYPE:
				/* first line is the type */
				if(sscanf(read_data, "%c", &c) == EOF) {
					fprintf(stderr, "can not match character\n");
					goto err_no_value;
				}
				if(c != 'g' && c != 's') {
					fprintf(stderr, "invalid matrix type: %c\n", c);
					goto err_no_value;
				}
				ret->type = c;
				state = MATRIX_GET_COLS;
				break;

			case MATRIX_GET_COLS:
				if(sscanf(read_data, "%zd", &t) == EOF) {
					goto err_no_value;
				}
				ret->number_cols = t;
				state = MATRIX_VALUE_LIST_LEN;
				break;

			case MATRIX_VALUE_LIST_LEN:
				/* second line is the number of non-zero elements */
				if(sscanf(read_data, "%zd", &(ret->value_list_len)) == EOF) {
					fprintf(stderr, "failed to get value_list_len\n");
					goto err_no_value;
				}
				ret->value_list =
						(long double*)malloc(sizeof(long double) * ret->value_list_len);
				if(!(ret->value_list)) {
					goto err_no_value;
				}
				ret->row_indexes =
						(size_t*)malloc(sizeof(size_t) * ret->value_list_len);
				if(!(ret->row_indexes)) {
					goto err_no_row_index;
				}
				state = NUMBER_JAGGED_DIAGS;
				break;

			case NUMBER_JAGGED_DIAGS:
				if(sscanf(read_data, "%zd", &t) == EOF) {
					goto err_no_pos_array;
				}
				ret->jagged_diagonals = t;
	
				state = POS_ARRAY_LEN;
				break;
				
			case POS_ARRAY_LEN:
				/* third line is the number of elements in position array */
				if(sscanf(read_data, "%zd", &t) == EOF) {
					goto err_no_pos_array;
				}

				ret->start_position_len = t;
				ret->start_position =
						(size_t*)malloc(t * sizeof(*(ret->start_position)));
				if(!(ret->start_position)) {
					goto err_no_pos_array;
				}

				state = PERM_ARRAY_LEN; 
				break;

			case PERM_ARRAY_LEN:
				/* fourth line is the numbr of jagged diagonals */
				if(sscanf(read_data, "%zd", &t) == EOF) {
					goto err_no_jagged_diagonal;
				}

				ret->perm_array_len = t;
				ret->perm_array =
						(size_t*)malloc(t * sizeof(*(ret->perm_array)));
				if(!(ret->perm_array)) {
					goto err_no_jagged_diagonal;
				}
				
				state = DATA_VALUES;
				break;

			case DATA_VALUES:
				/* matrix data: first data values */
				if(sscanf(read_data, "%Lf", &d) == EOF) {
					goto err_parse;
				}
				ret->value_list[counter++] = d;
				if(counter == ret->value_list_len) {
					counter = 0;
					state = DATA_ROWS;
				}
				break;
			case DATA_ROWS:
				if(sscanf(read_data, "%zd", &t) == EOF) {
					goto err_parse;
				}
				ret->row_indexes[counter++] = t;
				if(counter == ret->value_list_len) {
					counter = 0;
					state = DATA_PERM_LIST;
				}
				break;
			case DATA_PERM_LIST:
				if(sscanf(read_data, "%zd", &t) == EOF) {
					goto err_parse;
				}
				ret->perm_array[counter++] = t;
				if(counter == ret->perm_array_len) {
					counter = 0;
					state = DATA_START_POS;
				}
				break;
			case DATA_START_POS:
				if(sscanf(read_data, "%zd", &t) == EOF) {
					goto err_parse;
				}
				ret->start_position[counter++] = t;
				if(counter == ret->start_position_len) {
					/* done */
				}
				break;
		}
		free(read_data);
	}

	return ret;

err_parse:
	free(ret->perm_array);
err_no_jagged_diagonal:
	free(ret->start_position);
err_no_pos_array:
	free(ret->row_indexes);
err_no_row_index:
	free(ret->value_list);
err_no_value:
	free(ret);
	free(read_data);
	return (struct tjds_matrix*)NULL;

}

void dump_tjds_matrix(FILE* stream, const struct tjds_matrix* m) {
	fprintf(stream,
			"TJDS Matrix (%c)\njagged diags: %zd\nvalue_list: ",
			m->type, m->jagged_diagonals);
	for(size_t i = 0; i < m->value_list_len; i++) {
		fprintf(stream, "%Lf ", m->value_list[i]);
	}

	fprintf(stream, "\nrow_indexes: ");
	for(size_t i = 0; i < m->value_list_len; i++) {
		fprintf(stream, "%zd ", m->row_indexes[i]);
	}

	fprintf(stream, "\nstart_position: ");
	for(size_t i = 0; i < m->start_position_len; i++) {
		fprintf(stream, "%zd ", m->start_position[i]);
	}

	fprintf(stream, "\nperm_array: ");
	for(size_t i = 0; i < m->perm_array_len; i++) {
		fprintf(stream, "%zd ", m->perm_array[i]);
	}

	fprintf(stream, "\n");

}

struct tjds_matrix* destroy_tjds_matrix(struct tjds_matrix* m) {
	free(m->value_list);
	free(m->row_indexes);
	free(m->start_position);
	free(m->perm_array);
	free(m);
	return (struct tjds_matrix*)NULL;
}

const long double* get_tjds_matrix_val_array(const struct tjds_matrix* m) {
	return m->value_list;
}

const size_t* get_tjds_permutation_array(const struct tjds_matrix* m) {
	return m->perm_array;
}

size_t get_tjds_perm_len(const struct tjds_matrix* m) {
	return m->perm_array_len;
}

const size_t* get_tjds_matrix_start_pos_array(const struct tjds_matrix* m) {
	return m->start_position;
}

const size_t* get_tjds_matrix_row_array(const struct tjds_matrix* m) {
	return m->row_indexes;
}

size_t get_jagged_diagonals(const struct tjds_matrix* m) {
	return m->jagged_diagonals;
}

int tjds_is_symmetric(const struct tjds_matrix* m) {
	return m->type == 's';
}

size_t get_tjds_matrix_size(const struct tjds_matrix* m) {
	return m->number_cols;
}

#ifdef TESTCASE
#include <assert.h>

int main(void) {
	struct tjds_matrix* m;
	m = load_tjds_matrix(stdin);
	assert(m != NULL);
	dump_tjds_matrix(stdout, m);
	m = destroy_tjds_matrix(m);

	return EXIT_SUCCESS;
}
#endif
