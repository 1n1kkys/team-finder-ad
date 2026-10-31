import io
import random
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont

from team_finder import constants
from users.managers import UserManager
from users.utils import normalize_phone, validate_github_url


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=constants.MAX_LENGTH_NAME)
    surname = models.CharField(max_length=constants.MAX_LENGTH_SURNAME)
    avatar = models.ImageField(upload_to="avatars/")
    phone = models.CharField(
        max_length=constants.MAX_LENGTH_PHONE,
        unique=True,
    )
    github_url = models.URLField(blank=True, default="")
    about = models.TextField(
        max_length=constants.MAX_LENGTH_ABOUT,
        blank=True,
        default="",
    )
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

    def clean(self):
        super().clean()
        if self.github_url:
            self.github_url = validate_github_url(self.github_url)
        if self.phone:
            try:
                self.phone = normalize_phone(self.phone)
            except ValidationError as error:
                raise ValidationError({"phone": error.messages}) from error
            taken = User.objects.filter(phone=self.phone)
            if self.pk:
                taken = taken.exclude(pk=self.pk)
            if taken.exists():
                raise ValidationError(
                    {"phone": "Этот номер телефона уже используется"}
                )

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = self.generate_avatar()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:user_detail", kwargs={"user_id": self.pk})

    def generate_avatar(self):
        size = constants.AVATAR_SIZE
        bg_color = random.choice(constants.AVATAR_COLORS)
        img = Image.new("RGB", size, color=bg_color)
        draw = ImageDraw.Draw(img)
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
        img.save(buffer, format="PNG")
        return ContentFile(
            buffer.getvalue(),
            name=f"avatar_{uuid.uuid4()}.png",
        )
