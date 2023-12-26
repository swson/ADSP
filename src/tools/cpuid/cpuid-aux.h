#ifndef CPUID_AUX_H__
#define CPUID_AUX_H__


struct proc_info;

unsigned get_cpuid(char* buffer);
unsigned get_leaf(unsigned eax, char* buffer);
unsigned get_max_extended(void);
struct proc_info* get_processor_info(struct proc_info* p);
char* get_processor_name(char* buffer);

struct proc_info {
	unsigned char family;
	unsigned char model;
	unsigned char type;
	unsigned char stepping;
};

#endif	/* CPUID_AUX_H__ */
