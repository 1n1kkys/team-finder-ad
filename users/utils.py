import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

from team_finder import constants

PHONE_FORMAT_ERROR = (
    "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
)
PHONE_RE = re.compile(r"^(8\d{10}|\+7\d{10})$")


def validate_github_url(url):
    host = (urlparse(url).hostname or "").lower()
    domain = constants.GITHUB_DOMAIN
    if host != domain and not host.endswith(f".{domain}"):
        raise ValidationError(f"Ссылка должна вести на {domain}")


def validate_phone(phone):
    if not PHONE_RE.fullmatch(phone):
        raise ValidationError(PHONE_FORMAT_ERROR)


def normalize_phone(phone):
    if phone.startswith("+7"):
        return "8" + phone[2:]
    return phone
