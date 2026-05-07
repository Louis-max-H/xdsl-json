	.att_syntax
	.file	"LLVMDialectModule"
	.text
	.globl	main                            # -- Begin function main
	.prefalign	4, .Lfunc_end0, nop
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	pushq	%r14
	.cfi_def_cfa_offset 16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	pushq	%rax
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -24
	.cfi_offset %r14, -16
	movq	%rdi, %r14
	movl	$8, %edi
	callq	malloc@PLT
	movq	%rax, %rbx
	movq	%r14, (%rax)
	movl	$8, %edi
	callq	malloc@PLT
	movq	%rax, %r14
	movq	$0, (%rax)
	movl	$8, %edi
	callq	malloc@PLT
	movq	$0, (%rax)
	.p2align	4
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	movq	(%rax), %rcx
	cmpq	(%rbx), %rcx
	jge	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movq	(%rax), %rcx
	addq	%rcx, (%r14)
	incq	(%rax)
	jmp	.LBB0_1
.LBB0_3:
	movq	(%r14), %rax
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%r14
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
