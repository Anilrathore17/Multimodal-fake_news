import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import timm

# Load pretrained EfficientNet model
model = timm.create_model('efficientnet_b0', pretrained=True, num_classes=2)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def detect_deepfake(image_input) -> dict:
    """
    Detects if an image/frame is AI-manipulated (deepfake).
    Args:
        image_input: PIL Image or file path
    Returns:
        dict with 'deepfake_score', 'is_deepfake' (bool)
    """
    if isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")
    else:
        image = image_input.convert("RGB")

    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)
        probs = torch.softmax(output, dim=1)

    deepfake_score = probs[0][1].item()
    real_score = probs[0][0].item()

    return {
        "deepfake_score": round(deepfake_score * 100, 2),
        "real_score": round(real_score * 100, 2),
        "is_deepfake": deepfake_score > 0.5
    }


# Test it
if __name__ == "__main__":
    from PIL import Image
    import numpy as np

    dummy_image = Image.fromarray(
        np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    )
    result = detect_deepfake(dummy_image)
    print(f"Deepfake Score: {result['deepfake_score']}%")
    print(f"Is Deepfake: {result['is_deepfake']}")