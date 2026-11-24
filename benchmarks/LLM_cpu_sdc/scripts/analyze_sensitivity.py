import csv
import json
from pathlib import Path

import torch

from error_metrics import calculate_metrics

ROOT = Path("results/phase3_c220g2")
BASE = ROOT / "baseline"
EXPERIMENTS = ROOT / "fma_experiments"

base_activation = torch.load(
    BASE / "full_inference_baseline_down_proj.pt",
    map_location="cpu"
)

base_scores = torch.load(
    BASE / "full_inference_baseline_scores.pt",
    map_location="cpu"
)

with open(BASE / "full_inference_baseline.json") as f:
    base_info = json.load(f)

rows = []

for folder in sorted(EXPERIMENTS.iterdir()):

    if not folder.is_dir():
        continue

    activation_file = (
        folder / "full_inference_faulty_down_proj.pt"
    )

    scores_file = (
        folder / "full_inference_faulty_scores.pt"
    )

    json_file = (
        folder / "full_inference_faulty.json"
    )

    row = {"experiment": folder.name}

    if not all(
        p.exists()
        for p in [
            activation_file,
            scores_file,
            json_file
        ]
    ):
        row["status"] = "Incomplete artifacts"
        rows.append(row)
        continue

    try:
        activation = torch.load(
            activation_file,
            map_location="cpu"
        )

        scores = torch.load(
            scores_file,
            map_location="cpu"
        )

        with open(json_file) as f:
            info = json.load(f)

        metrics = calculate_metrics(
            base_activation,
            activation
        )

        row.update(metrics)

        row["baseline_answer"] = base_info["answer"]
        row["experiment_answer"] = info["answer"]

        row["answer_changed"] = (
            base_info["answer"] != info["answer"]
        )

        row["answer_correct"] = (
            info["answer"].strip() == "96"
        )

        row["tokens_changed"] = (
            base_info["generated_token_ids"]
            != info["generated_token_ids"]
        )

        row["baseline_steps"] = len(base_scores)
        row["experiment_steps"] = len(scores)

        row["generation_step_count_changed"] = (
            len(base_scores) != len(scores)
        )

        first_step_diff = (
            scores[0].double()
            - base_scores[0].double()
        ).abs()

        row["first_step_logits_max_error"] = (
            first_step_diff.max().item()
        )

        row["first_step_logits_mean_error"] = (
            first_step_diff.mean().item()
        )

        row["first_step_logits_changed"] = (
            torch.count_nonzero(
                first_step_diff
            ).item()
        )

        row["baseline_top_token"] = (
            base_scores[0].argmax().item()
        )

        row["experiment_top_token"] = (
            scores[0].argmax().item()
        )

        if metrics["nan_count"] or metrics["inf_count"]:
            row["status"] = "Non-finite activation"

        elif row["answer_changed"]:
            row["status"] = "Answer changed"

        elif row["tokens_changed"]:
            row["status"] = "Token sequence changed"

        elif row["first_step_logits_changed"] > 0:
            row["status"] = "Numerical propagation"

        elif metrics["changed_elements"] > 0:
            row["status"] = "Activation-only difference"

        else:
            row["status"] = "No observed difference"

    except Exception as exc:
        row["status"] = "Analysis error"
        row["error"] = str(exc)

    rows.append(row)

if not rows:
    print("No experiment folders found.")
    raise SystemExit(0)

columns = sorted({
    key
    for row in rows
    for key in row
})

output = ROOT / "analysis" / "sensitivity_summary.csv"
output.parent.mkdir(parents=True, exist_ok=True)

with open(output, "w", newline="") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=columns
    )

    writer.writeheader()
    writer.writerows(rows)

print(f"Analyzed {len(rows)} experiments")
print(f"Saved: {output}")

for row in rows:
    print(
        row["experiment"],
        row["status"]
    )
