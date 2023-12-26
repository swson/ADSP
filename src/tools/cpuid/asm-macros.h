#ifndef ASM_MACROS_H__
#define ASM_MACROS_H__

#ifdef __ASSEMBLER__

.macro declfn fn
	.section .text.\fn
	.globl \fn
	.type \fn, %function
\fn:
.endm

.macro endf fn
	.size \fn, . - \fn
.endm

#endif

#endif	/* ASM_MACROS_H__ */
