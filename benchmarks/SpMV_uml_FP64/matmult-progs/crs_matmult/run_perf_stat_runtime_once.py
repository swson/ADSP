import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import math
import time  # add runtime measurement

# ======================
# CONFIGURATION
# ======================
input_dir = "input_2/494_bus_input"
output_dir = "time_494_bus"
os.makedirs(output_dir, exist_ok=True)

normal_matrix = os.path.join(input_dir, "494_bus.mtx.crs")
error_matrix = os.path.join(input_dir, "494_bus_point_gauss_0.20_0.05.mtx.crs")

event_name_arr = [
    "inst_retired.any",
    "branch-loads",
    "br_inst_retired.not_taken",
    "br_inst_retired.conditional",
]

num_runs = 1000  # adjust to 100 for full experiment

# ======================
# PERF STAT FUNCTION
# ======================
def run_perf_stat_json(matrix_file, label, run_idx, event_name_arr):
    """
    Run perf stat -j -o (JSON output) and measure elapsed time
    (perf + ./crs_matmult total runtime)
    """
    event_str = ",".join(event_name_arr)
    json_path = os.path.join(output_dir, f"perf_{label}_run_{run_idx:03d}.json")

    perf_cmd = [
        "sudo", "perf", "stat",
        "-j", "-o", json_path,
        "-e", event_str,
        "./crs_matmult", "--matrix", matrix_file
    ]

    print(f"[INFO] Running {label} matrix (run {run_idx})...")

    t0 = time.perf_counter()
    subprocess.run(perf_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    t1 = time.perf_counter()
    elapsed = t1 - t0  # perf+crs_matmult time for this run

    print(f"  → Saved JSON: {json_path}, elapsed = {elapsed:.6f} s")
    return json_path, elapsed

# ======================
# PARSER USING PANDAS
# ======================
def json_to_dataframe(json_path):
    """Read perf JSON (newline-delimited) and return pandas DataFrame"""
    df = pd.read_json(json_path, lines=True)
    # extracting the necessary columns
    df = df[["event", "counter-value", "unit"]].dropna()
    df = df[df["event"].notnull()]
    df = df.rename(columns={"counter-value": "count"})
    return df

def aggregate_events(df, event_name_arr):
    """Return dictionary of event: count pairs"""
    result = {}
    for ev in event_name_arr:
        matched = df[df["event"] == ev]
        result[ev] = matched["count"].sum() if not matched.empty else 0
    return result

# ======================
# MAIN EXECUTION
# ======================
results_normal = []
results_error = []
normal_times = []  # save runtime by run (normal)
error_times = []   # save runtime by run (error)

# Normal runs
for i in range(1, num_runs + 1):
    json_n, t_n = run_perf_stat_json(normal_matrix, "normal", i, event_name_arr)
    df_n = json_to_dataframe(json_n)
    results_normal.append(aggregate_events(df_n, event_name_arr))
    normal_times.append(t_n)

# Error runs
for i in range(1, num_runs + 1):
    json_e, t_e = run_perf_stat_json(error_matrix, "error", i, event_name_arr)
    df_e = json_to_dataframe(json_e)
    results_error.append(aggregate_events(df_e, event_name_arr))
    error_times.append(t_e)

# ======================
# SAVE TO CSV (pandas)
# ======================
df_normal = pd.DataFrame(results_normal)
df_error = pd.DataFrame(results_error)

# add run number and runtime columns
df_normal.insert(0, "run", range(1, num_runs + 1))
df_normal.insert(1, "runtime_sec", normal_times)   # add runtime col 

df_error.insert(0, "run", range(1, num_runs + 1))
df_error.insert(1, "runtime_sec", error_times)     # add runtime col 

csv_normal = os.path.join(output_dir, "perf_normal_summary_.csv")
csv_error = os.path.join(output_dir, "perf_error_summary_.csv")

df_normal.to_csv(csv_normal, index=False)
df_error.to_csv(csv_error, index=False)

print(f"\n CSV saved:\n  Normal → {csv_normal}\n  Error  → {csv_error}")

# ======================
# PLOTTING: trend plot 
# ======================

plots_per_page = 4
num_pages = math.ceil(len(event_name_arr) / plots_per_page)

for page in range(num_pages):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()

    start_idx = page * plots_per_page
    end_idx = min(start_idx + plots_per_page, len(event_name_arr))
    current_events = event_name_arr[start_idx:end_idx]

    for idx, ev in enumerate(current_events):
        y_normal = df_normal[ev].tolist()
        y_error = df_error[ev].tolist()
        x = list(range(1, num_runs * 2 + 1))
        y_combined = y_normal + y_error
        split_index = len(y_normal)

        axes[idx].plot(x, y_combined, marker='o', color='steelblue', linestyle='-')
        axes[idx].axvline(split_index + 0.5, color='gray', linestyle='--', alpha=0.6)
        axes[idx].set_title(ev)
        axes[idx].set_xlabel("Run # (Normal → Error)")
        axes[idx].set_ylabel("Event Count")
        axes[idx].grid(True, linestyle=':')

    for j in range(len(current_events), plots_per_page):
        fig.delaxes(axes[j])

    plt.suptitle("Perf Stat Event Counts (pandas JSON-based: Normal → Error)", fontsize=14)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, f"perf_stat_plot_page{page+1}.png")
    plt.savefig(plot_path)
    plt.close()

# ======================
# HISTOGRAM PLOTTING: 
# ======================
plots_per_page = 4
num_pages = math.ceil(len(event_name_arr) / plots_per_page)

for page in range(num_pages):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.flatten()
    start_idx = page * plots_per_page
    end_idx = min(start_idx + plots_per_page, len(event_name_arr))
    current_events = event_name_arr[start_idx:end_idx]

    for idx, ev in enumerate(current_events):
        n_vals = df_normal[ev]
        e_vals = df_error[ev]

        axes[idx].hist(n_vals, bins=30, alpha=0.6, color="steelblue", label="Normal", density=True)
        axes[idx].hist(e_vals, bins=30, alpha=0.6, color="tomato", label="Error", density=True)
        axes[idx].set_title(ev)
        axes[idx].set_xlabel("Event Count")
        axes[idx].set_ylabel("Density")
        axes[idx].legend()
        axes[idx].grid(True, linestyle=':')

    plt.suptitle("Perf Stat Histogram (Normal vs Error, runs)", fontsize=15)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, f"perf_stat_histogram_page{page+1}.png")
    plt.savefig(plot_path)
    plt.close()

print("\n All trend + histogram (event counts) plots generated successfully")

# ======================
# HISTOGRAM PLOTTING: add runtime histogram (Normal vs Error)
# ======================
plt.figure(figsize=(8, 6))
plt.hist(normal_times, bins=30, alpha=0.6, color="steelblue", label="Normal runtime", density=True)
plt.hist(error_times, bins=30, alpha=0.6, color="tomato", label="Error runtime", density=True)
plt.xlabel("Elapsed time (seconds)")
plt.ylabel("Density")
plt.title("Runtime Histogram (perf + crs_matmult): Normal vs Error")
plt.legend()
plt.grid(True, linestyle=':')

runtime_hist_path = os.path.join(output_dir, "runtime_histogram_normal_vs_error.png")
plt.tight_layout()
plt.savefig(runtime_hist_path)
plt.close()

print(f" Runtime histogram saved: {runtime_hist_path}")
