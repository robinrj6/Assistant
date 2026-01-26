"""ControlNet canny conditioning pipeline."""
from io import BytesIO
from typing import Optional

import torch
from PIL import Image, ImageFilter
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline

controlnet_id = "lllyasviel/sd-controlnet-canny"
base_model_id = "sd-legacy/stable-diffusion-v1-5"


def _get_device():
    """Get the best available device (cuda > mps > cpu)."""
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def _prep_canny_image(image_bytes: bytes) -> Image.Image:
    """Decode upload bytes and create a canny-like edge map for ControlNet."""
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
    return edges.convert("RGB")


def control_net_Canny(generate_request, image_bytes: bytes):
    device = _get_device()
    controlnet = ControlNetModel.from_pretrained(
        controlnet_id, torch_dtype=torch.float16
    )
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        base_model_id, controlnet=controlnet, torch_dtype=torch.float16
    ).to(device)

    generator: Optional[torch.Generator] = (
        torch.Generator(device).manual_seed(generate_request.seed)
        if generate_request.seed is not None
        else None
    )
    pipe.enable_model_cpu_offload()

    control_image = _prep_canny_image(image_bytes)

    result = pipe(
        prompt=generate_request.prompt,
        num_inference_steps=generate_request.steps,
        guidance_scale=generate_request.guidance_scale,
        generator=generator,
        image=control_image,
    )
    return result.images[0]
    