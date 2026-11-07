from django.conf import settings
from django.db import models
from django.urls import reverse

from team_finder import constants
from users.utils import validate_github_url


class Project(models.Model):
    name = models.CharField(
        "Название",
        max_length=constants.MAX_LENGTH_PROJECT_NAME,
    )
    description = models.TextField("Описание", blank=True, default="")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True,
    )
    github_url = models.URLField(
        "GitHub",
        blank=True,
        default="",
        validators=[validate_github_url],
    )
    status = models.CharField(
        "Статус",
        max_length=constants.MAX_LENGTH_STATUS,
        choices=constants.STATUS_CHOICES,
        default=constants.STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Участники",
        related_name="participated_projects",
        blank=True,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "projects:project_detail",
            kwargs={"project_id": self.pk},
        )