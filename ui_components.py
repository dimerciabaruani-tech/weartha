# ui_components.py
import streamlit as st
import os
import random

# ---------------------------------------------------------------------------
# Design tokens live here in one place so the whole app stays visually
# consistent. Colors are deliberately close to the original palette (the
# app's identity), just refined slightly for contrast and a calmer,
# "native app" feel.
# ---------------------------------------------------------------------------


def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

    :root {
        --bg: #0B0F17;
        --surface: rgba(255,255,255,0.045);
        --surface-strong: rgba(255,255,255,0.07);
        --border: rgba(255,255,255,0.09);
        --text: #F5F6F8;
        --text-secondary: #8B93A6;
        --accent: #FF9F45;
        --accent-2: #5DDBC9;
        --storm: #7B93BE;
        --radius-lg: 22px;
        --radius-md: 14px;
        --font-display: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
        --font-mono: ui-monospace, 'SF Mono', 'JetBrains Mono', monospace;
    }

    /* Use stable, documented Streamlit hooks (data-testid) rather than
       hashed CSS-module classnames, which change between Streamlit
       versions and were silently breaking most of this file's styling. */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        font-family: var(--font-display);
        background: radial-gradient(circle at 30% 0%, #131B2C 0%, var(--bg) 60%) fixed;
        color: var(--text);
    }
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    /* Mobile-first: a narrow, centered column that reads like a native
       app frame rather than a stretched desktop web page. */
    [data-testid="stMainBlockContainer"], .block-container {
        max-width: 480px;
        margin: 0 auto;
        padding: max(1.25rem, env(safe-area-inset-top)) 1.1rem 2.5rem 1.1rem !important;
    }

    /* ---------------- Top bar / large-title header ---------------- */
    .brand-row {
        display: flex; align-items: center; gap: 0.5rem;
        color: var(--text-secondary); font-size: 0.78rem;
        font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .brand-row svg { width: 16px; height: 16px; }
    .cloak-hero { margin-bottom: 1.3rem; }
    .cloak-hero h1 {
        display: flex; align-items: center; gap: 0.55rem;
        font-weight: 700; font-size: 2.0rem; line-height: 1.15;
        color: var(--text); letter-spacing: -0.02em; margin: 0;
    }
    .cloak-hero h1 svg { width: 30px; height: 30px; flex-shrink: 0; }
    .cloak-hero p { color: var(--text-secondary); font-size: 0.95rem; margin: 0.35rem 0 0 0; }

    /* ---------------- Section labels ---------------- */
    .section-label {
        display: flex; align-items: center; gap: 0.45rem;
        font-size: 0.82rem; font-weight: 600; color: var(--text-secondary);
        margin: 1.6rem 0 0.6rem 0;
    }
    .section-label svg { width: 15px; height: 15px; }

    /* ---------------- Inputs: sized to avoid iOS auto-zoom (16px) ---------------- */
    .stTextInput input, .stNumberInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        font-size: 16px !important;
        min-height: 44px;
    }
    /* Fix white text on white background for autofill */
    .stTextInput input:-webkit-autofill,
    .stTextInput input:-webkit-autofill:hover,
    .stTextInput input:-webkit-autofill:focus,
    .stTextInput input:-webkit-autofill:active {
        -webkit-box-shadow: 0 0 0 30px #ffffff inset !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
    }
    .stTextInput input::placeholder { color: #888888 !important; }

    /* Primary button, sized to Apple's 44pt minimum tap target */
    .stButton button {
        background: var(--accent) !important;
        color: #10131A !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        min-height: 48px !important;
        transition: opacity 0.15s ease;
    }
    .stButton button:active { opacity: 0.75; }

    /* ---------------- Segmented controls (st.segmented_control) ---------------- */
    [data-baseweb="button-group"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        padding: 3px !important;
        gap: 2px !important;
    }
    [data-testid^="stBaseButton-segmented_control"] {
        border-radius: 10px !important;
        border: none !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        min-height: 38px !important;
    }
    [data-testid="stBaseButton-segmented_controlActive"] {
        background: var(--surface-strong) !important;
        color: var(--text) !important;
    }

    /* st.metric used for forecast days */
    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 0.7rem 0.4rem;
        text-align: center;
        min-width: 0;
        width: 100%;
    }
    [data-testid="stMetricLabel"] { 
        justify-content: center; 
        color: var(--text-secondary) !important;
        font-size: 0.75rem !important;
        white-space: nowrap;
    }
    [data-testid="stMetricValue"] { 
        justify-content: center; 
        font-family: var(--font-mono);
        font-size: 1.1rem !important;
    }
    [data-testid="stMetricDelta"] { 
        justify-content: center;
        font-size: 0.7rem !important;
    }

    /* ---------------- Weather card ---------------- */
    .weather-card {
        position: relative;
        background: var(--surface);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.4rem;
        margin: 0.4rem 0 1.4rem 0;
        overflow: hidden;
    }
    .weather-backdrop {
        position: absolute; inset: 0; z-index: 0;
        overflow: hidden; pointer-events: none;
    }
    .weather-card-content {
        position: relative; z-index: 1;
        display: flex; justify-content: space-between; align-items: flex-start;
        gap: 0.75rem; flex-wrap: wrap;
    }
    .weather-temp { font-family: var(--font-mono); font-size: 3rem; font-weight: 600; color: var(--accent); line-height: 1; }
    .weather-sub { display: flex; flex-wrap: wrap; gap: 0.9rem 1.3rem; font-size: 0.82rem; color: var(--text-secondary); margin-top: 0.6rem; }
    .weather-sub b { color: var(--text); font-weight: 600; }
    .weather-city { font-size: 1.15rem; font-weight: 700; color: var(--text); }
    .weather-condition { font-size: 0.88rem; color: var(--text-secondary); text-align: right; text-transform: capitalize; }

    /* ---------------- CSS-only ambient backdrop animations ---------------- */
    .p-rain { position: absolute; width: 1.5px; height: 16px; border-radius: 2px;
        background: linear-gradient(to bottom, rgba(123,147,190,0), rgba(123,147,190,0.5));
        animation: fallRain linear infinite; top: -20px; }
    @keyframes fallRain { to { transform: translateY(220px); } }

    .p-snow { position: absolute; width: 5px; height: 5px; border-radius: 50%;
        background: rgba(230,240,250,0.35); animation: fallSnow linear infinite; top: -10px; }
    @keyframes fallSnow { to { transform: translate(var(--drift, 10px), 220px); } }

    .p-cloud { position: absolute; width: 90px; height: 34px; border-radius: 50px;
        background: radial-gradient(ellipse at center, rgba(200,215,235,0.10), rgba(200,215,235,0) 70%);
        animation: driftCloud linear infinite; }
    @keyframes driftCloud { from { transform: translateX(-40px); } to { transform: translateX(340px); } }

    .p-sparkle { position: absolute; width: 3px; height: 3px; border-radius: 50%;
        background: rgba(255,205,110,0.55); animation: twinkle ease-in-out infinite; }
    @keyframes twinkle { 0%,100% { opacity: 0.15; transform: scale(1); } 50% { opacity: 0.7; transform: scale(1.8); } }

    .p-glow { position: absolute; inset: -20%; border-radius: 50%;
        background: radial-gradient(circle, rgba(123,147,190,0.10), rgba(123,147,190,0) 70%);
        animation: pulseGlow 6s ease-in-out infinite; }
    @keyframes pulseGlow { 0%,100% { opacity: 0.5; } 50% { opacity: 1; } }

    /* ---------------- Clothing rail ---------------- */
    .rail-track { display: flex; gap: 1.1rem; flex-wrap: wrap; justify-content: center; margin-top: 1rem; }
    .hanger-item { display: flex; flex-direction: column; align-items: center; opacity: 0;
        transform: translateY(-12px); animation: hangIn 0.5s cubic-bezier(.2,.9,.3,1.3) forwards; width: 64px; }
    .icon-wrap { width: 58px; height: 58px; border-radius: var(--radius-md); background: var(--surface);
        border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; }
    .icon-wrap img { max-width: 80%; max-height: 80%; object-fit: contain; border-radius: 8px; }
    .icon-wrap svg { width: 30px; height: 30px; }
    @keyframes hangIn { 0% { opacity: 0; transform: translateY(-14px) rotate(-5deg); } 100% { opacity: 1; transform: translateY(0) rotate(0deg); } }
    .hanger-label { font-size: 0.72rem; color: var(--text-secondary); margin-top: 0.4rem; text-align: center; line-height: 1.2; }

    /* Respect reduced-motion preferences */
    @media (prefers-reduced-motion: reduce) {
        .p-rain, .p-snow, .p-cloud, .p-sparkle, .p-glow, .hanger-item { animation: none !important; opacity: 1 !important; transform: none !important; }
    }

    /* ---------------- Responsive design ---------------- */
    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"], .block-container {
            max-width: 100%;
            padding: 1rem 0.8rem 2rem 0.8rem !important;
        }
        .cloak-hero h1 { font-size: 1.7rem; }
        .weather-temp { font-size: 2.8rem; }
        .weather-card { padding: 1.2rem 1rem; }
        .weather-sub { gap: 0.6rem 1rem; font-size: 0.75rem; }
        .rail-track { gap: 0.8rem; }
        .hanger-item { width: 54px; }
        .icon-wrap { width: 48px; height: 48px; }
        .icon-wrap svg { width: 24px; height: 24px; }
        .hanger-label { font-size: 0.65rem; }
    }

    @media (max-width: 480px) {
        .cloak-hero h1 { font-size: 1.4rem; }
        .weather-temp { font-size: 2.2rem; }
        .weather-card { padding: 1rem 0.8rem; }
        .weather-city { font-size: 1rem; }
        .weather-condition { font-size: 0.8rem; }
        .weather-sub { gap: 0.4rem 0.8rem; font-size: 0.7rem; }
        [data-testid="stMetricValue"] { font-size: 0.9rem !important; }
        [data-testid="stMetricLabel"] { font-size: 0.65rem !important; }
        .rail-track { gap: 0.6rem; }
        .hanger-item { width: 48px; }
        .icon-wrap { width: 42px; height: 42px; }
        .icon-wrap svg { width: 20px; height: 20px; }
        .hanger-label { font-size: 0.55rem; }
    }

    @media (min-width: 769px) {
        [data-testid="stMainBlockContainer"], .block-container {
            max-width: 520px;
            margin: 0 auto;
            padding: max(1.5rem, env(safe-area-inset-top)) 1.5rem 2.5rem 1.5rem !important;
        }
    }

    @media (max-width: 380px) {
        .cloak-hero h1 { font-size: 1.6rem; }
        .weather-temp { font-size: 2.5rem; }
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Icons — a single line-icon system (stroke-based, matches Apple's SF
# Symbols visual language) used everywhere instead of emoji.
# ---------------------------------------------------------------------------

_ICONS = {
    "heavy_coat": '<path d="M9 3l3 2 3-2 3 3-2 2 1 12H8L9 8 7 6z"/><path d="M9 8L5 10l1 5"/><path d="M15 8l4 2-1 5"/>',
    "tshirt": '<path d="M8 4L4 7l2 3 2-1v10h8V9l2 1 2-3-4-3-2 2h-4z"/>',
    "coat": '<path d="M9 4l3 2 3-2 3 3-2 2 1 11H8L9 9 7 7z"/><path d="M9 9L6 11l1 4"/><path d="M15 9l3 2-1 4"/><line x1="12" y1="10" x2="12" y2="20"/>',
    "jacket": '<path d="M9 4l3 2 3-2 3 3-2 3v10H8V10L6 7z"/>',
    "sweater": '<path d="M7 5l5-2 5 2v3l-2 1v11H9V9L7 8z"/>',
    "shorts": '<path d="M5 5h14l1 6-2 1v8h-4l-1-9-1 9H8v-8l-2-1z"/>',
    "scarf": '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M9 8l-2 12 4-2 2 2 2-2 4 2-2-12"/>',
    "gloves": '<path d="M7 10V6a2 2 0 014 0v3"/><path d="M11 9V5a2 2 0 014 0v4"/><path d="M15 9V6a2 2 0 014 0v6c0 4-3 7-6 7H9a4 4 0 01-4-4v-4a2 2 0 012-2h1"/>',
    "umbrella": '<path d="M4 11a8 8 0 0116 0z"/><line x1="12" y1="11" x2="12" y2="19"/><path d="M12 19a2 2 0 004 0"/>',
    "boots": '<path d="M8 3v9l-4 3v3h9v-4l3 1h4v-2l-5-2V3z"/>',
    "sunglasses": '<circle cx="7" cy="12" r="3.2"/><circle cx="17" cy="12" r="3.2"/><line x1="10.2" y1="11" x2="13.8" y2="11"/><path d="M4 11l-1.5-1M20 11l1.5-1"/>',
    "windbreaker": '<path d="M4 8h11a2.5 2.5 0 100-5"/><path d="M2 12h15a2.5 2.5 0 110 5"/><path d="M4 16h8a2 2 0 110 4"/>',
    "pants": '<path d="M4 4h16v2l-3 10v6H7v-6L4 6V4z"/>',
    "sneakers": '<path d="M3 12l2-6h14l2 6-2 4H5l-2-4z"/><path d="M3 12h18"/>',
    "hat": '<path d="M8 12l2-6h4l2 6"/><path d="M5 12h14v4H5z"/><circle cx="12" cy="10" r="2"/>',
    "water": '<path d="M12 2l-4 8 4 8 4-8-4-8z"/><path d="M12 2v16"/><path d="M8 10h8"/>',
    # UI / brand icons (replace former emoji usage)
    "hanger": '<path d="M12 3a2 2 0 012 2c0 .9-.6 1.6-1.4 1.9L12 8l-.6-1.1C10.6 6.6 10 5.9 10 5a2 2 0 012-2z"/><path d="M12 8l9 6-2 3-7-3-7 3-2-3z"/><path d="M5 17h14"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.9l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.9-.3 1.7 1.7 0 00-1 1.6V21a2 2 0 11-4 0v-.2a1.7 1.7 0 00-1-1.5 1.7 1.7 0 00-1.9.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.9 1.7 1.7 0 00-1.6-1H3a2 2 0 110-4h.2a1.7 1.7 0 001.5-1 1.7 1.7 0 00-.3-1.9l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.9.3H9a1.7 1.7 0 001-1.6V3a2 2 0 114 0v.2a1.7 1.7 0 001 1.6 1.7 1.7 0 001.9-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.9V9c.4.3 1 .5 1.6.5H21a2 2 0 110 4h-.2a1.7 1.7 0 00-1.6 1z"/>',
    "sun": '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.4M12 19.1v2.4M4.6 4.6l1.7 1.7M17.7 17.7l1.7 1.7M2.5 12h2.4M19.1 12h2.4M4.6 19.4l1.7-1.7M17.7 6.3l1.7-1.7"/>',
    "sun_cloud": '<path d="M8.5 3v2M4.6 5.6l1.4 1.4M13 4.4l-1.4 1.4"/><circle cx="8.5" cy="8.5" r="3"/><path d="M6 17h11a3.5 3.5 0 000-7 5 5 0 00-9.6-1.7A4 4 0 006 17z"/>',
    "sunset": '<path d="M4 15h16M6 15a6 6 0 0112 0"/><path d="M12 4v5M8.5 6.5l1.8 1.8M15.5 6.5l-1.8 1.8"/><path d="M3 19h18"/>',
    "moon_stars": '<path d="M15 3a7 7 0 100 14 6.5 6.5 0 01-5-11.9A7 7 0 0115 3z"/><path d="M19 3v3M17.5 4.5h3"/>',
    "settings_slider": '<line x1="4" y1="6" x2="20" y2="6"/><circle cx="9" cy="6" r="2"/><line x1="4" y1="12" x2="20" y2="12"/><circle cx="15" cy="12" r="2"/><line x1="4" y1="18" x2="20" y2="18"/><circle cx="7" cy="18" r="2"/>',
    "location": '<path d="M12 22s7-7.4 7-12a7 7 0 10-14 0c0 4.6 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
}


def get_icon_svg(key, color="currentColor", size=24):
    """Returns an inline stroke-icon SVG string. Falls back to an empty
    placeholder for unknown keys rather than raising, since this is used
    inside f-strings composed at render time."""
    body = _ICONS.get(key)
    if not body:
        return '<svg></svg>'
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'width="{size}" height="{size}">{body}</svg>')


def get_period_icon(period):
    """Maps a time-of-day period to a matching line icon instead of the
    previous sun/cloud/moon emoji glyphs."""
    mapping = {
        "morning": "sun",
        "afternoon": "sun_cloud",
        "evening": "sunset",
        "night": "moon_stars",
    }
    return get_icon_svg(mapping.get(period, "sun"), color="#FF9F45", size=30)


# ---------------------------------------------------------------------------
# CSS-only ambient weather backdrop (replaces the non-functional JS canvas)
# ---------------------------------------------------------------------------

def build_weather_backdrop(anim_type, seed=0):
    """Builds a small set of absolutely-positioned particles whose motion
    is driven entirely by CSS keyframes (see load_css). This renders
    reliably inside st.markdown, unlike the previous <script> based
    canvas animation, which browsers never execute when HTML is inserted
    this way."""
    rnd = random.Random(seed)
    spans = []

    if anim_type == "rain":
        for _ in range(28):
            left = rnd.uniform(0, 100)
            dur = rnd.uniform(0.6, 1.1)
            delay = rnd.uniform(0, 1.2)
            spans.append(f'<span class="p-rain" style="left:{left:.1f}%;animation-duration:{dur:.2f}s;animation-delay:-{delay:.2f}s;"></span>')
    elif anim_type == "snow":
        for _ in range(20):
            left = rnd.uniform(0, 100)
            dur = rnd.uniform(4, 7)
            delay = rnd.uniform(0, 5)
            drift = rnd.uniform(-20, 20)
            spans.append(f'<span class="p-snow" style="left:{left:.1f}%;--drift:{drift:.0f}px;animation-duration:{dur:.2f}s;animation-delay:-{delay:.2f}s;"></span>')
    elif anim_type == "cloud":
        for _ in range(5):
            top = rnd.uniform(0, 70)
            dur = rnd.uniform(18, 30)
            delay = rnd.uniform(0, 20)
            spans.append(f'<span class="p-cloud" style="top:{top:.0f}%;animation-duration:{dur:.1f}s;animation-delay:-{delay:.1f}s;"></span>')
    elif anim_type == "sparkle":
        for _ in range(16):
            left = rnd.uniform(0, 100)
            top = rnd.uniform(0, 100)
            dur = rnd.uniform(1.6, 3.2)
            delay = rnd.uniform(0, 3)
            spans.append(f'<span class="p-sparkle" style="left:{left:.1f}%;top:{top:.1f}%;animation-duration:{dur:.2f}s;animation-delay:-{delay:.2f}s;"></span>')
        spans.append('<span class="p-glow" style="top:-20%;right:-10%;"></span>')
    else:
        spans.append('<span class="p-glow" style="top:-10%;right:-10%;"></span>')

    return f'<div class="weather-backdrop">{"".join(spans)}</div>'


def display_outfit_recommendation(items):
    """Generates HTML for the outfit rail. Uses a real image from
    assets/clothes/ when one exists, otherwise falls back to the SVG
    icon set."""
    html_parts = ['<div class="rail-track">']
    asset_dir = "assets/clothes/"

    for i, (key, label, color, note) in enumerate(items):
        delay = i * 0.1
        icon_content = None
        img_path_jpg = f"{asset_dir}{key}.jpg"
        img_path_png = f"{asset_dir}{key}.png"

        try:
            if os.path.exists(img_path_jpg):
                import base64
                with open(img_path_jpg, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read()).decode()
                icon_content = f'<img src="data:image/jpeg;base64,{b64_string}" alt="{label}">'
            elif os.path.exists(img_path_png):
                import base64
                with open(img_path_png, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read()).decode()
                icon_content = f'<img src="data:image/png;base64,{b64_string}" alt="{label}">'
        except OSError:
            icon_content = None

        if icon_content is None:
            icon_content = get_icon_svg(key, color)

        html_parts.append(
            f'<div class="hanger-item" style="animation-delay:{delay}s;" title="{note}">'
            f'<div class="icon-wrap">{icon_content}</div>'
            f'<div class="hanger-label">{label}</div>'
            '</div>'
        )
    
    html_parts.append('</div>')
    return ''.join(html_parts)