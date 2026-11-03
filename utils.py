from urllib.parse import urlparse

def is_valid_profile_url(url: str) -> bool:
    """Check if the provided URL matches supported Google Cloud Skills Boost public profiles."""
    if not url:
        return False
    try:
        parsed = urlparse(url.strip())
        allowed_hosts = {
            "skills.google",
            "www.skills.google",
            "cloudskillsboost.google",
            "www.cloudskillsboost.google",
        }
        return (
            parsed.scheme in {"http", "https"}
            and parsed.hostname in allowed_hosts
            and "/public_profiles/" in parsed.path
        )
    except Exception:
        return False

def mask_profile_url(url: str) -> str:
    """Masks public profile identifier cleanly for privacy."""
    try:
        parsed = urlparse(url.strip())
        profile_id = parsed.path.rstrip("/").split("/")[-1]
        if len(profile_id) <= 10:
            masked_id = profile_id
        else:
            masked_id = f"{profile_id[:5]}...{profile_id[-4:]}"
        host = parsed.netloc.replace("www.", "")
        return f"{host}/public_profiles/{masked_id}"
    except Exception:
        return "skills.google/public_profiles/..."
