# from app.services.image_preprocessing_service import (
#     load_and_preprocess_image,
# )


# image_path = "uploads/459efb19-bd66-4a5a-ab20-f619936b8da7.jpg"

# tensor = load_and_preprocess_image(image_path)

# print("Tensor shape:", tensor.shape)
# print("Tensor dtype:", tensor.dtype)
# print("Tensor minimum:", tensor.min().item())
# print("Tensor maximum:", tensor.max().item())

from pathlib import Path

import torch
from PIL import Image

from app.services.image_preprocessing_service import preprocess


image_path = Path(
    "uploads/459efb19-bd66-4a5a-ab20-f619936b8da7.jpg"
)

image = Image.open(image_path)

print("Original:")
print("Format:", image.format)
print("Mode:", image.mode)
print("Size:", image.size)


image = image.convert("RGB")

print("\nAfter RGB conversion:")
print("Mode:", image.mode)
print("Size:", image.size)


tensor = preprocess(image)

print("\nAfter preprocessing:")
print("Shape:", tensor.shape)
print("Dtype:", tensor.dtype)


tensor = tensor.unsqueeze(0)

print("\nAfter batch dimension:")
print("Shape:", tensor.shape)