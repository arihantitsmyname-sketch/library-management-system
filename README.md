# Library Management System — Django Version

This is a Django + MySQL rewrite of the console-based library system.
Same database logic (add/view books & students, issue/return books) —
now with a proper web interface.

## 1. Install dependencies

Open a terminal in this folder and run:

```
pip install -r requirements.txt
```

> `mysqlclient` needs MySQL's dev headers installed on your machine.
> - Windows: usually installs fine via pip directly.
> - Mac: `brew install mysql-client` first, then pip install.
> - Linux: `sudo apt install default-libmysqlclient-dev` first.
>
> If you get stuck installing mysqlclient, you can swap to `pip install PyMySQL`
> instead and add this to the very top of `library_project/__init__.py`:
> ```python
> import pymysql
> pymysql.install_as_MySQLdb()
> ```

## 2. Configure your database credentials

Open `library_project/settings.py` and edit the `DATABASES` section
with your MySQL username/password (same ones you used in your original
Python script). The database itself (`library`) will be created for you
by MySQL if it doesn't exist — but you do need MySQL Server running.

If your MySQL user doesn't auto-create databases, run this once in
MySQL Workbench / CLI first:

```sql
CREATE DATABASE IF NOT EXISTS library;
```

## 3. Create the tables (migrations)

```
python manage.py makemigrations
python manage.py migrate
```

This creates the `books`, `students`, and `issue_records` tables —
same structure as your original script.

## 4. Run the server

```
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

## 5. (Optional) Admin panel

Django gives you a free admin panel to inspect/edit data directly:

```
python manage.py createsuperuser
```

Then visit **http://127.0.0.1:8000/admin/**

## Project structure

```
library_django/
├── manage.py
├── requirements.txt
├── library_project/       # settings, root URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── library_app/
│   ├── models.py          # Book, Student, IssueRecord
│   ├── views.py            # add/view/issue/return logic
│   ├── urls.py
│   ├── admin.py
│   └── templates/library_app/
│       ├── base.html       # sidebar nav + layout
│       ├── home.html
│       ├── book_list.html / add_book.html
│       ├── student_list.html / add_student.html
│       ├── issue_book.html / return_book.html
│       └── issued_list.html
└── static/css/style.css    # library card-catalog theme
```

## Notes for your project report

- Uses Django's ORM instead of raw SQL — `Book.objects.create(...)` generates
  the same `INSERT INTO books ...` your original script wrote by hand.
- Foreign keys (`admn_no`, `book_id` on `IssueRecord`) are enforced by MySQL,
  same as your original `FOREIGN KEY` constraints.
- Django's `messages` framework replaces your `print("Error:", e)` /
  `print("success")` lines with on-page banners.
- CSRF protection (`{% csrf_token %}`) is built into every form — something
  your console script didn't need, but any real web app does.
