# Company Website Backend (Django + DRF)

Production-oriented Django REST Framework backend with full CRUD APIs for homepage stats, services, news (with ordered images), and projects (with execution list and ordered images).

## Features

- Django + Django REST Framework
- SQLite (development default)
- Media file upload with `MEDIA_ROOT` and `MEDIA_URL`
- Django admin support
- `ModelViewSet` + `DefaultRouter`
- Multipart form-data support for image uploads
- CORS support (configurable by env vars)
- Nested images in API responses for News and Projects
- Multiple image upload for News/Projects using `uploaded_images`

## Project Structure

- `api/models.py` — models
- `api/serializers.py` — serializers + nested output + multipart upload handling
- `api/views.py` — DRF viewsets
- `api/urls.py` — router endpoints
- `api/admin.py` — admin registration

## Setup (Development)

```bash
cd company_site
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Base URL: `http://127.0.0.1:8000`

## Environment Variables

The project is now configurable for deployment:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (`False` for production)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `CORS_ALLOW_ALL_ORIGINS` (`False` for production)
- `CORS_ALLOWED_ORIGINS` (comma-separated, required when not allowing all)
- `SQLITE_NAME` (optional sqlite filename)

See `.env.example`.

## API Endpoints

- `GET/POST /api/homepage/`
- `GET/PUT/PATCH/DELETE /api/homepage/{id}/`
- `GET/POST /api/services/`
- `GET/PUT/PATCH/DELETE /api/services/{id}/`
- `GET/POST /api/contact/`
- `GET/PUT/PATCH/DELETE /api/contact/{id}/`
- `GET/POST /api/news/`
- `GET/PUT/PATCH/DELETE /api/news/{id}/`
- `GET/POST /api/projects/`
- `GET/PUT/PATCH/DELETE /api/projects/{id}/`

## cURL Examples

### HomepageStats Create

```bash
curl -X POST http://127.0.0.1:8000/api/homepage/ \
  -H "Content-Type: application/json" \
  -d '{
    "projects_executed": 120,
    "field_personnel": 55,
    "clients_partners": 30,
    "operational_locations": 8
  }'
```

### Service Create with Images

```bash
curl -X POST http://127.0.0.1:8000/api/services/ \
  -F "name=Engineering" \
  -F "text=Full engineering service" \
  -F "first_image=@/path/to/first.jpg" \
  -F "second_image=@/path/to/second.jpg"
```


### Contact Form Submission

```bash
curl -X POST http://127.0.0.1:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone_number": "+1-555-100-200",
    "service": "Engineering",
    "description": "Please contact me about a project quote."
  }'
```

### News Create with Multiple Ordered Images

```bash
curl -X POST http://127.0.0.1:8000/api/news/ \
  -F "title=New Plant Opened" \
  -F "content=Project details and announcement." \
  -F "is_hidden=false" \
  -F "author=Admin" \
  -F "uploaded_images=@/path/to/news1.jpg" \
  -F "uploaded_images=@/path/to/news2.jpg"
```

### Project Create with Execution JSON List + Multiple Images

```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -F "title=Pipeline Upgrade" \
  -F "status=active" \
  -F "client=Example Client" \
  -F "scope=Upgrade regional pipeline" \
  -F 'execution=["Site survey", "Procurement", "Deployment"]' \
  -F "outcome=Increased throughput by 20%" \
  -F "uploaded_images=@/path/to/project1.jpg" \
  -F "uploaded_images=@/path/to/project2.jpg"
```

## Deployment Notes

- Set `DJANGO_DEBUG=False`.
- Set a strong `DJANGO_SECRET_KEY`.
- Restrict `DJANGO_ALLOWED_HOSTS` and CORS origins.
- Run migrations and static collection:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

- Start with gunicorn:

```bash
gunicorn company_site.wsgi:application --bind 0.0.0.0:8000
```
