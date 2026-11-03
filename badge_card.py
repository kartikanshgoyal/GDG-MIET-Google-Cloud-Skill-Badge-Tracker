import html
import streamlit as st

def render_badge_card(badge):
    """
    Renders an accessible Dark Mode badge card with official badge artwork.
    No credit references whatsoever.
    """
    is_completed = badge.get("completed", False)
    status_label = "Completed" if is_completed else "Not started"
    action_text = "View badge ↗" if is_completed else "Start badge ↗"

    title = html.escape(str(badge["title"]))
    category = html.escape(str(badge["category"]))
    course_url = html.escape(str(badge["course_url"]), quote=True)
    icon = html.escape(str(badge.get("icon", "☁️")))

    # Use fetched image if earned, otherwise fallback campaign artwork
    img_url = badge.get("image_url") or badge.get("fallback_image")
    img_url_escaped = html.escape(str(img_url), quote=True) if img_url else ""
    
    completed_class = "completed-badge" if is_completed else "pending-badge"
    earned_date = html.escape(str(badge.get("earned_date", ""))) if badge.get("earned_date") else ""
    date_display = f'<span class="badge-date">({earned_date})</span>' if earned_date else ''

    img_html = f'<img src="{img_url_escaped}" alt="{title}" class="badge-artwork"/>' if img_url_escaped else f'<div class="badge-emoji-fallback">{icon}</div>'

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
