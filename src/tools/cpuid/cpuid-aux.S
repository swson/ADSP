#include "asm-macros.h"

#if defined(__ASSEMBLER__)

declfn get_cpuid
	pushq %rbx
	xorl %eax, %eax
	cpuid		/* trashes eax, ebx, ecx, edx */
	movl %ebx, (%rdi)
	movl %edx, 4(%rdi)
	movl %ecx, 8(%rdi)
	popq %rbx
	ret
endf get_cpuid

declfn get_max_extended
	pushq %rbx
	movl $0x80000000u, %eax
	cpuid
	popq %rbx
	ret
endf get_max_extended

declfn get_leaf
	pushq %rbx
	movl %edi, %eax
	cpuid
	movl %eax, (%rsi)
	movl %ebx, 4(%rsi)
	movl %ecx, 8(%rsi)
	movl %edx, 12(%rsi)
	popq %rbx
	ret
endf get_leaf

#endif

#if !defined(__ASSEMBLER__)
#include <stddef.h>

#include "cpuid-aux.h"

struct proc_info* get_processor_info(struct proc_info* p) {
	unsigned eax;
	__asm__ volatile (
			"cpuid"				"\n"
			: "=a"(eax) : "a"(1) : "ebx", "ecx", "edx"
		);


	p->stepping = eax & 0xf;
	p->model = (eax>>=4) & 0xf;
	p->family = (eax >>= 4) & 0xf;
	p->type = (eax >>=4) & 0x3;

	if(p->family == 15 || p->family == 6) {
		p->model += (eax & 0xf0);
	}

	if(p->family == 15) {
		p->family += (eax >> 8) & 0xff;
	}

	return p;
}

char* get_processor_name(char* buffer) {
	if(get_max_extended() < 0x80000003u) {
		return (char*)NULL;
	}

	for(unsigned i = 0; i < 3; i++) {
		get_leaf(0x80000002 + i, buffer + 16*i);
	}
	return buffer;
}

#if defined(TESTCASE)

#include <stdio.h>
#include <stdlib.h>

int main(void) {
	char buffer[13] = { 0 };
	char name[128] = { 0 };
	struct proc_info p;
	unsigned eax = get_cpuid(buffer);
	fprintf(stderr, "max base: %08x\n", eax);
	fprintf(stderr, "max extn: %08x\n", get_max_extended());
	fprintf(stderr, "CPUID: %s\n", buffer);
	get_processor_info(&p);
	fprintf(stderr, "%x %x %x %x\n", p.family, p.model, p.type, p.stepping);
	fprintf(stderr, "%s\n", get_processor_name(name));

	return EXIT_SUCCESS;
}


#endif	/* defined(TESTCASE) */

#endif	/* !defined(__ASSEMBLER__) */
