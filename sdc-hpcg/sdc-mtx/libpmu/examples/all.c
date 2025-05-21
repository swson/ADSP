#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/random.h>

#include "skylake.h"

#define N (1 << 10)
#define BUF (sizeof(int) * N * N)

void do_work(int *a, int *b, int *c) {
  for (int i = 0; i < N; ++i)
    for (int j = 0; j < N; ++j)
      ((volatile int *)c)[i * N + j] = a[i * N + j] * b[i * N + j];
}

int main() {
  struct pmu_ctx p;
  uint64_t cntrs[7]; /* 3 fixed + 4 variable */
  int *a, *b, *c, ret;

  a = (int *)malloc(BUF);
  b = (int *)malloc(BUF);
  c = (int *)malloc(BUF);

  if (getrandom(a, BUF, GRND_RANDOM) < 0)
    return errno;

  if (getrandom(b, BUF, GRND_RANDOM) < 0)
    return errno;

  if ((ret = pmu_init(&p)))
    return ret;

  TRACE_ALL_CORE("core.txt", &p, do_work, a, b, c);
  TRACE_ALL_UNCORE("uncore.txt", &p, do_work, a, b, c);

  free(a);
  free(b);
  free(c);
  return pmu_exit(&p);
}
