#ifndef CPU_H__
#define CPU_H__

#include <inttypes.h>

const char* get_cpu_name(void);
int cpu_has_tsx(void);
int cpu_has_rtdscp(void);
int cpu_has_rtdsc(void);
uint64_t rdtscp(void);
uint64_t rdtsc(void);

#endif
