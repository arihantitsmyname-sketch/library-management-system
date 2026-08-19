from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('books/', views.view_books, name='view_books'),
    path('books/add/', views.add_book, name='add_book'),

    path('students/', views.view_students, name='view_students'),
    path('students/add/', views.add_student, name='add_student'),

    path('issue/', views.issue_book, name='issue_book'),
    path('return/', views.return_book, name='return_book'),
    path('issued/', views.view_issued_books, name='view_issued_books'),
]
