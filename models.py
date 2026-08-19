from django.db import models


class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title


class Student(models.Model):
    admn_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    student_class = models.CharField(max_length=10, db_column='class')
    section = models.CharField(max_length=1)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return self.name


class IssueRecord(models.Model):
    issue_id = models.AutoField(primary_key=True)
    admn_no = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='admn_no')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='book_id')
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'issue_records'

    def __str__(self):
        return f"Issue #{self.issue_id}"
