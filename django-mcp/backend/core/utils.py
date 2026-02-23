import hashlib
import re
import secrets
import string


def generate_token(length: int = 32) -> str:
    """Cryptographically secure random URL-safe token."""
    return secrets.token_urlsafe(length)


def generate_otp(length: int = 6) -> str:
    """Numeric OTP suitable for 2FA / email verification."""
    return "".join(secrets.choice(string.digits) for _ in range(length))


def hash_value(value: str) -> str:
    """SHA-256 hash of a string (hex digest)."""
    return hashlib.sha256(value.encode()).hexdigest()


def slugify_unique(text: str, model_class, slug_field: str = "slug") -> str:
    """Generate a unique slug for a model by appending a counter if needed."""
    from django.utils.text import slugify

    base = slugify(text)
    slug = base
    counter = 1
    while model_class._default_manager.filter(**{slug_field: slug}).exists():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


def normalize_email(email: str) -> str:
    return email.strip().lower()


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def paginate_queryset(queryset, page: int, page_size: int = 20):
    """Simple offset-based slice; prefer DRF pagination in views."""
    start = (page - 1) * page_size
    return queryset[start : start + page_size]  # noqa: E203
