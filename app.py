import streamlit as st
from PIL import Image
from datetime import datetime
from module.nlp_module import analyze_text
from module.fusion import fuse_scores
from module.explainer import generate_explanation

st.set_page_config(
    page_title="NewsGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

try:
    from module.clip_module import check_image_text_consistency
except:
    def check_image_text_consistency(t, i):
        return {"similarity_score": 50, "consistent": True, "mismatch_score": 50}

try:
    from module.deepfake_module import detect_deepfake
except:
    def detect_deepfake(i):
        return {"deepfake_score": 0, "real_score": 100, "is_deepfake": False}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap');
* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0f0f0f !important;
    color: #f0f0f0 !important;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
.ng-header {
    background: #0f0f0f;
    border-bottom: 3px solid #e63946;
    padding: 14px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.ng-logo {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    color: #fff;
    letter-spacing: 1px;
}
.ng-logo span { color: #e63946; }
.ng-tagline {
    font-size: 10px;
    color: #666;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}
.ng-date {
    font-size: 11px;
    color: #555;
    text-align: right;
    font-family: 'Inter', sans-serif;
}
.ng-ticker {
    background: #e63946;
    padding: 8px 32px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    color: #fff;
    text-transform: uppercase;
}
.ng-panel-title {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    color: #fff;
    border-bottom: 1px solid #2a2a2a;
    padding-bottom: 10px;
    margin-bottom: 18px;
}
.ng-howto {
    background: #0a0a0a;
    border: 1px solid #1e1e1e;
    padding: 14px 16px;
    margin-top: 14px;
}
.ng-howto-title {
    font-size: 10px;
    font-weight: 700;
    color: #e63946;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.ng-step {
    display: flex;
    gap: 10px;
    margin-bottom: 8px;
    align-items: flex-start;
}
.ng-step-num {
    background: #e63946;
    color: #fff;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.ng-step-text { font-size: 11px; color: #666; line-height: 1.6; }
.ng-awaiting {
    background: #141414;
    border: 1px solid #2a2a2a;
    padding: 80px 24px;
    text-align: center;
    min-height: 340px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.ng-awaiting-icon { font-size: 44px; margin-bottom: 14px; }
.ng-awaiting-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    color: #444;
    margin-bottom: 8px;
}
.ng-awaiting-sub { font-size: 12px; color: #333; line-height: 1.7; }
.ng-verdict-fake {
    background: #e63946;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
}
.ng-verdict-real {
    background: #2ecc71;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
}
.ng-verdict-suspicious {
    background: #f39c12;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
}
.ng-verdict-text {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    color: #fff;
    letter-spacing: 2px;
}
.ng-verdict-sub {
    font-size: 10px;
    color: rgba(255,255,255,0.75);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 5px;
}
.ng-pills {
    display: flex;
    gap: 6px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}
.ng-pill {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    color: #888;
    padding: 4px 10px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.ng-pill-red {
    background: #2a0a0a;
    border: 1px solid #5a1a1a;
    color: #e63946;
    padding: 4px 10px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.ng-pill-green {
    background: #0a1e0a;
    border: 1px solid #1a3a1a;
    color: #2ecc71;
    padding: 4px 10px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.ng-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    padding: 16px;
    margin-bottom: 10px;
}
.ng-card-title {
    font-size: 10px;
    font-weight: 700;
    color: #666;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-bottom: 1px solid #222;
    padding-bottom: 8px;
    margin-bottom: 14px;
}
.ng-meter-row { margin-bottom: 12px; }
.ng-meter-label {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #666;
    margin-bottom: 5px;
}
.ng-meter-track {
    background: #222;
    height: 6px;
    border-radius: 1px;
    overflow: hidden;
}
.ng-score-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #1e1e1e;
}
.ng-score-row:last-child { border-bottom: none; }
.ng-score-name { font-size: 12px; color: #777; }
.ng-score-val-red { font-size: 16px; font-weight: 700; color: #e63946; }
.ng-score-val-green { font-size: 16px; font-weight: 700; color: #2ecc71; }
.ng-score-val-blue { font-size: 16px; font-weight: 700; color: #3498db; }
.ng-score-val-purple { font-size: 16px; font-weight: 700; color: #9b59b6; }
.ng-mini-bar {
    background: #1e1e1e;
    height: 3px;
    margin-top: 3px;
    margin-bottom: 2px;
}
.ng-ai-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #e63946;
    padding: 16px;
    margin-bottom: 10px;
}
.ng-ai-text {
    font-size: 12px;
    color: #888;
    font-style: italic;
    line-height: 1.9;
}
.ng-footer {
    background: #0a0a0a;
    border-top: 1px solid #1e1e1e;
    padding: 12px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
}
.ng-footer-brand {
    font-family: 'Playfair Display', serif;
    font-size: 14px;
    color: #333;
}
.ng-footer-brand span { color: #e63946; }
.ng-footer-links { font-size: 10px; color: #333; letter-spacing: 1px; text-transform: uppercase; }

/* Streamlit widget overrides */
.stTextArea label { color: #888 !important; font-size: 12px !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
.stTextArea textarea {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-top: 2px solid #e63946 !important;
    border-radius: 0 !important;
    color: #ccc !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}
.stTextArea textarea::placeholder { color: #444 !important; font-style: italic; }
.stFileUploader label { color: #888 !important; font-size: 12px !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
div[data-testid="stFileUploader"] {
    background: #1a1a1a !important;
    border: 2px dashed #2a2a2a !important;
    border-radius: 0 !important;
}
.stButton > button {
    background: #e63946 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 14px !important;
    width: 100% !important;
    margin-top: 8px !important;
}
.stButton > button:hover { background: #c1121f !important; }
div[data-testid="stSpinner"] { color: #e63946 !important; }
</style>
""", unsafe_allow_html=True)

today = datetime.now().strftime("%A, %B %d, %Y")

st.markdown(f"""
<div class="ng-header">
    <div>
        <div class="ng-logo">News<span>Guard</span> AI</div>
        <div class="ng-tagline">Multimodal Fake News Detection System</div>
    </div>
    <div class="ng-date">{today}<br>RoBERTa · CLIP · EfficientNet</div>
</div>
<div class="ng-ticker">
    ⚡ Live Analysis &nbsp;·&nbsp;
    Paste any news article below to verify its authenticity instantly &nbsp;·&nbsp;
    Unisys Innovation Program 2026
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown('<div class="ng-panel-title">Submit Article for Verification</div>',
                unsafe_allow_html=True)

    news_text = st.text_area(
        "NEWS TEXT",
        height=180,
        placeholder="Paste your news headline or full article text here...\n\nExample: Scientists discover drinking bleach cures cancer! Government HIDING this secret!!!"
    )

    uploaded_image = st.file_uploader(
        "ATTACH IMAGE (OPTIONAL)",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_image:
        st.image(Image.open(uploaded_image),
                 caption="Attached image",
                 use_column_width=True)

    analyze_btn = st.button("🔍 VERIFY THIS NEWS", use_container_width=True)

    st.markdown("""
    <div class="ng-howto">
        <div class="ng-howto-title">How It Works</div>
        <div class="ng-step">
            <div class="ng-step-num">1</div>
            <div class="ng-step-text">NLP model scans text for fake indicators and sensational language</div>
        </div>
        <div class="ng-step">
            <div class="ng-step-num">2</div>
            <div class="ng-step-text">CLIP model checks image-text consistency</div>
        </div>
        <div class="ng-step">
            <div class="ng-step-num">3</div>
            <div class="ng-step-text">EfficientNet scans for deepfake manipulation</div>
        </div>
        <div class="ng-step">
            <div class="ng-step-num">4</div>
            <div class="ng-step-text">All scores fused into final credibility verdict</div>
        </div>
        <div class="ng-step">
            <div class="ng-step-num">5</div>
            <div class="ng-step-text">AI generates human-readable explanation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="ng-panel-title">Verification Report</div>',
                unsafe_allow_html=True)

    if not analyze_btn:
        st.markdown("""
        <div class="ng-awaiting">
            <div class="ng-awaiting-icon">🗞️</div>
            <div class="ng-awaiting-title">Awaiting Submission</div>
            <div class="ng-awaiting-sub">
                Paste a news article on the left<br>and click Verify to see results here
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        if not news_text.strip():
            st.error("Please paste a news article before verifying.")
            st.stop()

        with st.spinner("Analyzing article..."):
            nlp_result = analyze_text(news_text)

        image = None
        if uploaded_image:
            image = Image.open(uploaded_image)
            with st.spinner("Checking image consistency..."):
                clip_result = check_image_text_consistency(news_text, image)
            with st.spinner("Scanning for deepfakes..."):
                deepfake_result = detect_deepfake(image)
        else:
            clip_result     = {"similarity_score": 50, "consistent": True,  "mismatch_score": 50}
            deepfake_result = {"deepfake_score": 0,    "real_score": 100,   "is_deepfake": False}

        fusion_result = fuse_scores(nlp_result, clip_result, deepfake_result)
        explanation   = generate_explanation(
            news_text, fusion_result,
            nlp_result, clip_result, deepfake_result
        )

        verdict   = fusion_result["verdict"]
        fake_prob = fusion_result["fake_probability"]
        real_prob = fusion_result["real_probability"]
        conf      = fusion_result["confidence"]

        vclass = {
            "FAKE":       "ng-verdict-fake",
            "REAL":       "ng-verdict-real",
            "SUSPICIOUS": "ng-verdict-suspicious"
        }.get(verdict, "ng-verdict-fake")

        vtext = {
            "FAKE":       "🔴 FAKE NEWS DETECTED",
            "REAL":       "🟢 CREDIBLE NEWS",
            "SUSPICIOUS": "🟡 SUSPICIOUS — VERIFY FURTHER"
        }.get(verdict, "⚪ UNKNOWN")

        pill_verdict = "ng-pill-red" if verdict == "FAKE" else "ng-pill-green"

        st.markdown(f"""
        <div class="{vclass}">
            <div class="ng-verdict-text">{vtext}</div>
            <div class="ng-verdict-sub">{conf} confidence · {fake_prob}% fake probability</div>
        </div>
        <div class="ng-pills">
            <div class="{pill_verdict}">Verdict: {verdict}</div>
            <div class="ng-pill">Confidence: {conf}</div>
            <div class="ng-pill-red">Fake: {fake_prob}%</div>
            <div class="ng-pill-green">Real: {real_prob}%</div>
        </div>
        """, unsafe_allow_html=True)

        t  = nlp_result['fake_score']
        im = clip_result['mismatch_score']
        df = deepfake_result['deepfake_score']

        st.markdown(f"""
        <div class="ng-card">
            <div class="ng-card-title">Confidence Meters</div>
            <div class="ng-meter-row">
                <div class="ng-meter-label">
                    <span>Text Fake Indicators</span>
                    <span style="color:#e63946;font-weight:600">{t}%</span>
                </div>
                <div class="ng-meter-track">
                    <div style="background:#e63946;height:6px;width:{t}%"></div>
                </div>
            </div>
            <div class="ng-meter-row">
                <div class="ng-meter-label">
                    <span style="color:#3498db">Image–Text Mismatch</span>
                    <span style="color:#3498db;font-weight:600">{im}%</span>
                </div>
                <div class="ng-meter-track">
                    <div style="background:#3498db;height:6px;width:{im}%"></div>
                </div>
            </div>
            <div class="ng-meter-row">
                <div class="ng-meter-label">
                    <span style="color:#9b59b6">Deepfake Risk</span>
                    <span style="color:#9b59b6;font-weight:600">{df}%</span>
                </div>
                <div class="ng-meter-track">
                    <div style="background:#9b59b6;height:6px;width:{df}%"></div>
                </div>
            </div>
            <div class="ng-meter-row" style="margin-bottom:0">
                <div class="ng-meter-label">
                    <span>Overall Fake Probability</span>
                    <span style="color:#e63946;font-weight:600">{fake_prob}%</span>
                </div>
                <div class="ng-meter-track">
                    <div style="background:#e63946;height:6px;width:{fake_prob}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        scores = [
            ("NLP Text Analysis",      t,        "#e63946"),
            ("Image–Text Mismatch",    im,       "#3498db"),
            ("Deepfake Risk Score",    df,       "#9b59b6"),
            ("Final Fake Probability", fake_prob,"#e63946"),
        ]

        breakdown = '<div class="ng-card"><div class="ng-card-title">Detailed Score Breakdown</div>'
        for name, val, color in scores:
            breakdown += f"""
            <div class="ng-score-row">
                <span class="ng-score-name">{name}</span>
                <span style="font-size:16px;font-weight:700;color:{color}">{val}%</span>
            </div>
            <div class="ng-mini-bar">
                <div style="background:{color};height:3px;width:{val}%"></div>
            </div>
            """
        breakdown += "</div>"
        st.markdown(breakdown, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ng-ai-card">
            <div class="ng-card-title">AI Analyst Report</div>
            <div class="ng-ai-text">{explanation}</div>
        </div>
        """, unsafe_allow_html=True)

        if image:
            st.image(image, caption="Analyzed image", use_column_width=True)

st.markdown("""
<div class="ng-footer">
    <div class="ng-footer-brand">News<span>Guard</span> AI</div>
    <div class="ng-footer-links">
        Unisys Innovation Program 2026 &nbsp;·&nbsp;
        RoBERTa · CLIP · EfficientNet · GenAI
    </div>
</div>
""", unsafe_allow_html=True)