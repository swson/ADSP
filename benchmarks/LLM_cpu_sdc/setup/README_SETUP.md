
# Fresh CloudLab node: ADSP Llama CPU SDC

Tested source configuration: Ubuntu 22.04, Python 3.10, Intel Haswell CPU,
`torch==2.14.1+cpu`, `transformers==4.46.3`.

## Add these files to ADSP

Copy `setup_cloudlab.sh` to `benchmarks/LLM_cpu_sdc/setup/` and
`full_inference_target.py` to `benchmarks/LLM_cpu_sdc/scripts/`.
Commit both on `main` after reviewing them.

## Fresh node

```bash
sudo apt-get update && sudo apt-get install -y git

git clone https://github.com/swson/ADSP.git ~/ADSP
bash ~/ADSP/benchmarks/LLM_cpu_sdc/setup/setup_cloudlab.sh
source ~/llama-cpu-env/bin/activate
cd ~/ADSP/benchmarks/LLM_cpu_sdc
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 MKL_VERBOSE=0
hf auth login
python scripts/full_inference_target.py baseline
```

### Confirm model and native library

Run `python scripts/isolate_down_proj.py target` to verify saved fixtures.
On a CPU with a different MKL dispatch, rerun perf before selecting an
instruction. Symbol offsets are not portable across library builds.

## Full inference under GDB (manual, first execution)

```bash
INJECT_FMA=1 gdb -q --args python scripts/full_inference_target.py faulty
```

Inside GDB:

```gdb
set pagination off
set disassembly-flavor intel
handle SIGUSR1 stop print nopass
catch load libtorch_cpu.so
run
```

At library load:

```gdb
break *('mkl_blas_avx2_sgemm_kernel_nocopy_TN_b0'+1133)
disable 2
continue
```

**Check `info breakpoints` before using `disable 2`:** the FMA breakpoint
number depends on what breakpoints exist. The expression uses the known
kernel offset from the prior Haswell node, which MUST be reverified if the
CPU, MKL, or PyTorch build differs.

When `SIGUSR1` stops within the first `layer0.mlp.down_proj` pre-hook:

```gdb
info breakpoints
enable 2
continue
```

At the FMA breakpoint, verify `x/i $pc` prints `vfmadd231ps ymm4,ymm2,ymm0`.
If not, stop. If yes:

```gdb
stepi
set $original = $ymm4.v8_float[0]
set $ymm4.v8_float[0] = $original + 100.0
p $ymm4.v8_float[0]
disable 2
continue
```

Here again breakpoint `2` is just an example. Once the fault run completes,
compare `results/full_inference_baseline.json` to
`results/full_inference_faulty.json`, and examine the saved tensors/scores.

WARNING: `faulty` mode intentionally raises SIGUSR1 as a debug marker.
Running it outside configured GDB will terminate the process.
The marker gates the first projection invocation; confirm GDB stopped at it
and that the FMA breakpoint is reached in the expected call stack.

This is software-emulated register-result injection, not a physical fault.
