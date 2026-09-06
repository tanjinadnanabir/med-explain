from pathlib import Path

import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

IMAGE_SIZE = 224

preprocess = transforms.Compose(
    [
        transforms.Resize(
            (IMAGE_SIZE, IMAGE_SIZE)
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


def load_and_preprocess_image(
    image_path: str,
) -> torch.Tensor:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    try:
        image = Image.open(path)
        image = image.convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(
            "Could not load the image."
        ) from exc

    tensor = preprocess(image)

    tensor = tensor.unsqueeze(0)

    return tensor