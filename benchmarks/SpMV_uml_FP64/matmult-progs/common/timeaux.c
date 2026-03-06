#include <inttypes.h>
#include <time.h>

#include "timeaux.h"

uint64_t soft_timer(void) {
	struct timespec ts;
	clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ts);

	return ((uint64_t)ts.tv_sec) * 1000000000000UL + ts.tv_nsec;
}

#ifdef TESTCASE
#include <stdlib.h>

int main(void) {
	return EXIT_SUCCESS;
}
#endif
