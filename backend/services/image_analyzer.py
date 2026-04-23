from PIL import Image

from module.clip_module import check_image_text_consistency as _check_image_text_consistency
from module.deepfake_module import detect_deepfake as _detect_deepfake


def analyze_image(text: str, image: Image.Image | None) -> tuple[dict, dict]:
    if image is None:
        clip_result = {"similarity_score": 50, "consistent": True, "mismatch_score": 50}
        deepfake_result = {"deepfake_score": 0, "real_score": 100, "is_deepfake": False}
        return clip_result, deepfake_result

    clip_result = _check_image_text_consistency(text, image)
    deepfake_result = _detect_deepfake(image)
    return clip_result, deepfake_result

