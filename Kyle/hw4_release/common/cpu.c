#include <inttypes.h>
#include <stdlib.h>
#include <string.h>

#if defined(__i386__) || defined(__x86_64)
#include <x86intrin.h>
#endif

#include "cpu.h"

char cpu_name[48];

static uint32_t get_max_leaf(void);

const char* get_cpu_name(void) {
#	if defined(__i386__) || defined(__x86_64__)
	struct {
		uint32_t eax, ebx, ecx, edx;
	} __attribute__((packed)) cpuid;


	if(get_max_leaf() < 0x80000004) {
		return "unknown cpu name";
	}

	for(size_t i = 0; i < 48; i += 4) {
		__asm__(
					"cpuid"
				:
					"=a"(cpuid.eax),
					"=b"(cpuid.ebx),
					"=c"(cpuid.ecx),
					"=d"(cpuid.edx)
				:
					"a"(0x80000002 + (i >> 2))
				:
			);
		memcpy(&cpu_name[i<<2], &cpuid, sizeof(cpuid));
	}

	return cpu_name + strspn(cpu_name, " ");
#	else
	return "architecture identification not supported"
#	endif
}

int cpu_has_tsx(void) {
#	if defined(__i386__) || defined(__x86_64__)
	uint32_t ebx;
	__asm__(
				"cpuid"
			:
				"=b"(ebx)
			:
				"a"(0x7),
				"c"(0x0)
			:
				"edx"
		);

	return !!(ebx & (1 << 11));
#	else
	return 0;
#	endif
}

int cpu_has_rtdscp(void) {
#	if defined(__i386__) || defined(__x86_64__)
	uint32_t edx;
	if(get_max_leaf() < 0x80000001) {
		return 0;
	}
	__asm__(
				"cpuid"
			:
				"=d"(edx)
			:
				"a"(0x80000001)
			:
				"ebx",
				"ecx"
		);
	return !!(edx & (1 << 27));
#	else
	return 0;
#	endif
}

int cpu_has_rtdsc(void) {
#	if defined(__i386__) || defined(__x86_64__)
	uint32_t edx;
	__asm__(
				"cpuid"
			:
				"=d"(edx)
			:
				"a"(0x1)
			:
				"ebx",
				"ecx"
		);
	return !!(edx & (1 << 4));
#	else
	return 0;
#	endif
}

uint64_t rdtscp(void) {
	uint32_t unused;
	return __rdtscp(&unused);
}

uint64_t rdtsc(void) {
	uint32_t eax, edx;
	/* the rdtsc instruction is not serializing, we need a serializing
	 * instruction before it so that things do not execute out of order
	 */
	__asm__(
				"cpuid"		"\n"
				"rdtsc"
			:
				"=a"(eax),
				"=d"(edx)
			:
				"a"(0)
			:
				"rbx",
				"rcx"
		);
	return (((uint64_t)edx) << 32) | eax;
}

static uint32_t get_max_leaf(void) {
	uint32_t eax;
	__asm__(
					"cpuid"
				:
					"=a"(eax)
				:
					"a"(0x80000000)
				:
			);
	return eax;
}

#ifdef TESTCASE
#include <assert.h>
#include <stdio.h>

int main(void) {
	fprintf(stdout, "%s\n", get_cpu_name());
	fprintf(stdout, "CPU %ssupports rtdscp\n",
			cpu_has_rtdscp() ? "" : "does not "
		);
	fprintf(stdout, "CPU %ssupports rtdsc\n",
			cpu_has_rtdsc() ? "" : "does not "
		);
	fprintf(stdout, "CPU %ssupports TSX\n",
			cpu_has_tsx() ? "" : "does not "
		);

	return EXIT_SUCCESS;
}
#endif
