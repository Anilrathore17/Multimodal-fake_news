import open_clip
import torch
from PIL import Image
import requests
from io import BytesIO

model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-B-32', pretrained='openai'
)
tokenizer = open_clip.get_tokenizer('ViT-B-32')
model.eval()

def load_image(image_input):
    """Accepts PIL image, file path, or URL."""
    if isinstance(image_input, str):
        if image_input.startswith("http"):
            response = requests.get(image_input)
            return Image.open(BytesIO(response.content)).convert("RGB")
        else:
            return Image.open(image_input).convert("RGB")
    return image_input.convert("RGB")

def check_image_text_consistency(text: str, image_input) -> dict:
    """
    Checks whether the image matches the text using CLIP.
    Returns:
        dict with 'similarity_score', 'consistent' (bool)
    """
    image = load_image(image_input)
    image_tensor = preprocess(image).unsqueeze(0)
    text_tokens = tokenizer([text])

    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        text_features = model.encode_text(text_tokens)

        # Normalize
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (image_features @ text_features.T).item()

    # Scale to 0-100
    score = round((similarity + 1) / 2 * 100, 2)
    consistent = score > 50

    return {
        "similarity_score": score,
        "consistent": consistent,
        "mismatch_score": round(100 - score, 2)
    }


# Test it
if __name__ == "__main__":
    from PIL import Image
    import numpy as np

    # Create a dummy test image (green image = grass/nature)
    dummy_image = Image.fromarray(
        np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    )

    result = check_image_text_consistency(
        "A rocket launch into space at night",
        dummy_image
    )
    print(f"Similarity Score: {result['similarity_score']}%")
    print(f"Consistent: {result['consistent']}")
    print(f"Mismatch Score: {result['mismatch_score']}%")