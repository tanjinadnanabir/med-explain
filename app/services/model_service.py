import torch
from torchvision.models import (
    ResNet18_Weights,
    resnet18,
)


MODEL_VERSION = "resnet18-imagenet-v1"


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


weights = ResNet18_Weights.DEFAULT

model = resnet18(weights=weights)

model.eval()

model.to(device)


categories = weights.meta["categories"]


def predict(image_tensor: torch.Tensor) -> dict:
    image_tensor = image_tensor.to(device)

    with torch.inference_mode():
        outputs = model(image_tensor)

    probabilities = torch.softmax(
        outputs,
        dim=1,
    )

    confidence, class_index = torch.max(
        probabilities,
        dim=1,
    )

    prediction = categories[class_index.item()]

    return {
        "prediction": prediction,
        "confidence": confidence.item(),
        "model_version": MODEL_VERSION,
    }