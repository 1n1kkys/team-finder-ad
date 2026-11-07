import django.db.models.deletion
import users.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_project_created_at_alter_project_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-created_at',), 'verbose_name': 'проект', 'verbose_name_plural': 'проекты'},
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_projects', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='project',
            name='github_url',
            field=models.URLField(blank=True, default='', validators=[users.utils.validate_github_url], verbose_name='GitHub'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('open', 'Открыт'), ('closed', 'Закрыт')], default='open', max_length=6, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='project',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participated_projects', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
    ]