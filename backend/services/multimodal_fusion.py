from __future__ import annotations

from io import BytesIO

from fastapi import HTTPException, UploadFile
from PIL import Image

from module.explainer import generate_explanation
from module.fusion import fuse_scores

from services.image_analyzer import analyze_image
from services.text_analyzer import analyze_text


def _prediction_label(verdict: str) -> str:
    return {
        "FAKE": "Likely Fake",
        "REAL": "Likely Real",
        "SUSPICIOUS": "Suspicious",
    }.get(verdict, "Suspicious")


def _confidence_for_frontend(fusion_result: dict) -> float:
    verdict = fusion_result["verdict"]
    fake_p = float(fusion_result["fake_probability"])
    real_p = float(fusion_result["real_probability"])

    if verdict == "FAKE":
        return round(fake_p / 100.0, 4)
    if verdict == "REAL":
        return round(real_p / 100.0, 4)
    return round(max(fake_p, real_p) / 100.0, 4)


async def analyze_multimodal(text: str, image: UploadFile | None) -> dict:
    nlp_result = analyze_text(text)

    pil_image: Image.Image | None = None
    if image is not None:
        try:
            data = await image.read()
            if not data:
                raise HTTPException(status_code=400, detail="Uploaded image file is empty.")
            pil_image = Image.open(BytesIO(data)).convert("RGB")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image uploaded.")

    clip_result, deepfake_result = analyze_image(text, pil_image)

    fusion_result = fuse_scores(nlp_result, clip_result, deepfake_result)
    explanation = generate_explanation(
        text, fusion_result, nlp_result, clip_result, deepfake_result
    )

    verdict = fusion_result["verdict"]
    return {
        "prediction": _prediction_label(verdict),
        "confidence": _confidence_for_frontend(fusion_result),
        "explanation": explanation,
    }

