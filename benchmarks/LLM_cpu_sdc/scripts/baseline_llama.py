import json
from pathlib import Path

import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"
OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)

torch.manual_seed(42)
torch.set_num_threads(4)
torch.set_num_interop_threads(1)

print("PyTorch:", torch.__version__)
print("Transformers:", transformers.__version__)
print("CPU threads:", torch.get_num_threads())

print("\nLoading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

print("Loading Llama in FP32 on CPU...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
)

model = model.to("cpu")
model.eval()

print("\nModel:", MODEL_ID)
print("Model device:", next(model.parameters()).device)
print("Weight dtype:", next(model.parameters()).dtype)

messages = [
    {
        "role": "user",
        "content": "What is 12 multiplied by 8? Answer with only the number."
    }
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
)

print("Input shape:", tuple(inputs["input_ids"].shape))
print("Input dtype:", inputs["input_ids"].dtype)

with torch.inference_mode():
    outputs = model.generate(
        **inputs,
        max_new_tokens=20,
        do_sample=False,
        use_cache=True,
        pad_token_id=tokenizer.eos_token_id,
    )

generated_ids = outputs[0][inputs["input_ids"].shape[-1]:]
answer = tokenizer.decode(generated_ids, skip_special_tokens=True)

print("\n===== BASELINE RESULT =====")
print("Prompt:", messages[0]["content"])
print("Answer:", repr(answer))
print("Generated token IDs:", generated_ids.tolist())

result = {
    "model": MODEL_ID,
    "torch_version": torch.__version__,
    "transformers_version": transformers.__version__,
    "device": str(next(model.parameters()).device),
    "weight_dtype": str(next(model.parameters()).dtype),
    "prompt": messages[0]["content"],
    "answer": answer,
    "generated_token_ids": generated_ids.tolist(),
}

with open(OUTPUT_DIR / "baseline.json", "w") as f:
    json.dump(result, f, indent=2)

print("\nSaved: results/baseline.json")
