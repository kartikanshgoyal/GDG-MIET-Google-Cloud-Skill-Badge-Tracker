import html
import streamlit as st

# Official Google Cloud Skill Badge artwork image (verified active 200 PNG)
DEFAULT_BADGE_IMAGE = "https://cdn.qwiklabs.com/9lB99Ij%2BMz%2FyOV0484V995beQHBMMCw0kimBFfZVtcM%3D"

def render_badge_card(badge):
    """
    Renders an accessible Dark Mode badge card with official badge artwork.
    Uses the verified official Google Cloud badge artwork for all badges.
    """
    is_completed = badge.get("completed", False)
    status_label = "Completed" if is_completed else "Not started"
    action_text = "View badge ↗" if is_completed else "Start badge ↗"

    title = html.escape(str(badge["title"]))
    category = html.escape(str(badge["category"]))
    course_url = html.escape(str(badge["course_url"]), quote=True)

    # Use fetched image if earned, otherwise the verified official Google Cloud badge artwork
    img_url = badge.get("image_url") or badge.get("fallback_image") or DEFAULT_BADGE_IMAGE
    img_url_escaped = html.escape(str(img_url), quote=True)
    
    completed_class = "completed-badge" if is_completed else "pending-badge"
    earned_date = html.escape(str(badge.get("earned_date", ""))) if badge.get("earned_date") else ""
    date_display = f'<span class="badge-date">({earned_date})</span>' if earned_date else ''

    img_html = f'<img src="{img_url_escaped}" alt="{title}" class="badge-artwork"/>'

    html_content = f"""
    <div class="custom-badge-card {completed_class}">
        <div class="card-left">
            {img_html}
        </div>
        <div class="card-right">
            <div class="card-header-meta">
                <span class="cat-pill">{category}</span>
            </div>
            <div class="card-title">{title}</div>
            <div class="card-footer-meta">
                <span class="status-indicator">{status_label} {date_display}</span>
                <a class="action-btn" href="{course_url}" target="_blank" rel="noopener noreferrer">{action_text}</a>
            </div>
        </div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)
