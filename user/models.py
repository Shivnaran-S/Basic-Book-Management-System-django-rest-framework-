from django.db import models
from books.models import Book
# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username