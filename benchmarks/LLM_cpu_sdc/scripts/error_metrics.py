import torch
import torch.nn.functional as F


def calculate_metrics(baseline, experiment):

    assert baseline.shape == experiment.shape

    b = baseline.detach().double().flatten()
    e = experiment.detach().double().flatten()

    diff = e - b
    abs_diff = diff.abs()

    changed = torch.count_nonzero(diff).item()
    total = b.numel()

    return {
        "total_elements": total,
        "changed_elements": changed,
        "changed_percentage": 100.0 * changed / total,
        "max_abs_error": abs_diff.max().item(),
        "mean_abs_error": abs_diff.mean().item(),
        "rmse": torch.sqrt(
            torch.mean(diff ** 2)
        ).item(),
        "relative_l2_error": (
            torch.linalg.vector_norm(diff)
            / torch.linalg.vector_norm(b).clamp_min(1e-12)
        ).item(),
        "cosine_similarity": F.cosine_similarity(
            b.unsqueeze(0),
            e.unsqueeze(0)
        ).item(),
        "nan_count": torch.isnan(e).sum().item(),
        "inf_count": torch.isinf(e).sum().item()
    }


def token_metrics(scores):

    values, indices = torch.topk(
        scores, k=5, dim=-1
    )

    return {
        "top_5_token_ids": indices.tolist(),
        "top_5_scores": values.tolist(),
        "top_1_margin": (
            values[..., 0] - values[..., 1]
        ).tolist()
    }
