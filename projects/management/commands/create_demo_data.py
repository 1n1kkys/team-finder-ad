from django.core.management.base import BaseCommand
from django.db import transaction

from projects.models import Project
from users.models import User


DEMO_USERS = [
    {
        "email": "anna@example.com",
        "name": "Анна",
        "surname": "Иванова",
        "phone": "89001112201",
        "password": "demo12345",
        "about": "Frontend-разработчик, люблю React и аккуратный UI.",
        "github_url": "https://github.com/anna-demo",
        "project": {
            "name": "Умный список задач",
            "description": (
                "Веб-приложение для совместного планирования задач "
                "с ролями и уведомлениями."
            ),
        },
    },
    {
        "email": "boris@example.com",
        "name": "Борис",
        "surname": "Смирнов",
        "phone": "89001112202",
        "password": "demo12345",
        "about": "Backend на Django и PostgreSQL.",
        "github_url": "https://github.com/boris-demo",
        "project": {
            "name": "API для pet-проектов",
            "description": (
                "REST API и админка для поиска команд и публикации идей."
            ),
        },
    },
    {
        "email": "vera@example.com",
        "name": "Вера",
        "surname": "Кузнецова",
        "phone": "89001112203",
        "password": "demo12345",
        "about": "UX/UI дизайнер, ищу команду для pet-проекта.",
        "github_url": "https://github.com/vera-demo",
        "project": {
            "name": "Дизайн-система TeamFinder",
            "description": (
                "Набор компонентов и гайдлайнов для быстрого старта UI."
            ),
        },
    },
]

PARTICIPATION = [
    ("boris@example.com", "Умный список задач"),
    ("vera@example.com", "API для pet-проектов"),
    ("anna@example.com", "Дизайн-система TeamFinder"),
]

FAVORITES = [
    ("anna@example.com", "API для pet-проектов"),
    ("anna@example.com", "Дизайн-система TeamFinder"),
    ("boris@example.com", "Умный список задач"),
    ("vera@example.com", "Умный список задач"),
    ("vera@example.com", "API для pet-проектов"),
]


class Command(BaseCommand):
    help = "Creates demo users and projects for variant 1"

    @transaction.atomic
    def handle(self, *args, **options):
        created_users = 0
        created_projects = 0

        for item in DEMO_USERS:
            user, user_created = User.objects.get_or_create(
                email=item["email"],
                defaults={
                    "name": item["name"],
                    "surname": item["surname"],
                    "phone": item["phone"],
                    "about": item["about"],
                    "github_url": item["github_url"],
                },
            )
            if user_created:
                user.set_password(item["password"])
                user.save()
                created_users += 1

            project_data = item["project"]
            project, project_created = Project.objects.get_or_create(
                name=project_data["name"],
                owner=user,
                defaults={
                    "description": project_data["description"],
                    "status": "open",
                    "github_url": item["github_url"],
                },
            )
            project.participants.add(user)
            if project_created:
                created_projects += 1

        for email, project_name in PARTICIPATION:
            user = User.objects.get(email=email)
            project = Project.objects.get(name=project_name)
            project.participants.add(user)

        for email, project_name in FAVORITES:
            user = User.objects.get(email=email)
            project = Project.objects.get(name=project_name)
            user.favorites.add(project)

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo ready: users +{created_users}, "
                f"projects +{created_projects}. "
                "Password for demo users: demo12345"
            )
        )
