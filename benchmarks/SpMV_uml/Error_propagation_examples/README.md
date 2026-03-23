# matmult-iter.py

This script runs an error propagation experiment for the SpMV multiplication algorithm.

When `matmult-iter.py` is executed, it creates an output folder containing the following files:

- `mtx_orig`: he original matrix before corruption.
- `mtx_modif`: he modified matrix containing injected error(s).
- `pts_corrupt`: shows the error propagation over repeated executions
  (e.g., run with `--iterations 100`, this file records the error propagation over 100 runs)
- `seed`: the random seed number used for generating the corruption.

## Arguments

| Argument | Type | Default | Description |
|---|---:|---:|---|
| `--matrix-shape` | int | `400` | Matrix size |
| `--base-dir` | str | `.` | Base directory for generated output |
| `--iterations` | int | `100` | Number of iterations for propagation |
| `--sparsity` | int | `400` | Number of nonzero entries in the matrix |
| `--random-seed` | int | `None` | Random seed for reproducibility |
| `--bad-elements` | int | `1` | Number of elements to corrupt |
| `--save-history` | flag | `False` | Save propagation history |
| `--save-intermediate` | flag | `False` | Save intermediate results |
| `--corrupt-nonzero-only` | flag | `False` | Corrupt only nonzero elements |

For reference, in our experiments, `--matrix-shape 400 --sparsity 400` was used, meaning a `400 x 400` matrix with 400 nonzero elements, corresponding to a sparsity of `0.9975`.

## Example Command

```bash
python matmult-iter.py

