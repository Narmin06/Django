# 🎬 IMDB API (Django REST Framework)

IMDB-style movie database REST API with JWT auth, image upload, YouTube links,
ratings with auto-computed averages, search, filtering, pagination and a Top-10
endpoint.

## Stack
- Django 6 + Django REST Framework
- SimpleJWT (auth) · django-filter (filtering) · Pillow (image upload)
- drf-spectacular (OpenAPI schema + Swagger UI)

## Architecture
```
core/        # settings, root urls
users/       # registration + JWT auth
categories/  # Category CRUD
directors/   # Director CRUD
writers/     # Writer CRUD
movies/      # Movie CRUD + search/filter/top10 (image + youtube_link)
ratings/     # Rating CRUD (1 per user/movie, auto-updates movie average)
```

## Run
```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser   # optional, for /admin
uv run python manage.py runserver
```
- Swagger UI: http://127.0.0.1:8000/api/docs/
- OpenAPI schema: http://127.0.0.1:8000/api/schema/
- Admin: http://127.0.0.1:8000/admin/

## Auth
| Method | Endpoint              | Description              |
|--------|-----------------------|--------------------------|
| POST   | /api/auth/register/   | Create user              |
| POST   | /api/auth/login/      | Get access + refresh JWT |
| POST   | /api/auth/refresh/    | Refresh access token     |
| GET    | /api/auth/me/         | Current user (protected) |

Send the token on protected (write) requests:
`Authorization: Bearer <access_token>`

Read endpoints are **public**; create/update/delete require authentication.

## Resources (CRUD via REST)
`/api/categories/` · `/api/directors/` · `/api/writers/` · `/api/movies/` · `/api/ratings/`

Each supports: `GET` (list), `POST` (create), `GET /{id}/`, `PUT/PATCH /{id}/`, `DELETE /{id}/`.

## Movies — advanced features
| Feature            | Example                                      |
|--------------------|----------------------------------------------|
| Search by title    | `GET /api/movies/?search=dune`               |
| Filter by category | `GET /api/movies/?category=1`                |
| Filter by director | `GET /api/movies/?director=1`                |
| Filter by writer   | `GET /api/movies/?writer=1`                   |
| Filter by year     | `GET /api/movies/?year=2021`                 |
| Min rating         | `GET /api/movies/?min_rating=8`              |
| Ordering           | `GET /api/movies/?ordering=-average_rating`  |
| Pagination         | `GET /api/movies/?page=2` (10 per page)      |
| **Top 10**         | `GET /api/movies/top/`                        |

**Image upload + YouTube link:** `Movie.image` (multipart `image` field, stored
under `MEDIA_ROOT/movies/`) and `Movie.youtube_link` (validated YouTube URL).
For uploads send `multipart/form-data` instead of JSON.

## Ratings (business logic)
- A user can rate each movie **once** (unique `user`+`movie`); duplicates are rejected.
- Score is validated to `1–10`.
- On create/update/delete, the movie's `average_rating` and `rating_count` are
  recomputed automatically (`ratings/signals.py`).
- Users may only edit/delete **their own** ratings.

## Validation highlights
- Empty / whitespace-only names blocked everywhere.
- Movie `title` ≥ 2 chars, `content` ≥ 10 chars, `release_year` sanity-checked.
- `youtube_link` must contain `youtube.com` / `youtu.be`.
- Invalid FK references rejected by the serializers.
