# Field lengths
MAX_LENGTH_NAME = 124
MAX_LENGTH_SURNAME = 124
MAX_LENGTH_PHONE = 12
MAX_LENGTH_ABOUT = 256
MAX_LENGTH_PROJECT_NAME = 200
MAX_LENGTH_STATUS = 6

# Project statuses
STATUS_OPEN = "open"
STATUS_CLOSED = "closed"
STATUS_CHOICES = [
    (STATUS_OPEN, "Открыт"),
    (STATUS_CLOSED, "Закрыт"),
]

# Pagination
PAGINATION_PAGE_SIZE = 12

# External URLs
GITHUB_DOMAIN = "github.com"

# Avatar generation. Colors stay muted so a white letter stays readable.
AVATAR_SIZE = (200, 200)
AVATAR_FONT_SIZE = 96
AVATAR_FONT_FILE = "static/fonts/Neue_Haas_Grotesk_Display_Pro_75_Bold.otf"
AVATAR_TEXT_COLOR = "white"
AVATAR_ANCHOR_OFFSET = 8
AVATAR_COLORS = (
    (70, 110, 130),
    (72, 118, 104),
    (120, 96, 86),
    (96, 92, 128),
    (122, 86, 98),
    (78, 108, 118),
)
