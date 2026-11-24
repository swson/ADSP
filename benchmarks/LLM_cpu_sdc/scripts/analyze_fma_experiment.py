import argparse
import json
from pathlib import Path

import torch

parser = argparse.ArgumentParser()
parser.add_argument("--reference", required=True)
parser.add_argument("--experiment", required=True)
args = parser.parse_args()

reference = Path(args.reference)
experiment = Path(args.experiment)

base = torch.load(
    reference / "full_inference_baseline_down_proj.pt",
    map_location="cpu"
)

test = torch.load(
    experiment / "full_inference_faulty_down_proj.pt",
    map_location="cpu"
)

assert base.shape == test.shape

diff = (test - base).abs()

print("\n===== ACTIVATION ANALYSIS =====")
print("Shape:", list(base.shape))
print("Total elements:", base.numel())
print("Exactly equal:", torch.equal(base, test))
print("Changed elements:", torch.count_nonzero(diff).item())
print("Changed (>1e-5):", (diff > 1e-5).sum().item())
print("Maximum difference:", diff.max().item())
print("Mean difference:", diff.mean().item())
print("Baseline finite:", torch.isfinite(base).all().item())
print("Experiment finite:", torch.isfinite(test).all().item())

base_scores = torch.load(
    reference / "full_inference_baseline_scores.pt",
    map_location="cpu"
)

test_scores = torch.load(
    experiment / "full_inference_faulty_scores.pt",
    map_location="cpu"
)

print("\n===== LOGITS ANALYSIS =====")
print("Baseline steps:", len(base_scores))
print("Experiment steps:", len(test_scores))

for i, (b, t) in enumerate(zip(base_scores, test_scores)):
    d = (t - b).abs()

    print(f"\nGeneration step {i}")
    print("Maximum difference:", d.max().item())
    print("Mean difference:", d.mean().item())
    print("Changed elements:", torch.count_nonzero(d).item())
    print("Baseline top token:", b.argmax(dim=-1).tolist())
    print("Experiment top token:", t.argmax(dim=-1).tolist())

print("\n===== INFERENCE RESULTS =====")

with open(reference / "full_inference_baseline.json") as f:
    print("Baseline:", json.load(f))

with open(experiment / "full_inference_faulty.json") as f:
    print("Experiment:", json.load(f))
