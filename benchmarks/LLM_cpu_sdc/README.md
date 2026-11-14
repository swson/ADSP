# LLM CPU FMA Fault Injection

Research objective: study propagation of software-emulated
floating-point arithmetic faults during LLM inference.

## Environment
- Model: meta-llama/Llama-3.2-1B-Instruct
- Execution: CPU, FP32
- CPU tested: Intel Xeon E5-2630 v3 (Haswell)
- Native BLAS: Intel MKL SGEMM
- Profiling: Linux perf
- Debugging and fault injection: GDB

## Completed
1. Verified deterministic Llama CPU baseline.
2. Captured layer 0 MLP down_proj input and reference.
3. Reproduced isolated FP32 down_proj output.
4. Identified active MKL kernels using perf.
5. Verified execution of native vfmadd231ps.
6. Injected +100 into one FP32 FMA result lane.

## First isolated injection result
- Kernel: mkl_blas_avx2_sgemm_kernel_nocopy_TN_b0
- FMA offset: +1133
- Destination: ymm4, lane 0
- Input shape: (1, 50, 8192)
- Output shape: (1, 50, 2048)
- Changed output elements: 1 / 102400
- Changed position: [0, 0, 0]
- Maximum absolute output difference: 99.99996185302734
- All outputs finite: True

This is a software-emulated arithmetic-result fault, not a
physical CPU hardware fault. End-to-end LLM output corruption
has not yet been established.

## Reproduction
See setup/requirements-lock.txt for Python dependencies.
See scripts/ for the baseline, capture, target, and profiling code.

The Hugging Face model must be downloaded separately using
an authorized Hugging Face account.

## Next
Integrate one controlled native FMA fault into a selected
down_proj invocation during full Llama inference, and compare
activations, logits, and generated tokens.
