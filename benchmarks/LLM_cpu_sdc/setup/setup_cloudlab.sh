
#!/usr/bin/env bash
# CloudLab Ubuntu 22.04 / x86_64 bootstrap for ADSP Llama CPU SDC experiments.
# Run as your normal account with sudo access, not as root.
set -Eeuo pipefail

REPO_URL="${REPO_URL:-https://github.com/swson/ADSP.git}"
REPO_DIR="${REPO_DIR:-$HOME/ADSP}"
VENV_DIR="${VENV_DIR:-$HOME/llama-cpu-env}"
PROJECT_REL="benchmarks/LLM_cpu_sdc"
RUN_BASELINE=0
RUN_CAPTURE=0
ENABLE_PERF=1

usage() {
  cat <<'HELP'
Usage: bash setup_cloudlab.sh [--baseline] [--capture] [--skip-perf-sysctl]
  Default: install system utilities, clone/update ADSP main, recreate Python
           environment from saved lock, validate imports. No model download.
  --baseline: run the original full Llama baseline (downloads gated model if needed)
  --capture:  capture a NEW first-layer down_proj input/reference; implies --baseline
  --skip-perf-sysctl: do not change kernel.perf_event_paranoid

Environment overrides: REPO_DIR, REPO_URL, VENV_DIR
A fresh node needs Python 3.10, sudo rights, network access, and access to the
HF gated model meta-llama/Llama-3.2-1B-Instruct for inference.
HELP
}

for arg in "$@"; do
  case "$arg" in
    --baseline) RUN_BASELINE=1 ;;
    --capture) RUN_BASELINE=1; RUN_CAPTURE=1 ;;
    --skip-perf-sysctl) ENABLE_PERF=0 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; usage >&2; exit 2 ;;
  esac
done

log() { printf '\n[CloudLab bootstrap] %s\n' "$*"; }
fail() { printf '\n[ERROR] %s\n' "$*" >&2; exit 1; }
trap 'echo "[ERROR] Command failed near line $LINENO. Resolve before using this node for experiments." >&2' ERR

[[ "$(id -u)" != 0 ]] || fail "Run as your normal user, not root."
[[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || fail "Requires Linux x86_64."
command -v sudo >/dev/null || fail "sudo missing"
sudo -v

log "Installing only the required system tools (no kernel upgrade or reboot)"
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git gdb python3 python3-pip python3-venv python3-dev linux-tools-common

KERNEL="$(uname -r)"
if apt-cache show "linux-tools-$KERNEL" >/dev/null 2>&1; then
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "linux-tools-$KERNEL"
else
  echo "[WARN] No packaged perf tool matches running kernel $KERNEL; perf may be unavailable." >&2
fi

if [[ "$ENABLE_PERF" == 1 ]]; then
  # Temporary only; the running node's kernel setting is not part of Git/venv.
  sudo sysctl -w kernel.perf_event_paranoid=1 || \
    echo "[WARN] Could not enable perf for unprivileged users." >&2
fi

log "Retrieving ADSP main"
if [[ -d "$REPO_DIR/.git" ]]; then
  git -C "$REPO_DIR" status --short
  [[ -z "$(git -C "$REPO_DIR" status --porcelain)" ]] || \
    fail "Repository has uncommitted changes: $REPO_DIR. Commit/stash them first."
  [[ "$(git -C "$REPO_DIR" branch --show-current)" == main ]] || \
    fail "Existing checkout isn't on main. Switch it manually first."
  git -C "$REPO_DIR" pull --ff-only origin main
elif [[ -e "$REPO_DIR" ]]; then
  fail "$REPO_DIR exists but is not a Git repository. Set REPO_DIR to another location."
else
  git clone --branch main --single-branch "$REPO_URL" "$REPO_DIR"
fi

PROJECT="$REPO_DIR/$PROJECT_REL"
LOCK="$PROJECT/setup/requirements-lock.txt"
[[ -f "$LOCK" ]] || fail "Missing $LOCK. Confirm setup files are pushed to main."
[[ -f "$PROJECT/scripts/baseline_llama.py" ]] || fail "Missing baseline script."
[[ -f "$PROJECT/scripts/isolate_down_proj.py" ]] || fail "Missing isolated projection script."

command -v python3.10 >/dev/null || fail "Python 3.10 missing. Use a CloudLab Ubuntu 22.04 image."
log "Creating/reusing Python 3.10 venv at $VENV_DIR"
if [[ ! -f "$VENV_DIR/bin/python" ]]; then
  python3.10 -m venv "$VENV_DIR"
fi
VENV_PY="$VENV_DIR/bin/python"
[[ "$($VENV_PY -c 'import sys; print(sys.version_info[:2] == (3, 10))')" == True ]] || \
  fail "Existing venv uses wrong Python version: $VENV_DIR"

"$VENV_PY" -m pip install --upgrade pip

TORCH_PIN="$(grep -E '^torch==' "$LOCK" | head -1 || true)"
[[ -n "$TORCH_PIN" ]] || fail "Lock file does not pin torch."
log "Installing $TORCH_PIN from official PyTorch CPU wheel index"
"$VENV_PY" -m pip install --index-url https://download.pytorch.org/whl/cpu "$TORCH_PIN" || \
  fail "Unable to obtain pinned $TORCH_PIN. Check wheel availability/network; do not silently change torch."

# PyTorch is already installed exactly; other pinned packages are resolved on PyPI.
log "Installing remaining locked Python packages"
"$VENV_PY" -m pip install -r "$LOCK"
"$VENV_PY" -m pip check

log "Validating architecture, dependencies, and MKL"
"$VENV_PY" - <<'PY'
import sys
import torch
import transformers
import huggingface_hub
assert sys.version_info[:2] == (3, 10), sys.version
assert torch.__version__ == '2.14.1+cpu', torch.__version__
assert transformers.__version__ == '4.46.3', transformers.__version__
assert torch.backends.mkl.is_available(), 'PyTorch MKL backend unavailable'
assert not torch.cuda.is_available(), 'Expected CPU-only PyTorch wheel'
x = torch.randn(16, 16, dtype=torch.float32)
y = x @ x
assert torch.isfinite(y).all(), 'CPU matrix multiply failed'
print('Python:', sys.version.split()[0])
print('Torch:', torch.__version__)
print('Transformers:', transformers.__version__)
print('huggingface_hub:', huggingface_hub.__version__)
print('MKL available:', torch.backends.mkl.is_available())
print('CPU matmul: PASS')
PY

log "System profiler versions"
gdb --version | head -1
if command -v perf >/dev/null; then perf --version || true; else echo 'perf unavailable'; fi
printf 'Kernel: %s\n' "$KERNEL"
printf 'perf_event_paranoid: %s\n' "$(cat /proc/sys/kernel/perf_event_paranoid)"

cat <<EOF

=== Node preparation complete ===
Repository: $PROJECT
Virtual env: $VENV_DIR
To enter the environment:
  source "$VENV_DIR/bin/activate"
  cd "$PROJECT"
  export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 MKL_VERBOSE=0

For model access on this node, authenticate to Hugging Face using:
  hf auth login
(The model requires that your Hugging Face account has been approved.)

For a baseline check after HF authentication:
  python scripts/baseline_llama.py
For recapturing first-layer inputs on this machine:
  python scripts/isolate_down_proj.py capture
Then verify isolated projection:
  python scripts/isolate_down_proj.py target

Note: full-inference GDB fault targeting has NOT been automated by this script.
EOF

if [[ "$RUN_BASELINE" == 1 ]]; then
  log "Running full baseline inference (requires gated-model access)"
  (cd "$PROJECT" && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 MKL_VERBOSE=0 "$VENV_PY" scripts/baseline_llama.py)
fi
if [[ "$RUN_CAPTURE" == 1 ]]; then
  log "Capturing fresh down_proj tensors on this node"
  (cd "$PROJECT" && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 MKL_VERBOSE=0 "$VENV_PY" scripts/isolate_down_proj.py capture)
  (cd "$PROJECT" && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 MKL_VERBOSE=0 "$VENV_PY" scripts/isolate_down_proj.py target)
fi
