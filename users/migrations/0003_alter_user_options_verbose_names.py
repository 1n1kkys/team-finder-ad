import users.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_options_verbose_names'),
        ('users', '0002_alter_user_about_alter_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-date_joined',), 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=124, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='surname',
            field=models.CharField(max_length=124, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='avatars/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=12, unique=True, validators=[users.utils.validate_phone], verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='user',
            name='github_url',
            field=models.URLField(blank=True, default='', validators=[users.utils.validate_github_url], verbose_name='GitHub'),
        ),
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, default='', max_length=256, verbose_name='О себе'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='interested_users', to='projects.project', verbose_name='Избранные проекты'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата регистрации'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Сотрудник'),
        ),
    ]