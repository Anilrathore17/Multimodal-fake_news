def analyze_text(text: str) -> dict:
    """
    Local keyword-based fake news detection.
    No API, no internet, no installation issues.
    Works 100% offline.
    """
    text_lower = text.lower()
    words = text.split()

    # ---- Fake news indicators ----
    fake_keywords = {
        # Health misinformation
        "miracle cure": 3, "cures cancer": 3, "cures all": 3,
        "doctors hate": 3, "bleach": 3, "drinking bleach": 3,
        "secret cure": 2, "they don't want you": 2,

        # Conspiracy
        "government hiding": 2, "mainstream media won't": 2,
        "deep state": 2, "illuminati": 3, "new world order": 2,
        "population control": 2, "microchip": 2, "5g causes": 3,
        "bill gates": 1, "conspiracy": 2,

        # Sensational language
        "you won't believe": 2, "shocking": 1, "explosive": 1,
        "bombshell": 2, "breaking news": 1, "urgent": 1,
        "hoax": 2, "scam": 2, "fraud": 1,
        "100% guaranteed": 3, "amazing secret": 2,
        "alien": 1, "ufo": 1, "reptilian": 3,

        # Clickbait
        "click here": 2, "share before deleted": 3,
        "banned video": 3, "censored": 1,
        "what they hide": 2, "secret they": 2,
    }

    # ---- Real news indicators ----
    real_keywords = {
        "according to": 2, "research shows": 2, "study finds": 2,
        "officials said": 2, "announced": 1, "confirmed": 1,
        "per cent": 1, "percent": 1, "published": 1,
        "university": 2, "scientists": 1, "reported": 1,
        "data shows": 2, "statistics": 2, "evidence": 2,
        "survey": 1, "report": 1, "analysis": 1,
        "government announced": 2, "minister": 1,
        "press release": 2, "official": 1,
        "study published": 2, "journal": 2,
        "researchers": 2, "experts say": 2,
        "according to sources": 2, "statement": 1,
    }

    # ---- Calculate scores ----
    fake_score = 0
    real_score = 0

    for keyword, weight in fake_keywords.items():
        if keyword in text_lower:
            fake_score += weight
            print(f"  [FAKE indicator] '{keyword}' found (+{weight})")

    for keyword, weight in real_keywords.items():
        if keyword in text_lower:
            real_score += weight
            print(f"  [REAL indicator] '{keyword}' found (+{weight})")

    # ---- Caps ratio check (SHOUTING = fake) ----
    caps_words = sum(1 for w in words if w.isupper() and len(w) > 2)
    caps_ratio = caps_words / max(len(words), 1)
    if caps_ratio > 0.2:
        fake_score += 3
        print(f"  [FAKE indicator] Too many CAPS ({caps_ratio:.0%}) (+3)")

    # ---- Exclamation marks check ----
    exclamations = text.count("!")
    if exclamations >= 2:
        fake_score += 2
        print(f"  [FAKE indicator] {exclamations} exclamation marks (+2)")

    # ---- Question marks baiting ----
    questions = text.count("?")
    if questions >= 2:
        fake_score += 1
        print(f"  [FAKE indicator] {questions} question marks (+1)")

    # ---- Text length check ----
    # Very short sensational text = more likely fake
    if len(words) < 10 and fake_score > 0:
        fake_score += 1

    # ---- Convert to percentage ----
    total = fake_score + real_score

    if total == 0:
        # Neutral text — slight real bias
        fake_pct  = 35.0
        real_pct  = 65.0
    else:
        fake_pct = round((fake_score / total) * 100, 2)
        real_pct = round((real_score / total) * 100, 2)

    # ---- Clamp between 5 and 95 ----
    fake_pct = max(5.0, min(95.0, fake_pct))
    real_pct = round(100 - fake_pct, 2)

    label = "FAKE" if fake_pct >= 50 else "REAL"

    return {
        "label": label,
        "fake_score": fake_pct,
        "real_score": real_pct
    }


if __name__ == "__main__":
    tests = [
        # Should be FAKE
        "SHOCKING: Scientists discover that drinking bleach daily "
        "cures cancer completely! Government is HIDING this secret "
        "from public!!! Share before deleted!!!",

        # Should be REAL
        "According to a study published in Nature journal, researchers "
        "at Harvard University confirmed that regular exercise reduces "
        "risk of heart disease by 30 percent.",

        # Should be FAKE
        "You won't believe what they found! Illuminati controls all "
        "mainstream media. The deep state is hiding the truth about "
        "5G causes cancer conspiracy.",

        # Should be REAL
        "The Reserve Bank of India announced a 0.25% increase in "
        "repo rate. Officials confirmed the decision following "
        "analysis of inflation data statistics.",
    ]

    print("=" * 55)
    print("   FAKE NEWS DETECTOR — LOCAL KEYWORD ANALYSIS")
    print("=" * 55)

    for i, sample in enumerate(tests, 1):
        print(f"\nTest {i}: {sample[:65]}...")
        result = analyze_text(sample)
        icon = "🔴" if result["label"] == "FAKE" else "🟢"
        print(f"{icon} Label     : {result['label']}")
        print(f"   Fake Score: {result['fake_score']}%")
        print(f"   Real Score: {result['real_score']}%")
        print("-" * 55)