from django.contrib.auth.models import User
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=255, default="No description provided.")
    published_date = models.DateField()
    isbn_number = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
