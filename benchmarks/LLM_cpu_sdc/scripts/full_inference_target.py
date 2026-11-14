
"""Full Llama greedy generation with a GDB-gated native FMA injection point.

Run baseline: python scripts/full_inference_target.py baseline
Run under GDB: INJECT_FMA=1 python scripts/full_inference_target.py faulty

On 'faulty', SIGUSR1 marks entry into layer-0 mlp.down_proj on its first
invocation. GDB must intercept and suppress the signal. Never run 'faulty'
without configuring GDB: an unhandled SIGUSR1 terminates the process.
"""
import json
import os
import signal
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"
PROMPT = "What is 12 multiplied by 8? Answer with only the number."
RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)

if len(sys.argv) != 2 or sys.argv[1] not in ("baseline", "faulty"):
    raise SystemExit("Usage: python scripts/full_inference_target.py baseline|faulty")
mode = sys.argv[1]
if mode == "faulty" and os.environ.get("INJECT_FMA") != "1":
    raise SystemExit("faulty mode requires INJECT_FMA=1 and a GDB SIGUSR1 handler")

torch.manual_seed(42)
torch.set_num_threads(1)
torch.set_num_interop_threads(1)

print("Loading tokenizer and model...", flush=True)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, torch_dtype=torch.float32
).to("cpu").eval()

inputs = tokenizer.apply_chat_template(
    [{"role": "user", "content": PROMPT}],
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
)

projection = model.model.layers[0].mlp.down_proj
state = {"calls": 0, "first_shape": None, "first_output": None}

def pre_hook(module, args):
    state["calls"] += 1
    if state["calls"] == 1:
        state["first_shape"] = list(args[0].shape)
        print("[MARKER] layer0 down_proj first invocation, shape:",
              state["first_shape"], flush=True)
        if mode == "faulty":
            print("[MARKER] raising SIGUSR1; GDB must suppress delivery", flush=True)
            signal.raise_signal(signal.SIGUSR1)

def post_hook(module, args, output):
    if state["calls"] == 1 and state["first_output"] is None:
        state["first_output"] = output.detach().cpu().clone()

pre_handle = projection.register_forward_pre_hook(pre_hook)
post_handle = projection.register_forward_hook(post_hook)

with torch.inference_mode():
    generated = model.generate(
        **inputs,
        max_new_tokens=20,
        do_sample=False,
        use_cache=True,
        pad_token_id=tokenizer.eos_token_id,
        return_dict_in_generate=True,
        output_scores=True,
    )
pre_handle.remove()
post_handle.remove()

input_len = inputs["input_ids"].shape[-1]
new_ids = generated.sequences[0, input_len:].tolist()
answer = tokenizer.decode(new_ids, skip_special_tokens=True)
scores = [s.detach().cpu().float().clone() for s in generated.scores]

assert state["first_output"] is not None, "down_proj hook never captured output"
assert all(torch.isfinite(x).all().item() for x in scores), "Non-finite generation scores"

result = {
    "mode": mode,
    "model": MODEL_ID,
    "prompt": PROMPT,
    "torch_version": torch.__version__,
    "transformers_version": __import__("transformers").__version__,
    "first_down_proj_input_shape": state["first_shape"],
    "first_down_proj_output_shape": list(state["first_output"].shape),
    "down_proj_call_count": state["calls"],
    "generated_token_ids": new_ids,
    "answer": answer,
    "first_step_top_token_id": int(scores[0].argmax(-1)[0]),
}
with (RESULTS / f"full_inference_{mode}.json").open("w") as f:
    json.dump(result, f, indent=2)
torch.save(state["first_output"], RESULTS / f"full_inference_{mode}_down_proj.pt")
torch.save(scores, RESULTS / f"full_inference_{mode}_scores.pt")

print("===== FULL INFERENCE =====", flush=True)
print("Mode:", mode, flush=True)
print("Answer:", repr(answer), flush=True)
print("Generated token IDs:", new_ids, flush=True)
print("Down-proj calls:", state["calls"], flush=True)
print("Saved output, scores, and JSON under results/", flush=True)

if mode == "faulty":
    ref_path = RESULTS / "full_inference_baseline_down_proj.pt"
    scores_path = RESULTS / "full_inference_baseline_scores.pt"
    if ref_path.exists():
        ref = torch.load(ref_path, map_location="cpu", weights_only=True)
        delta = (state["first_output"] - ref).abs()
        print("Down-proj max difference:", float(delta.max()), flush=True)
        print("Down-proj changed (>1e-5):", int((delta > 1e-5).sum()), flush=True)
    if scores_path.exists():
        baseline_scores = torch.load(scores_path, map_location="cpu", weights_only=True)
        for step, (base, faulty) in enumerate(zip(baseline_scores, scores)):
            print(f"Generation step {step}: logits max diff =",
                  float((faulty - base).abs().max()), flush=True)
