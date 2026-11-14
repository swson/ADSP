import sys
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"
RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)

torch.set_num_threads(1)

print("Loading Llama...", flush=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32
).to("cpu").eval()

projection = model.model.layers[0].mlp.down_proj

mode = sys.argv[1]

if mode == "capture":
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

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

    captured = {}

    def hook(module, args):
        captured["input"] = args[0].detach().clone()

    handle = projection.register_forward_pre_hook(hook)

    with torch.inference_mode():
        model(**inputs, use_cache=False)

    handle.remove()

    x = captured["input"]

    with torch.inference_mode():
        y = projection(x)

    torch.save(x, RESULTS / "down_proj_input.pt")
    torch.save(y, RESULTS / "down_proj_reference.pt")

    print("Captured input:", tuple(x.shape), flush=True)
    print("Reference output:", tuple(y.shape), flush=True)
    print("Saved captured tensors.", flush=True)

elif mode == "target":
    x = torch.load(
        RESULTS / "down_proj_input.pt",
        map_location="cpu",
        weights_only=True
    )

    reference = torch.load(
        RESULTS / "down_proj_reference.pt",
        map_location="cpu",
        weights_only=True
    )

    print("\n===== TARGET DOWN_PROJ =====", flush=True)
    print("Input:", tuple(x.shape), flush=True)
    print("Weight:", tuple(projection.weight.shape), flush=True)


    with torch.inference_mode():
        y = projection(x)

    diff = (y - reference).abs()
    changed = diff > 1e-5

    print("\n===== OUTPUT VERIFICATION =====", flush=True)
    print("Output:", tuple(y.shape))
    print("Max difference:", diff.max().item())
    print("Changed elements:", changed.sum().item())
    print("Total elements:", diff.numel())
    print("All finite:", torch.isfinite(y).all().item())

    positions = torch.nonzero(changed)

    for idx in positions[:10]:
        i, j, k = idx.tolist()
        print(
            f"Position [{i},{j},{k}]: "
            f"baseline={reference[i,j,k].item():.8f}, "
            f"faulty={y[i,j,k].item():.8f}"
        )

    torch.save(y, RESULTS / "down_proj_last_output.pt")
