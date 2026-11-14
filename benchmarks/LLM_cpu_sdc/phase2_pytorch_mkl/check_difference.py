
import numpy as np

baseline = np.load("pytorch_gemm_poc/results/baseline.npy")
faulty = np.load("pytorch_gemm_poc/results/faulty.npy")

diff = faulty - baseline
changed = ~np.isclose(baseline, faulty, rtol=0, atol=1e-5)

print("Total elements:", baseline.size)
print("Changed elements:", np.count_nonzero(changed))
print("Maximum absolute difference:", np.max(np.abs(diff)))
print("Baseline finite:", np.isfinite(baseline).all())
print("Faulty finite:", np.isfinite(faulty).all())

indices = np.argwhere(changed)

for i, j in indices[:20]:
    print(
        f"C[{i},{j}]: "
        f"{baseline[i,j]:.6f} -> "
        f"{faulty[i,j]:.6f}, "
        f"diff={diff[i,j]:.6f}"
    )
