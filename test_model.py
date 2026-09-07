from app.services.image_preprocessing_service import (
    load_and_preprocess_image,
)

from app.services.model_service import (
    device,
    predict,
)


image_path = "uploads/459efb19-bd66-4a5a-ab20-f619936b8da7.jpg"


print("Using device:", device)

image_tensor = load_and_preprocess_image(
    image_path
)

print(
    "Input shape:",
    image_tensor.shape,
)


result = predict(image_tensor)


print("\nPrediction:")
print("Class:", result["prediction"])
print("Confidence:", result["confidence"])
print(
    "Model:",
    result["model_version"],
)