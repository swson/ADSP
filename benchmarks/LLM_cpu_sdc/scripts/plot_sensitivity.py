from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

root = Path("results/phase3_c220g2/analysis")

df = pd.read_csv(
    root / "sensitivity_summary.csv"
)

df = df.dropna(
    subset=[
        "max_abs_error",
        "first_step_logits_max_error"
    ]
)

if df.empty:
    print("No valid experiment data available.")
    raise SystemExit(0)

plt.figure(figsize=(8, 5))

plt.scatter(
    df["max_abs_error"],
    df["first_step_logits_max_error"]
)

plt.xlabel("Maximum activation error")
plt.ylabel("Maximum first-step logit error")
plt.title("Activation Error vs Logit Error")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    root / "activation_vs_logits.png",
    dpi=200
)

plt.close()

plt.figure(figsize=(9, 5))

df["status"].value_counts().plot(
    kind="bar"
)

plt.ylabel("Number of experiments")
plt.title("Fault Propagation Outcomes")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig(
    root / "propagation_outcomes.png",
    dpi=200
)

plt.close()

print("Plots generated successfully.")
