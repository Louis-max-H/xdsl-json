	.att_syntax
	.file	"LLVMDialectModule"
	.text
	.globl	main                            # -- Begin function main
	.prefalign	4, .Lfunc_end0, nop
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movl	$8, %edi
	callq	malloc@PLT
	movq	%rax, %rbx
	movq	$42, (%rax)
	movl	$42, %edi
	callq	print_int@PLT
	movq	(%rbx), %rbx
	addq	$8, %rbx
	movl	$8, %edi
	callq	malloc@PLT
	movq	%rbx, (%rax)
	movq	%rbx, %rdi
	callq	print_int@PLT
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
