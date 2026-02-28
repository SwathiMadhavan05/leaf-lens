import cv2
import joblib
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="LeafLens", page_icon="🌿", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.cdnfonts.com/css/satoshi');
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap');
    @import url('https://fonts.cdnfonts.com/css/avantime');
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@700&display=swap');

    :root {
        --brand-dark: #193A3C;
        --brand-light: #D5E6AB;
    }

    html, body, [class*="css"], .stApp, h1, h2, h3, h4, h5, h6, p, label, span, div, button, input {
        font-family: "Satoshi", "Segoe UI", sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, var(--brand-dark) 0%, #21484A 60%, var(--brand-dark) 100%);
        color: var(--brand-light);
    }

    .stMarkdown, .stText, label, p, span {
        color: var(--brand-light) !important;
    }

    .stMarkdown, .stMarkdown *, h1, h2, h3, h4, h5, h6, p, label {
        text-align: center !important;
    }

    h1 {
        font-family: "Unbounded", "Syne", "Avantime", "Archivo Black", "Satoshi", sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: 0.02em !important;
    }

    div[data-testid="stFileUploader"] > label,
    div[data-testid="stFileUploaderDropzone"] {
        color: var(--brand-light) !important;
        border-color: var(--brand-light) !important;
    }

    .stButton > button {
        background-color: var(--brand-light) !important;
        color: var(--brand-dark) !important;
        border: 1px solid var(--brand-light) !important;
        font-weight: 700 !important;
    }

    .stMetric {
        background: rgba(213, 230, 171, 0.08);
        border: 1px solid rgba(213, 230, 171, 0.25);
        border-radius: 12px;
        padding: 8px;
    }

    .health-card h2,
    .health-card p,
    .disease-card h2,
    .disease-card p,
    .disease-card li {
        color: #193A3C !important;
        opacity: 1 !important;
    }

    .landing-wrap {
        min-height: 72vh;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }

    .landing-orb {
        position: absolute;
        width: 340px;
        height: 340px;
        border-radius: 50%;
        filter: blur(10px);
        background: radial-gradient(circle, rgba(213,230,171,0.34) 0%, rgba(213,230,171,0.04) 70%);
        animation: floaty 7s ease-in-out infinite;
    }

    .landing-orb.left { left: 4%; top: 18%; animation-delay: 0s; }
    .landing-orb.right { right: 5%; bottom: 8%; animation-delay: 1.2s; }

    .landing-card {
        background: linear-gradient(145deg, rgba(213,230,171,0.16), rgba(25,58,60,0.35));
        border: 1px solid rgba(213,230,171,0.35);
        border-radius: 22px;
        padding: 2.6rem 2.8rem;
        text-align: center;
        max-width: 880px;
        backdrop-filter: blur(6px);
        animation: riseIn 0.9s ease-out;
    }

    .landing-title {
        font-size: 3.2rem;
        letter-spacing: 0.02em;
        margin-bottom: 0.35rem;
        color: var(--brand-light);
        animation: pulseGlow 3.8s ease-in-out infinite;
    }

    .landing-sub {
        font-size: 1.15rem;
        line-height: 1.6;
        color: var(--brand-light);
        opacity: 0.95;
        margin-bottom: 1.6rem;
    }

    @keyframes floaty {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-18px) scale(1.04); }
    }

    @keyframes riseIn {
        from { opacity: 0; transform: translateY(22px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes pulseGlow {
        0%, 100% { text-shadow: 0 0 0 rgba(213,230,171,0.0); }
        50% { text-shadow: 0 0 18px rgba(213,230,171,0.33); }
    }

    .login-card {
        background: linear-gradient(145deg, rgba(213,230,171,0.16), rgba(25,58,60,0.35));
        border: 1px solid rgba(213,230,171,0.35);
        border-radius: 20px;
        padding: 1.7rem 1.4rem 1.2rem;
        backdrop-filter: blur(6px);
        position: relative;
        overflow: hidden;
        animation: riseIn 0.7s ease-out;
    }

    .login-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: -120%;
        width: 120%;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(213,230,171,0.95), transparent);
        animation: loginShimmer 2.7s linear infinite;
    }

    .login-orb {
        position: absolute;
        border-radius: 50%;
        pointer-events: none;
        filter: blur(1px);
        animation: loginFloat 6s ease-in-out infinite;
    }

    .login-orb.one {
        width: 72px;
        height: 72px;
        right: -18px;
        top: -14px;
        background: radial-gradient(circle, rgba(213,230,171,0.45) 0%, rgba(213,230,171,0.0) 72%);
        animation-delay: 0s;
    }

    .login-orb.two {
        width: 58px;
        height: 58px;
        left: -14px;
        bottom: -16px;
        background: radial-gradient(circle, rgba(213,230,171,0.35) 0%, rgba(213,230,171,0.0) 72%);
        animation-delay: 1.2s;
    }

    .login-title {
        font-size: 1.7rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        animation: pulseGlow 4.4s ease-in-out infinite;
    }

    .login-sub {
        font-size: 0.98rem;
        opacity: 0.92;
    }

    @keyframes loginFloat {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-10px) scale(1.05); }
    }

    @keyframes loginShimmer {
        0% { left: -120%; }
        100% { left: 120%; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_health_model():
    try:
        return joblib.load("leaf_health_model.joblib")
    except Exception:
        return None


def extract_model_features(image_rgb: np.ndarray) -> np.ndarray:
    img = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    b, g, r = cv2.split(img)

    features = []
    for ch in (h, s, v):
        features.extend(
            [np.mean(ch), np.std(ch), np.percentile(ch, 10), np.percentile(ch, 90)]
        )
    for ch in (r, g, b):
        features.extend([np.mean(ch), np.std(ch)])

    in_leaf = (s > 25) & (v > 30)
    leaf_px = max(np.count_nonzero(in_leaf), 1)
    green = in_leaf & (h >= 35) & (h <= 95) & (s >= 35) & (v >= 35)
    yellow = in_leaf & (h >= 15) & (h <= 40) & (s >= 30) & (v >= 55)
    brown = in_leaf & (h >= 5) & (h <= 30) & (s >= 45) & (v <= 180)
    white = in_leaf & (s <= 45) & (v >= 175)
    dark = in_leaf & (v <= 70)
    features.extend(
        [
            np.count_nonzero(green) / leaf_px,
            np.count_nonzero(yellow) / leaf_px,
            np.count_nonzero(brown) / leaf_px,
            np.count_nonzero(white) / leaf_px,
            np.count_nonzero(dark) / leaf_px,
        ]
    )

    edges = cv2.Canny(gray, 60, 160)
    features.append(np.mean(edges > 0))
    sobx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    soby = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    grad_mag = np.sqrt(sobx**2 + soby**2)
    features.extend([np.mean(grad_mag), np.std(grad_mag)])

    hist = cv2.calcHist([gray], [0], None, [32], [0, 256]).ravel()
    hist = hist / (hist.sum() + 1e-9)
    entropy = -np.sum(hist * np.log(hist + 1e-12))
    features.extend([np.var(hist), np.max(hist), entropy])

    return np.array(features, dtype=np.float32)


def _largest_component(mask: np.ndarray) -> np.ndarray:
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    if num <= 1:
        return mask
    largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    return np.where(labels == largest, 255, 0).astype(np.uint8)


def analyze_leaf(image_rgb: np.ndarray) -> dict:
    health_model = load_health_model()
    img = cv2.resize(image_rgb, (512, 512), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)

    raw_leaf = ((s > 25) & (v > 30)).astype(np.uint8) * 255
    kernel = np.ones((5, 5), np.uint8)
    raw_leaf = cv2.morphologyEx(raw_leaf, cv2.MORPH_CLOSE, kernel, iterations=2)
    leaf_mask = _largest_component(raw_leaf)
    leaf_area = int(np.count_nonzero(leaf_mask))

    if leaf_area < 12000:
        return {"ok": False, "reason": "No clear leaf detected. Upload a closer leaf photo."}

    in_leaf = leaf_mask > 0
    green_mask = in_leaf & (h >= 35) & (h <= 95) & (s >= 35) & (v >= 35)
    yellow_mask = in_leaf & (h >= 15) & (h <= 40) & (s >= 30) & (v >= 55)
    brown_mask = in_leaf & (h >= 5) & (h <= 30) & (s >= 45) & (v <= 180)
    dark_mask = in_leaf & (v <= 70)
    white_mask = in_leaf & (s <= 45) & (v >= 175)
    rust_mask = in_leaf & (h >= 5) & (h <= 22) & (s >= 80) & (v >= 70) & (v <= 200)

    lesion_mask = (yellow_mask | brown_mask | dark_mask | white_mask) & (~green_mask)
    lesion_u8 = lesion_mask.astype(np.uint8) * 255
    lesion_u8 = cv2.morphologyEx(lesion_u8, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)

    # Count medium/large lesions.
    num, _, stats, _ = cv2.connectedComponentsWithStats(lesion_u8, connectivity=8)
    min_spot_area = max(20, int(leaf_area * 0.0012))
    major_spots = int(np.sum(stats[1:, cv2.CC_STAT_AREA] >= min_spot_area)) if num > 1 else 0

    # Count small rust-like micro spots that were previously ignored.
    micro_mask = ((rust_mask | dark_mask) & (~green_mask)).astype(np.uint8) * 255
    micro_mask = cv2.morphologyEx(micro_mask, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8), iterations=1)
    micro_num, _, micro_stats, _ = cv2.connectedComponentsWithStats(micro_mask, connectivity=8)
    micro_min_area = max(6, int(leaf_area * 0.00006))
    micro_max_area = min_spot_area
    micro_spots = (
        int(np.sum((micro_stats[1:, cv2.CC_STAT_AREA] >= micro_min_area) & (micro_stats[1:, cv2.CC_STAT_AREA] < micro_max_area)))
        if micro_num > 1
        else 0
    )

    spot_count = major_spots + micro_spots

    green_ratio = float(np.count_nonzero(green_mask) / leaf_area)
    lesion_ratio = float(np.count_nonzero(lesion_mask) / leaf_area)
    yellow_ratio = float(np.count_nonzero(yellow_mask) / leaf_area)
    brown_ratio = float(np.count_nonzero(brown_mask) / leaf_area)
    white_ratio = float(np.count_nonzero(white_mask) / leaf_area)
    rust_ratio = float(np.count_nonzero(rust_mask) / leaf_area)
    dark_ratio = float(np.count_nonzero(dark_mask) / leaf_area)

    disease_score = (
        1.4 * lesion_ratio
        + 1.3 * brown_ratio
        + 1.1 * yellow_ratio
        + 1.1 * white_ratio
        + 1.2 * dark_ratio
        + 0.04 * min(spot_count, 20)
        + max(0.0, 0.5 - green_ratio)
    )
    strong_visual_disease = bool(
        (lesion_ratio >= 0.16)
        or (spot_count >= 10 and lesion_ratio >= 0.08)
        or (brown_ratio >= 0.08 and spot_count >= 6)
        or (disease_score >= 1.25)
    )
    if health_model is not None:
        model_features = extract_model_features(image_rgb).reshape(1, -1)
        prob_diseased = float(health_model.predict_proba(model_features)[0][1])
        model_diseased = prob_diseased >= 0.58
    else:
        prob_diseased = min(0.99, disease_score / 1.6)
        model_diseased = False

    diseased = bool(model_diseased or strong_visual_disease)
    healthy_no_spots = bool((not diseased) and lesion_ratio < 0.09 and spot_count <= 6 and green_ratio >= 0.52)

    if white_ratio > 0.08:
        disease_type = "Powdery mildew"
        treatment = [
            "Spray wettable sulfur (2 g/L) or potassium bicarbonate weekly.",
            "Prune crowded leaves and improve airflow around the plant.",
            "Avoid overhead watering; water near the root zone only.",
        ]
    elif rust_ratio > 0.04:
        disease_type = "Rust / fungal leaf spots"
        treatment = [
            "Use copper oxychloride (2.5-3 g/L) every 7-10 days for 2-3 cycles.",
            "Remove heavily infected leaves and keep tools sanitized.",
            "Keep foliage dry in the evening to reduce fungal spread.",
        ]
    elif yellow_ratio > 0.18 and brown_ratio < 0.06:
        disease_type = "Chlorosis / stress pattern"
        treatment = [
            "Check watering consistency and improve drainage.",
            "Apply balanced micronutrient feed (especially iron/magnesium).",
            "Keep in bright indirect light and monitor for 5-7 days.",
        ]
    else:
        disease_type = "Leaf blight / necrotic spot pattern"
        treatment = [
            "Apply Mancozeb (2 g/L) every 7 days for 2-3 rounds.",
            "Remove necrotic leaves to reduce reinfection pressure.",
            "Avoid wet leaves overnight and improve air circulation.",
        ]

    confidence = int(np.clip(55 + abs(prob_diseased - 0.5) * 90, 55, 99))

    return {
        "ok": True,
        "diseased": diseased,
        "healthy_no_spots": healthy_no_spots,
        "disease_type": disease_type,
        "treatment": treatment,
        "confidence": confidence,
        "metrics": {
            "green_ratio": green_ratio,
            "lesion_ratio": lesion_ratio,
            "spot_count": spot_count,
            "disease_score": disease_score,
            "model_prob_diseased": prob_diseased,
        },
    }


if "show_main_app" not in st.session_state:
    st.session_state.show_main_app = False
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

LOGIN_USERS = {"farmer01": "leaf123", "agriadmin": "crop456"}

if not st.session_state.is_authenticated:
    l1, l2, l3 = st.columns([1.15, 1.2, 1.15])
    with l2:
        st.markdown(
            """
            <div class="login-card">
                <div class="login-orb one"></div>
                <div class="login-orb two"></div>
                <div class="login-title">Welcome Back</div>
                <p class="login-sub">Enter your username and password to continue.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")
        username = st.selectbox("Username", list(LOGIN_USERS.keys()))
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True, type="primary"):
            if LOGIN_USERS.get(username) == password:
                st.session_state.is_authenticated = True
                st.rerun()
            else:
                st.error("Invalid username or password.")
elif not st.session_state.show_main_app:
    st.markdown(
        """
        <div class="landing-wrap">
            <div class="landing-orb left"></div>
            <div class="landing-orb right"></div>
            <div class="landing-card">
                <div class="landing-title">LeafLens</div>
                <p class="landing-sub">
                    AI-powered leaf diagnosis with instant healthy/diseased detection
                    and actionable treatment guidance.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Enter Diagnosis", use_container_width=True, type="primary"):
            st.session_state.show_main_app = True
            st.rerun()
else:
    st.title("🌿 LEAFLENS")
    st.markdown("**Upload a leaf image -> get Healthy/Diseased + treatment advice**")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("📱 Upload Leaf")
        uploaded_file = st.file_uploader("Drag JPG/PNG", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB").resize((350, 350))
            st.image(image, caption="Your leaf", use_container_width=True)

    with col2:
        if uploaded_file and st.button("🔍 **DIAGNOSE**", type="primary", use_container_width=True):
            image_rgb = np.array(Image.open(uploaded_file).convert("RGB"))
            result = analyze_leaf(image_rgb)

            if not result["ok"]:
                st.warning(result["reason"])
            elif result["healthy_no_spots"]:
                st.success("### ✅ HEALTHY LEAF")
                st.markdown(
                    """
                    <div class='health-card' style='background: linear-gradient(135deg, #D5E6AB, #C7D99B);
                                padding: 2rem; border-radius: 20px; border-left: 6px solid #193A3C;'>
                        <h2 style='color: #193A3C;'>GOOD TO GO</h2>
                        <p style='font-size: 1.1rem; font-weight: 700; text-shadow: none;'>
                            Leaf looks healthy and no significant spots were detected.
                            No treatment needed.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.error("### 🚨 DISEASED LEAF")
                treatment_html = "".join([f"<li>{item}</li>" for item in result["treatment"]])
                st.markdown(
                    f"""
                    <div class='disease-card' style='background: linear-gradient(135deg, rgba(213, 230, 171, 0.92), rgba(199, 217, 155, 0.92));
                                padding: 2rem; border-radius: 20px; border-left: 6px solid #193A3C;'>
                        <h2 style='color: #193A3C;'>Disease detected: {result["disease_type"]}</h2>
                        <p style='font-weight: 700; color: #193A3C;'>Recommended treatment:</p>
                        <ul style='color: #193A3C; font-size: 1rem; margin-top: 0.4rem;'>
                            {treatment_html}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if result["ok"]:
                m = result["metrics"]
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Confidence", f'{result["confidence"]}%')
                c2.metric("Green Area", f"{m['green_ratio'] * 100:.1f}%")
                c3.metric("Lesion Area", f"{m['lesion_ratio'] * 100:.1f}%")
                c4.metric("Spots", f"{m['spot_count']}")

    st.markdown("---")
    st.markdown("*🌿 LeafLens | Healthy vs Diseased + actionable treatment*")
