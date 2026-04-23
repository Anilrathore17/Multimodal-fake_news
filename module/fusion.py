def fuse_scores(nlp_result: dict, clip_result: dict, deepfake_result: dict) -> dict:
    """
    Combines scores from all 3 modules into a final credibility score.
    Weights: NLP=40%, CLIP=35%, Deepfake=25%
    """
    nlp_fake = nlp_result["fake_score"]          # 0-100
    clip_mismatch = clip_result["mismatch_score"] # 0-100
    deepfake = deepfake_result["deepfake_score"]  # 0-100

    # Weighted average
    weights = {"nlp": 0.40, "clip": 0.35, "deepfake": 0.25}

    fake_probability = (
        weights["nlp"] * nlp_fake +
        weights["clip"] * clip_mismatch +
        weights["deepfake"] * deepfake
    )

    fake_probability = round(fake_probability, 2)
    real_probability = round(100 - fake_probability, 2)

    if fake_probability >= 70:
        verdict = "FAKE"
        confidence = "High"
    elif fake_probability >= 45:
        verdict = "SUSPICIOUS"
        confidence = "Medium"
    else:
        verdict = "REAL"
        confidence = "High"

    return {
        "fake_probability": fake_probability,
        "real_probability": real_probability,
        "verdict": verdict,
        "confidence": confidence,
        "breakdown": {
            "text_score": nlp_fake,
            "image_text_mismatch": clip_mismatch,
            "deepfake_score": deepfake
        }
    }