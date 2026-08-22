from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Book, Student, IssueRecord


def home(request):
    context = {
        'total_books': Book.objects.count(),
        'total_students': Student.objects.count(),
        'currently_issued': IssueRecord.objects.filter(return_date__isnull=True).count(),
    }
    return render(request, 'library_app/home.html', context)


# ---------- Books ----------

def view_books(request):
    books = Book.objects.all().order_by('book_id')
    return render(request, 'library_app/book_list.html', {'books': books})


def add_book(request):
    if request.method == 'POST':
        try:
            Book.objects.create(
                book_id=request.POST['book_id'],
                title=request.POST['title'],
                author=request.POST['author'],
                price=request.POST['price'],
                quantity=request.POST['quantity'],
            )
            messages.success(request, f"“{request.POST['title']}” was added to the catalog.")
            return redirect('view_books')
        except Exception as e:
            messages.error(request, f"Could not add book: {e}")
    return render(request, 'library_app/add_book.html')


def delete_book(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        book = get_object_or_404(Book, pk=book_id)

        still_out = IssueRecord.objects.filter(book_id=book, return_date__isnull=True).exists()
        if still_out:
            messages.error(
                request,
                f"Can't delete “{book.title}” — a copy is still checked out. Return it first."
            )
        else:
            title = book.title
            book.delete()
            messages.success(request, f"“{title}” was removed from the catalog.")

    return redirect('view_books')


# ---------- Students ----------

def view_students(request):
    students = Student.objects.all().order_by('admn_no')
    return render(request, 'library_app/student_list.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        try:
            Student.objects.create(
                admn_no=request.POST['admn_no'],
                name=request.POST['name'],
                student_class=request.POST['student_class'],
                section=request.POST['section'],
            )
            messages.success(request, f"{request.POST['name']} was added.")
            return redirect('view_students')
        except Exception as e:
            messages.error(request, f"Could not add student: {e}")
    return render(request, 'library_app/add_student.html')


def delete_student(request):
    if request.method == 'POST':
        admn_no = request.POST['admn_no']
        student = get_object_or_404(Student, pk=admn_no)

        still_out = IssueRecord.objects.filter(admn_no=student, return_date__isnull=True).exists()
        if still_out:
            messages.error(
                request,
                f"Can't delete {student.name} — they still have a book checked out. Return it first."
            )
        else:
            name = student.name
            student.delete()
            messages.success(request, f"{name} was removed from the members list.")

    return redirect('view_students')


# ---------- Issue / Return ----------

def issue_book(request):
    if request.method == 'POST':
        admn_no = request.POST['admn_no']
        book_id = request.POST['book_id']
        try:
            student = Student.objects.get(pk=admn_no)
            book = Book.objects.get(pk=book_id)

            if book.quantity <= 0:
                messages.error(request, f"“{book.title}” has no copies available right now.")
                return redirect('issue_book')

            IssueRecord.objects.create(
                admn_no=student,
                book_id=book,
                issue_date=date.today(),
                return_date=None,
            )
            book.quantity -= 1
            book.save()
            messages.success(request, f"“{book.title}” issued to {student.name}.")
            return redirect('view_issued_books')

        except Student.DoesNotExist:
            messages.error(request, "No student found with that admission number.")
        except Book.DoesNotExist:
            messages.error(request, "No book found with that ID.")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'library_app/issue_book.html')


def return_book(request):
    if request.method == 'POST':
        issue_id = request.POST['issue_id']
        try:
            record = IssueRecord.objects.get(pk=issue_id, return_date__isnull=True)
            record.return_date = date.today()
            record.save()

            book = record.book_id
            book.quantity += 1
            book.save()

            messages.success(request, f"“{book.title}” marked as returned.")
        except IssueRecord.DoesNotExist:
            messages.error(request, "Invalid issue ID, or that book was already returned.")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect('view_issued_books')

    return render(request, 'library_app/return_book.html')


def view_issued_books(request):
    records = IssueRecord.objects.select_related('admn_no', 'book_id').order_by('-issue_id')
    return render(request, 'library_app/issued_list.html', {'records': records})
