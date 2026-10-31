# TeamFinder — платформа для поиска команд (вариант 1)

Сервис помогает находить команду для pet-проектов: опубликовать идею,
присоединиться к чужому проекту и сохранить понравившиеся проекты в избранное.

## Стек

- Python 3.12+, Django 5.2
- PostgreSQL 16 (Docker Compose, данные в volume)
- HTML / CSS / JavaScript из стартового набора, шаблоны `templates_var1`

## Быстрый старт для ревьюера

### 1. Зависимости

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

На Linux/macOS: `source venv/bin/activate`.

### 2. Переменные окружения

Windows:

```bash
copy .env_example .env
```

Linux и macOS:

```bash
cp .env_example .env
```

В `.env_example` уже стоит `TASK_VERSION=1` и `POSTGRES_PORT=5437`.
Значения `POSTGRES_*` совпадают с `docker-compose.yml`.

### 3. PostgreSQL

Нужен запущенный Docker Desktop.

```bash
docker compose up -d
```

База хранится в volume `postgres_data` и сохраняется после перезапуска контейнера.

### 4. Миграции и демо-данные

```bash
python manage.py migrate
python manage.py create_demo_data
```

Демо-пользователи, пароль у всех `demo12345`:

- `anna@example.com`
- `boris@example.com`
- `vera@example.com`

У каждого есть свой проект. Между ними уже проставлены участие и избранное,
чтобы на `/users/list/` были видны все четыре фильтра.

Админка (по желанию):

```bash
python manage.py createsuperuser
```

### 5. Запуск

```bash
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/

Админка: http://127.0.0.1:8000/admin/

## Что реализовано в варианте 1

- Сердечко на карточке и на странице проекта: `POST /projects/<id>/toggle-favorite/`
  отвечает `{"status": "ok", "favorited": true/false}`
- Страница избранного `/projects/favorites/` только для вошедшего пользователя
- На `/users/list/` четыре фильтра (только для авторизованных):
  - `?filter=owners-of-favorite-projects`
  - `?filter=owners-of-participating-projects`
  - `?filter=interested-in-my-projects`
  - `?filter=participants-of-my-projects`
- Гость смотрит проекты и профили. Создавать проекты, вступать и добавлять
  в избранное может только вошедший пользователь

## Замечания для ревьюера

- После регистрации открывается страница входа. Так записано в чек-листе сдачи.
- Участники на `/users/list/` отсортированы по дате регистрации, новые сверху.
  Так записано в чек-листе сдачи.
- Поле телефона в модели обязательное, а форма регистрации его не содержит.
  При регистрации сохраняется уникальный номер-заглушка. Настоящий номер
  задаётся в редактировании профиля: допускаются `8XXXXXXXXXX` и `+7XXXXXXXXXX`,
  номер уникальный, в базе хранится как `8XXXXXXXXXX`.
- Кнопка «Создать проект» на главной показана авторизованному пользователю.
- На странице избранного есть скрытый пустой блок: если снять последнее
  сердечко, подсказка появляется без перезагрузки.

## Автор

**Артём Молодцов**

- GitHub: [1n1kkys](https://github.com/1n1kkys)
- Email: [artem27042006@yandex.ru](mailto:artem27042006@yandex.ru)
