
import sys
import numpy as np
import torch

torch.manual_seed(42)
torch.set_num_threads(1)

N = 512

A = torch.randn(N, N, dtype=torch.float32)
B = torch.randn(N, N, dtype=torch.float32)

# Exactly one GEMM call; no warm-up.
C = torch.mm(A, B)

mode = sys.argv[1]
path = f"pytorch_gemm_poc/results/{mode}.npy"

np.save(path, C.numpy())

print("Mode:", mode)
print("Output shape:", C.shape)
print("Sample result:", C[0, 0].item())
print("Finite results:", torch.isfinite(C).all().item())
print("Saved:", path)
