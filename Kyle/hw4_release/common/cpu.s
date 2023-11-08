	.file	"cpu.c"
	.comm	cpu_name,48,32
	.section	.rodata
.LC0:
	.string	"unknown cpu name"
.LC1:
	.string	" "
	.text
	.globl	get_cpu_name
	.type	get_cpu_name, @function
get_cpu_name:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset 3, -24
	movq	%fs:40, %rax
	movq	%rax, -24(%rbp)
	xorl	%eax, %eax
	call	get_max_leaf
	cmpl	$-2147483645, %eax
	ja	.L2
	leaq	.LC0(%rip), %rax
	jmp	.L6
.L2:
	movq	$0, -56(%rbp)
	jmp	.L4
.L5:
	movq	-56(%rbp), %rax
	shrq	$2, %rax
	movq	%rax, %rdx
	movl	$2147483650, %eax
	addq	%rdx, %rax
#APP
# 23 "cpu.c" 1
	cpuid
# 0 "" 2
#NO_APP
	movl	%ebx, %esi
	movl	%eax, -48(%rbp)
	movl	%esi, -44(%rbp)
	movl	%ecx, -40(%rbp)
	movl	%edx, -36(%rbp)
	movq	-56(%rbp), %rax
	leaq	0(,%rax,4), %rdx
	leaq	cpu_name(%rip), %rax
	leaq	(%rdx,%rax), %rcx
	movq	-48(%rbp), %rax
	movq	-40(%rbp), %rdx
	movq	%rax, (%rcx)
	movq	%rdx, 8(%rcx)
	addq	$4, -56(%rbp)
.L4:
	cmpq	$47, -56(%rbp)
	jbe	.L5
	leaq	.LC1(%rip), %rsi
	leaq	cpu_name(%rip), %rdi
	call	strspn@PLT
	movq	%rax, %rdx
	leaq	cpu_name(%rip), %rax
	addq	%rdx, %rax
.L6:
	movq	-24(%rbp), %rdi
	xorq	%fs:40, %rdi
	je	.L7
	call	__stack_chk_fail@PLT
.L7:
	addq	$56, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	get_cpu_name, .-get_cpu_name
	.globl	cpu_has_tsx
	.type	cpu_has_tsx, @function
cpu_has_tsx:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	.cfi_offset 3, -24
	movl	$7, %edx
	movl	$0, %ecx
	movl	%edx, %eax
	movl	%ebx, %edx
	movl	%edx, -12(%rbp)
	movl	-12(%rbp), %eax
	andl	$2048, %eax
	testl	%eax, %eax
	setne	%al
	movzbl	%al, %eax
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	cpu_has_tsx, .-cpu_has_tsx
