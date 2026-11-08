import io
import random
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont

from team_finder import constants
from users.managers import UserManager
from users.utils import validate_github_url, validate_phone


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True)
    name = models.CharField("Имя", max_length=constants.MAX_LENGTH_NAME)
    surname = models.CharField(
        "Фамилия",
        max_length=constants.MAX_LENGTH_SURNAME,
    )
    avatar = models.ImageField("Аватар", upload_to="avatars/")
    phone = models.CharField(
        "Телефон",
        max_length=constants.MAX_LENGTH_PHONE,
        unique=True,
        validators=[validate_phone],
    )
    github_url = models.URLField(
        "GitHub",
        blank=True,
        default="",
        validators=[validate_github_url],
    )
    about = models.TextField(
        "О себе",
        max_length=constants.MAX_LENGTH_ABOUT,
        blank=True,
        default="",
    )
    favorites = models.ManyToManyField(
        "projects.Project",
        verbose_name="Избранные проекты",
        related_name="interested_users",
        blank=True,
    )
    date_joined = models.DateTimeField(
        "Дата регистрации",
        auto_now_add=True,
        db_index=True,
    )
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Сотрудник", default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    class Meta:
        ordering = ("-date_joined",)
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = self.generate_avatar()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:user_detail", kwargs={"user_id": self.pk})

    def generate_avatar(self):
        size = constants.AVATAR_SIZE
        background_color = random.choice(constants.AVATAR_COLORS)
        image = Image.new("RGB", size, color=background_color)
        draw = ImageDraw.Draw(image)
        letter = self.name[0].upper() if self.name else "U"
        font_path = settings.BASE_DIR / constants.AVATAR_FONT_FILE

        try:
            font = ImageFont.truetype(
                str(font_path),
                constants.AVATAR_FONT_SIZE,
            )
        except OSError:
            font = ImageFont.load_default()

        try:
            left, top, right, bottom = draw.textbbox((0, 0), letter, font=font)
            width, height = right - left, bottom - top
        except AttributeError:
            width, height = draw.textsize(letter, font=font)

        draw.text(
            (
                (size[0] - width) / 2,
                (size[1] - height) / 2 - constants.AVATAR_ANCHOR_OFFSET,
            ),
            letter,
            fill=constants.AVATAR_TEXT_COLOR,
            font=font,
        )

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return ContentFile(
            buffer.getvalue(),
            name=f"avatar_{uuid.uuid4()}.png",
        )
