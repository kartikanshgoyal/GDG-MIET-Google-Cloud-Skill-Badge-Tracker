import json
import streamlit as st

from utils import is_valid_profile_url, mask_profile_url
from profile_scraper import fetch_profile_data, clean_text
from badge_card import render_badge_card

# -------------------------------------------------------------
# 1. Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="GDG on Campus MIET - Cloud Skill Badge Tracker",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# 2. Dark Mode Styles
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@400;500;700&display=swap');

    :root {
        --bg-color: #0b0f17;
        --card-bg: #151d2a;
        --border-color: #273449;
        --text-primary: #e8eaed;
        --text-secondary: #9aa0a6;
        --accent-blue: #8ab4f8;
        --accent-green: #81c995;
        --accent-yellow: #fdd663;
        --accent-red: #f28b82;
    }

    html, body, [class*="css"], .stApp {
        background-color: var(--bg-color) !important;
        color: var(--text-primary) !important;
        font-family: 'Google Sans', 'Roboto', sans-serif;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }

    /* Google 4-Color Strip */
    .color-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        height: 4px;
        border-radius: 4px;
        margin-bottom: 16px;
    }
    .strip-b { background: #4285F4; }
    .strip-r { background: #EA4335; }
    .strip-y { background: #FBBC04; }
    .strip-g { background: #34A853; }

    /* Headline */
    .app-header {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 24px;
    }
    .header-community-tag {
        color: var(--accent-blue);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .app-header h1 {
        color: #ffffff;
        font-size: 26px;
        font-weight: 700;
        margin: 0 0 6px 0;
        letter-spacing: -0.3px;
    }
    .app-header p {
        color: var(--text-secondary);
        font-size: 14px;
        margin: 0;
    }

    /* Form Card */
    div[data-testid="stForm"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        padding: 22px !important;
    }

    /* Text Input Alignment */
    div[data-testid="stTextInput"] {
        margin-bottom: 14px !important;
    }
    div[data-testid="stTextInput"] input {
        background-color: #0e141f !important;
        color: #ffffff !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
        height: 46px !important;
        line-height: normal !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px rgba(138, 180, 248, 0.25) !important;
    }
    div[data-testid="InputInstructions"] {
        display: none !important;
    }

    /* Buttons */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #1a73e8 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        height: 46px !important;
        min-height: 46px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        cursor: pointer !important;
        transition: background 0.15s ease !important;
    }
    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #1557b0 !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }
    div[data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }

    /* Badge Card */
    .custom-badge-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 14px;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 18px;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .custom-badge-card:hover {
        transform: translateY(-2px);
        border-color: var(--accent-blue);
    }
    .completed-badge {
        border-left: 5px solid var(--accent-green) !important;
        background: #12201b !important;
    }
    .pending-badge {
        border-left: 5px solid var(--border-color);
    }

    .card-left {
        width: 82px;
        height: 82px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .badge-artwork {
        width: 82px;
        height: 82px;
        object-fit: contain;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.04);
        padding: 4px;
    }
    .badge-emoji-fallback {
        font-size: 42px;
    }

    .card-right {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .card-header-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
    }
    .cat-pill {
        background: rgba(138, 180, 248, 0.12);
        color: var(--accent-blue);
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }
    .card-title {
        color: #ffffff;
        font-size: 15px;
        font-weight: 600;
        line-height: 1.35;
    }
    .card-footer-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 4px;
        gap: 8px;
        flex-wrap: wrap;
    }
    .status-indicator {
        font-size: 13px;
        font-weight: 600;
    }
    .completed-badge .status-indicator {
        color: var(--accent-green);
    }
    .pending-badge .status-indicator {
        color: var(--text-secondary);
    }
    .badge-date {
        font-size: 11px;
        color: #81c995;
        font-weight: normal;
        margin-left: 3px;
    }
    .action-btn {
        background: #1a73e8;
        color: #ffffff !important;
        text-decoration: none !important;
        padding: 7px 15px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        transition: background 0.15s ease;
    }
    .action-btn:hover {
        background: #1557b0;
    }

    .section-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Learner Profile Card */
    .learner-info-card {
        background: #121822;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 14px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .learner-avatar-box {
        width: 44px;
        height: 44px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .learner-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid var(--accent-blue);
    }
    /* WhatsApp-style Initial Letter Avatar */
    .learner-initial-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%);
        color: #ffffff;
        font-size: 20px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(26, 115, 232, 0.35);
        user-select: none;
        border: 2px solid rgba(255, 255, 255, 0.15);
    }
    .learner-details {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 2px;
        overflow: hidden;
    }
    .learner-name {
        font-weight: 700;
        font-size: 16px;
        color: #ffffff;
        line-height: 1.2;
    }
    .learner-url {
        font-size: 12px;
        color: var(--text-secondary);
        font-family: monospace;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# 3. Application State & URL Parameter Memory
# -------------------------------------------------------------
query_params = st.query_params

if "saved_profile_url" not in st.session_state:
    st.session_state.saved_profile_url = query_params.get("profile", "")

if "profile_data" not in st.session_state:
    st.session_state.profile_data = None

# If user comes back with ?profile=... in URL, auto-load their profile
if st.session_state.saved_profile_url and not st.session_state.profile_data:
    if is_valid_profile_url(st.session_state.saved_profile_url):
        with st.spinner("Restoring your saved profile..."):
            initial_fetch = fetch_profile_data(st.session_state.saved_profile_url)
            if initial_fetch["success"]:
                st.session_state.profile_data = initial_fetch

@st.cache_data
def load_campaign_badges():
    with open("data/campaign_badges.json", "r", encoding="utf-8") as f:
        return json.load(f)

raw_badges = load_campaign_badges()

# -------------------------------------------------------------
# 4. Top Accent Strip & Header (GDG on Campus MIET)
# -------------------------------------------------------------
st.markdown("""
<div class="color-strip">
    <div class="strip-b"></div>
    <div class="strip-r"></div>
    <div class="strip-y"></div>
    <div class="strip-g"></div>
</div>

<div class="app-header">
    <div class="header-community-tag">GDG on Campus MIET</div>
    <h1>☁️ Google Cloud Skill Badge Tracker</h1>
    <p>Track your campaign badges and completion progress automatically from your public Google Skills Boost profile.</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. Two-Column Layout
# Left Column: Profile Input & Stats (1.1)
# Right Column: Upper (Fetched Badges) & Bottom (Remaining Badges) (2.4)
# -------------------------------------------------------------
col_left, col_right = st.columns([1.1, 2.4], gap="large")

# =============================================================
# LEFT COLUMN: Profile Form & Progress
# =============================================================
with col_left:
    st.markdown('<div class="section-title">👤 Public Profile Check</div>', unsafe_allow_html=True)
    
    with st.form("profile_form"):
        st.write("Enter your public Google Skills Boost profile URL:")
        profile_url_input = st.text_input(
            "Profile URL",
            value=st.session_state.saved_profile_url,
            placeholder="https://www.skills.google/public_profiles/your-id",
            label_visibility="collapsed"
        )
        
        submitted = st.form_submit_button("🚀 Check My Progress", use_container_width=True)

    # Form Submission handling
    if submitted:
        cleaned_url = profile_url_input.strip()
        if not cleaned_url:
            st.warning("⚠️ Please paste your public profile link.")
        elif not is_valid_profile_url(cleaned_url):
            st.error("❌ Please enter a valid public Google Cloud Skills Boost profile URL.")
        else:
            with st.spinner("Fetching profile data..."):
                fetch_result = fetch_profile_data(cleaned_url)
                if fetch_result["success"]:
                    st.session_state.profile_data = fetch_result
                    st.session_state.saved_profile_url = cleaned_url
                    # Persist user URL in browser query parameters so it's remembered when they come back
                    st.query_params["profile"] = cleaned_url
                    st.success("✅ Profile verified & saved!")
                else:
                    st.error(fetch_result.get("message", "Error checking profile."))

    # Automatic Profile Evaluation
    completed_badge_ids = set()
    badge_dates_map = {}
    badge_images_map = {}

    if st.session_state.profile_data and st.session_state.profile_data.get("success"):
        earned_list = st.session_state.profile_data.get("earned_badges", [])
        
        for badge in raw_badges:
            norm_title = clean_text(badge["title"])
            for earned in earned_list:
                norm_earned = clean_text(earned["title"])
                if norm_title == norm_earned or norm_title in norm_earned or norm_earned in norm_title:
                    completed_badge_ids.add(badge["id"])
                    badge_dates_map[badge["id"]] = earned.get("date", "")
                    if earned.get("image_url"):
                        badge_images_map[badge["id"]] = earned.get("image_url")
                    break

    # Build badge objects
    processed_badges = []
    for b in raw_badges:
        b_copy = dict(b)
        is_done = b["id"] in completed_badge_ids
        b_copy["completed"] = is_done
        b_copy["earned_date"] = badge_dates_map.get(b["id"], "")
        if b["id"] in badge_images_map:
            b_copy["image_url"] = badge_images_map[b["id"]]
        processed_badges.append(b_copy)

    total_badges = len(processed_badges)
    completed_count = len(completed_badge_ids)
    remaining_count = total_badges - completed_count
    completion_rate = int((completed_count / total_badges) * 100) if total_badges else 0

    # Display Learner Card (With WhatsApp-style Initial fallback & Only First Name)
    if st.session_state.profile_data and st.session_state.profile_data.get("success"):
        first_name = st.session_state.profile_data.get("user_name", "Learner")
        avatar = st.session_state.profile_data.get("avatar_url")
        first_letter = first_name[0].upper() if first_name else "U"
        
        masked_id = mask_profile_url(st.session_state.saved_profile_url)
        
        if avatar and avatar.strip() and "default" not in avatar.lower():
            avatar_html = f'<img src="{avatar}" class="learner-avatar" alt="{first_name}"/>'
        else:
            avatar_html = f'<div class="learner-initial-avatar">{first_letter}</div>'
        
        card_markup = (
            f'<div class="learner-info-card">'
            f'<div class="learner-avatar-box">{avatar_html}</div>'
            f'<div class="learner-details">'
            f'<div class="learner-name">{first_name}</div>'
            f'<div class="learner-url">{masked_id}</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card_markup, unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="section-title">📊 Progress Metrics</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    m1.metric("Completed", f"{completed_count} / {total_badges}")
    m2.metric("Remaining", f"{remaining_count} badges")

    st.metric("Completion Rate", f"{completion_rate}%")

    st.write("")
    st.caption(f"Campaign Progress: {completion_rate}%")
    st.progress(completed_count / total_badges if total_badges else 0)

    st.write("")
    # Guide button / expander on how to use & make profile public
    with st.expander("📖 Guide: How to use & find your profile"):
        st.markdown("""
        **Step-by-step instructions:**
        1. Open [Google Cloud Skills Boost](https://www.cloudskillsboost.google) or [Google Skills](https://www.skills.google).
        2. Sign in with your registered college account.
        3. Click your **profile avatar** in the top-right corner and select **Profile**.
        4. Make sure your profile is set to **Public** by clicking **Share your profile**.
        5. Copy your public link (looks like: `https://www.skills.google/public_profiles/...`).
        6. Paste the link into the box above and click **🚀 Check My Progress**.
        """)

# =============================================================
# RIGHT COLUMN: Fetched Badges (Top) & Remaining Badges (Bottom)
# =============================================================
with col_right:
    completed_badges = [b for b in processed_badges if b["completed"]]
    remaining_badges = [b for b in processed_badges if not b["completed"]]

    # 1. UPPER RIGHT: Fetched / Completed Badges
    st.markdown(
        f'<div class="section-title">🏆 Fetched Badges ({len(completed_badges)})</div>',
        unsafe_allow_html=True
    )

    if completed_badges:
        for badge in completed_badges:
            render_badge_card(badge)
    else:
        st.info("No badges completed yet. Paste your profile on the left and click 'Check My Progress'!")

    st.write("")
    st.markdown("---")

    # 2. BOTTOM RIGHT: Remaining / Not Started Badges
    st.markdown(
        f'<div class="section-title">🎯 Remaining Badges ({len(remaining_badges)})</div>',
        unsafe_allow_html=True
    )

    if remaining_badges:
        for badge in remaining_badges:
            render_badge_card(badge)
    else:
        st.success("🎉 Outstanding! You have completed all 10 Google Cloud Skill Badges!")
