import requests
import os

# ✅ New updated URL
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

def _headers() -> dict:
    token = os.getenv("HF_API_TOKEN", "").strip()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def generate_explanation(
    text: str,
    fusion_result: dict,
    nlp_result: dict,
    clip_result: dict,
    deepfake_result: dict
) -> str:
    verdict        = fusion_result["verdict"]
    fake_prob      = fusion_result["fake_probability"]
    text_score     = fusion_result["breakdown"]["text_score"]
    mismatch_score = fusion_result["breakdown"]["image_text_mismatch"]
    deepfake_score = fusion_result["breakdown"]["deepfake_score"]

    prompt = f"""Analyze this fake news detection result and explain in 3 simple sentences:
News: "{text[:200]}"
Verdict: {verdict} ({fake_prob}% fake probability)
Text fake indicators: {text_score}%
Image-text mismatch: {mismatch_score}%
Deepfake probability: {deepfake_score}%
Explanation:"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.3,
            "return_full_text": False
        }
    }

    try:
        headers = _headers()
        if not headers:
            return generate_rule_based_explanation(
                verdict, fake_prob, text_score, mismatch_score, deepfake_score
            )

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "").strip()
        else:
            return generate_rule_based_explanation(
                verdict, fake_prob,
                text_score, mismatch_score, deepfake_score
            )

    except Exception as e:
        print(f"Explainer Error: {e}")
        return generate_rule_based_explanation(
            verdict, fake_prob,
            text_score, mismatch_score, deepfake_score
        )


def generate_rule_based_explanation(
    verdict, fake_prob,
    text_score, mismatch_score, deepfake_score
) -> str:
    parts = []

    if text_score > 60:
        parts.append(
            f"The text contains {text_score:.0f}% fake indicators "
            "such as sensational language."
        )
    if mismatch_score > 50:
        parts.append(
            f"The image does not match the headline "
            f"({mismatch_score:.0f}% mismatch)."
        )
    if deepfake_score > 50:
        parts.append(
            f"The image shows {deepfake_score:.0f}% chance "
            "of being AI-manipulated."
        )
    if not parts:
        parts.append(
            "The content appears credible based on all analysis."
        )

    return (
        f"This content was classified as {verdict} "
        f"with {fake_prob:.0f}% fake probability. "
        + " ".join(parts)
    )