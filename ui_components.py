# ui_components.py
import streamlit as st
import os
import random

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

    :root {
        --surface: rgba(255,255,255,0.08);
        --surface-strong: rgba(255,255,255,0.15);
        --border: rgba(255,255,255,0.2);
        --text: #FFFFFF;
        --text-secondary: rgba(255,255,255,0.8);
        --accent: #FF9F45;
        --accent-2: #5DDBC9;
        --radius-lg: 24px;
        --radius-md: 16px;
        --font-display: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
        --font-mono: ui-monospace, 'SF Mono', 'JetBrains Mono', monospace;
    }

    /* Reset and Base */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        font-family: var(--font-display);
        color: var(--text);
        transition: background 0.5s ease;
    }
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    /* Mobile-first layout */
    [data-testid="stMainBlockContainer"], .block-container {
        max-width: 480px;
        margin: 0 auto;
        padding: max(0.8rem, env(safe-area-inset-top)) 1.2rem 2.5rem 1.2rem !important;
    }

    /* --- Top Navigation Bar --- */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.2rem;
        color: var(--text);
        font-weight: 600;
        font-size: 1.1rem;
    }
    .top-nav span { cursor: default; }
    .top-nav .icon-btn { font-size: 1.4rem; }

    /* --- Glassmorphism Card --- */
    .glass-card {
        background: var(--surface);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.2rem;
        margin: 0.8rem 0;
    }
    .glass-card-light {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.15);
    }

    /* --- Big Weather Header --- */
    .weather-main {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
    }
    .weather-main .temp {
        font-family: var(--font-display);
        font-weight: 300;
        font-size: 5.5rem;
        line-height: 1;
        margin: 0;
        color: var(--text);
        letter-spacing: -0.02em;
    }
    .weather-main .condition {
        font-weight: 400;
        font-size: 1.25rem;
        margin-top: 0.5rem;
        color: var(--text-secondary);
    }
    .weather-main .loc {
        font-weight: 500;
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }

    /* --- Hourly Scroll --- */
    .hourly-scroll {
        display: flex;
        gap: 1.2rem;
        overflow-x: auto;
        padding: 0.5rem 0;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }
    .hourly-scroll::-webkit-scrollbar { display: none; }
    .hourly-item {
        flex: 0 0 70px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.3rem;
        color: var(--text);
        font-weight: 500;
    }
    .hourly-item img { width: 36px; height: 36px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1)); }
    .hourly-item .h-time { font-size: 0.8rem; opacity: 0.8; }
    .hourly-item .h-temp { font-size: 1rem; font-weight: 600; }

    /* --- Daily Vertical List --- */
    .daily-list .row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .daily-list .row:last-child { border-bottom: none; }
    .daily-list .day-col { display: flex; align-items: center; gap: 0.8rem; min-width: 120px; }
    .daily-list .day-date { font-size: 0.8rem; opacity: 0.6; min-width: 45px; }
    .daily-list .day-label { font-size: 1rem; font-weight: 500; }
    .daily-list .day-icon { width: 32px; height: 32px; }
    .daily-list .day-temps { font-size: 1rem; font-weight: 600; display: flex; gap: 0.8rem; }
    .daily-list .day-min { opacity: 0.6; font-weight: 400; }

    /* --- Details Grid --- */
    .detail-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        gap: 0.8rem;
        margin-top: 0.5rem;
    }
    .detail-item {
        text-align: center;
        padding: 0.6rem 0.1rem;
    }
    .detail-item .val { font-size: 1.1rem; font-weight: 600; }
    .detail-item .lbl { font-size: 0.75rem; opacity: 0.7; margin-top: 0.2rem; }

    /* --- Section Label --- */
    .section-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin: 1rem 0 0.2rem 0;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    /* --- Inputs & Buttons --- */
    .stTextInput input {
        background: rgba(255,255,255,0.15) !important;
        color: #fff !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        font-size: 16px !important;
        min-height: 48px;
    }
    .stTextInput input::placeholder { color: rgba(255,255,255,0.6) !important; }
    .stButton button {
        background: var(--accent) !important;
        color: #10131A !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        min-height: 48px !important;
        width: 100%;
    }

    /* --- Clothing Rail (Unchanged) --- */
    .rail-track { display: flex; gap: 1.1rem; flex-wrap: wrap; justify-content: center; margin-top: 1rem; }
    .hanger-item { display: flex; flex-direction: column; align-items: center; opacity: 0;
        transform: translateY(-12px); animation: hangIn 0.5s cubic-bezier(.2,.9,.3,1.3) forwards; width: 64px; }
    .icon-wrap { width: 58px; height: 58px; border-radius: var(--radius-md); background: rgba(255,255,255,0.08);
        border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; }
    .icon-wrap img, .icon-wrap svg { max-width: 70%; max-height: 70%; object-fit: contain; }
    @keyframes hangIn { 0% { opacity: 0; transform: translateY(-14px) rotate(-5deg); } 100% { opacity: 1; transform: translateY(0) rotate(0deg); } }
    .hanger-label { font-size: 0.7rem; opacity: 0.8; margin-top: 0.4rem; text-align: center; }

    @media (prefers-reduced-motion: reduce) { .hanger-item { animation: none !important; opacity: 1 !important; transform: none !important; } }
    </style>
    """, unsafe_allow_html=True)


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
    "hanger": '<path d="M12 3a2 2 0 012 2c0 .9-.6 1.6-1.4 1.9L12 8l-.6-1.1C10.6 6.6 10 5.9 10 5a2 2 0 012-2z"/><path d="M12 8l9 6-2 3-7-3-7 3-2-3z"/><path d="M5 17h14"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.9l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.9-.3 1.7 1.7 0 00-1 1.6V21a2 2 0 11-4 0v-.2a1.7 1.7 0 00-1-1.5 1.7 1.7 0 00-1.9.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.9 1.7 1.7 0 00-1.6-1H3a2 2 0 110-4h.2a1.7 1.7 0 001.5-1 1.7 1.7 0 00-.3-1.9l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.9.3H9a1.7 1.7 0 001-1.6V3a2 2 0 114 0v.2a1.7 1.7 0 001 1.6 1.7 1.7 0 001.9-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.9V9c.4.3 1 .5 1.6.5H21a2 2 0 110 4h-.2a1.7 1.7 0 00-1.6 1z"/>',
}
def get_icon_svg(key, color="#FFFFFF", size=24):
    body = _ICONS.get(key)
    if not body: return '<svg></svg>'
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'width="{size}" height="{size}">{body}</svg>')

def display_outfit_recommendation(items):
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
            pass
        if icon_content is None:
            icon_content = get_icon_svg(key, color=color)
        html_parts.append(
            f'<div class="hanger-item" style="animation-delay:{delay}s;" title="{note}">'
            f'<div class="icon-wrap">{icon_content}</div>'
            f'<div class="hanger-label">{label}</div></div>'
        )
    html_parts.append('</div>')
    return ''.join(html_parts)