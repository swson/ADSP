import torch
from torch.profiler import profile, ProfilerActivity
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"

torch.set_num_threads(4)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32
).to("cpu").eval()

layer = model.model.layers[0]
projection = layer.mlp.down_proj

print("\n===== DOWN_PROJ DETAILS =====")
print("Module:", projection)
print("Weight shape:", tuple(projection.weight.shape))
print("Weight dtype:", projection.weight.dtype)
print("Weight device:", projection.weight.device)

def pre_hook(module, inputs):
    x = inputs[0]
    print("\nDOWN_PROJ INPUT")
    print("Shape:", tuple(x.shape))
    print("Dtype:", x.dtype)
    print("Device:", x.device)

def post_hook(module, inputs, output):
    print("\nDOWN_PROJ OUTPUT")
    print("Shape:", tuple(output.shape))
    print("Dtype:", output.dtype)
    print("Device:", output.device)
    print("All finite:", torch.isfinite(output).all().item())
    print("First 5 values:", output.flatten()[:5].tolist())

h1 = projection.register_forward_pre_hook(pre_hook)
h2 = projection.register_forward_hook(post_hook)

messages = [{
    "role": "user",
    "content": "What is 12 multiplied by 8? Answer with only the number."
}]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt"
)

print("\nPrompt shape:", tuple(inputs["input_ids"].shape))

with torch.inference_mode():
    with profile(
        activities=[ProfilerActivity.CPU],
        record_shapes=True
    ) as prof:
        outputs = model(
            **inputs,
            use_cache=False
        )

h1.remove()
h2.remove()

print("\n===== FINAL LOGITS =====")
print("Logits shape:", tuple(outputs.logits.shape))
print("Logits dtype:", outputs.logits.dtype)

print("\n===== PYTORCH OPERATORS =====")
print(prof.key_averages().table(
    sort_by="self_cpu_time_total",
    row_limit=25
))

print("\n===== MATRIX OPERATORS =====")
for event in prof.key_averages(group_by_input_shape=True):
    if any(name in event.key for name in [
        "aten::linear",
        "aten::mm",
        "aten::addmm",
        "aten::mv",
        "aten::matmul"
    ]):
        print(
            event.key,
            "shapes:", event.input_shapes,
            "calls:", event.count
        )

prof.export_chrome_trace("results/down_proj_trace.json")

print("\nSaved: results/down_proj_trace.json")
