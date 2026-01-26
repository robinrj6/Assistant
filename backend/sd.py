from diffusers import StableDiffusionPipeline
import torch

model_id = "sd-legacy/stable-diffusion-v1-5"


def _get_device():
    """Get the best available device (cuda > mps > cpu)."""
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def sd(generate_request):
    device = _get_device()
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(device)

    # Respect the provided seed when present for deterministic outputs
    generator = (
        torch.Generator(device).manual_seed(generate_request.seed)
        if generate_request.seed is not None
        else None
    )
    pipe.enable_model_cpu_offload()

    result = pipe(
        prompt=generate_request.prompt,
        num_inference_steps=generate_request.steps,
        guidance_scale=generate_request.guidance_scale,
        generator=generator,
    )
    return result.images[0]
