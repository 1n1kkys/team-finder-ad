from django.conf import settings
from django.db import models
from django.urls import reverse

from team_finder import constants
from users.utils import validate_github_url


class Project(models.Model):
    name = models.CharField(max_length=constants.MAX_LENGTH_PROJECT_NAME)
    description = models.TextField(blank=True, default="")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    github_url = models.URLField(blank=True, default="")
    status = models.CharField(
        max_length=constants.MAX_LENGTH_STATUS,
        choices=constants.STATUS_CHOICES,
        default=constants.STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def clean(self):
        super().clean()
        if self.github_url:
            self.github_url = validate_github_url(self.github_url)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "projects:project_detail",
            kwargs={"project_id": self.pk},
        )
