# Library Management System — Django Web Version

A Django-based Library Management System with books, students, issue and return tracking.

## Run locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000/

The local development fallback uses SQLite, so MySQL is not required for the deployment-ready version.

## Deploy on Render

Create a **Web Service** from this GitHub repository.

**Build Command**

```bash
./build.sh
```

**Start Command**

```bash
gunicorn library_project.wsgi:application
```

Choose the **Free** instance if available.

Create a Render PostgreSQL database and connect its `DATABASE_URL` to the web service. Also create a `SECRET_KEY` environment variable. Render automatically supplies `RENDER_EXTERNAL_HOSTNAME`.

## Important

The original local MySQL database is not copied automatically to the online PostgreSQL database. The deployment creates fresh Django tables using migrations. If you need your existing books/students/issue records online, export and import that data separately.
