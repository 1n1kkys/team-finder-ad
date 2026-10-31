import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

from team_finder import constants

PHONE_FORMAT_ERROR = (
    "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
)
PHONE_RE = re.compile(r"^(8\d{10}|\+7\d{10})$")


class GitHubUrlMixin:
    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url"))


def validate_github_url(url):
    if not url:
        return url
    host = (urlparse(url).hostname or "").lower()
    domain = constants.GITHUB_DOMAIN
    if host != domain and not host.endswith(f".{domain}"):
        raise ValidationError(f"Ссылка должна вести на {domain}")
    return url


def normalize_phone(phone):
    if not phone:
        raise ValidationError(PHONE_FORMAT_ERROR)
    compact = (
        str(phone)
        .strip()
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )
    if not PHONE_RE.fullmatch(compact):
        raise ValidationError(PHONE_FORMAT_ERROR)
    if compact.startswith("+7"):
        return "8" + compact[2:]
    return compact
