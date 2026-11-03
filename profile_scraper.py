import re
import requests
from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    """Normalize string for safe case-insensitive matching."""
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def extract_first_name(full_name: str) -> str:
    """Extracts only the first name cleanly, filtering out dummy/last names."""
    if not full_name or not full_name.strip():
        return "Learner"
    parts = full_name.strip().split()
    first = parts[0]
    # In case first name is something generic like 'Google', fallback gracefully
    return first.capitalize() if first else "Learner"

def fetch_profile_data(profile_url: str):
    """
    Fetches student info, earned badges, completion dates, and badge artwork from the public profile.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    try:
        response = requests.get(profile_url.strip(), headers=headers, timeout=12)
        
        if response.status_code == 404:
            return {
                "success": False,
                "status_code": 404,
                "error_type": "not_found",
                "message": "The profile could not be accessed. Make sure the profile is publicly visible."
            }
        elif response.status_code == 403:
            return {
                "success": False,
                "status_code": 403,
                "error_type": "access_denied",
                "message": "The profile could not be accessed. Make sure the profile is publicly visible."
            }
        elif response.status_code != 200:
            return {
                "success": False,
                "status_code": response.status_code,
                "error_type": "http_error",
                "message": "The profile could not be checked right now. Please try again."
            }

        soup = BeautifulSoup(response.text, "html.parser")
        
        # User name extraction (robust check for h1 or title)
        user_name_raw = None
        name_el = soup.find('h1', class_='ql-display-small') or soup.find('h1')
        if name_el:
            user_name_raw = name_el.get_text(strip=True)
        elif soup.title and '|' in soup.title.string:
            user_name_raw = soup.title.string.split('|')[0].strip()
        
        first_name = extract_first_name(user_name_raw) if user_name_raw else "Learner"

        # Avatar extraction
        avatar_el = soup.find('ql-avatar') or soup.find(class_=lambda x: x and 'avatar' in str(x).lower())
        avatar_url = avatar_el.get('src') if avatar_el else None

        # Badge extraction with images
        earned_badges = []
        
        # 1. Inspect .profile-badge divs (contains thumbnail image, title, and earned date)
        for badge_div in soup.find_all('div', class_='profile-badge'):
            title_span = badge_div.find('span', class_='ql-title-medium') or badge_div.find(['h3', 'h4', 'span'])
            date_span = badge_div.find('span', class_='ql-body-medium')
            img_tag = badge_div.find('img')
            
            if title_span:
                title = title_span.get_text(strip=True)
                date_str = date_span.get_text(strip=True) if date_span else ""
                img_src = img_tag.get('src') if img_tag else None
                earned_badges.append({
                    "title": title,
                    "date": date_str,
                    "image_url": img_src
                })

        # 2. Inspect modal dialogs (ql-dialog)
        for dialog in soup.find_all('ql-dialog'):
            headline = dialog.get('headline')
            if headline and not any(b["title"] == headline for b in earned_badges):
                earned_badges.append({
                    "title": headline,
                    "date": "",
                    "image_url": None
                })

        return {
            "success": True,
            "status_code": 200,
            "user_name": first_name,
            "avatar_url": avatar_url,
            "earned_badges": earned_badges,
            "error_type": None,
            "message": "Profile found. Campaign progress has been updated."
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status_code": None,
            "error_type": "timeout",
            "message": "Connection timed out while checking the profile. Please try again."
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "error_type": "network_error",
            "message": "The profile could not be checked right now. Please try again."
        }
