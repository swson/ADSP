import torch
from transformers import AutoModelForCausalLM

MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"

torch.set_num_threads(1)

print("Loading model...", flush=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32
).to("cpu").eval()

projection = model.model.layers[0].mlp.down_proj

x = torch.load(
    "results/down_proj_input.pt",
    map_location="cpu",
    weights_only=True
)

reference = torch.load(
    "results/down_proj_reference.pt",
    map_location="cpu",
    weights_only=True
)

print("Input:", tuple(x.shape), flush=True)
print("Weight:", tuple(projection.weight.shape), flush=True)

with torch.inference_mode():
    for i in range(100):
        y = projection(x)

        if i == 0:
            print("First iteration completed", flush=True)

    print("Completed 100 iterations", flush=True)
    print("Max difference:",
          (y - reference).abs().max().item(),
          flush=True)
