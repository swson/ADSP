import torch
import time

torch.manual_seed(42)
torch.set_num_threads(1)

N = 512
A = torch.randn(N, N, dtype=torch.float32)
B = torch.randn(N, N, dtype=torch.float32)

for _ in range(5):
    C = torch.mm(A, B)

start = time.perf_counter()
C = torch.mm(A, B)
elapsed = time.perf_counter() - start

print("PyTorch:", torch.__version__)
print("Matrix size:", A.shape)
print("Output shape:", C.shape)
print("Sample result:", C[0, 0].item())
print("Execution time:", round(elapsed * 1000, 3), "ms")
print("Finite results:", torch.isfinite(C).all().item())
