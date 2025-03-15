from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255) # CharField for short-to-moderate text (e.g., names, titles)
    bio = models.TextField(blank=True, null=True) # TextField for large blocks of text (e.g., descriptions, comments, or long content) blank for forms and null for database

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)

    authors = models.ManyToManyField(Author, related_name='books') # reverse lookups: From author side - author.books.all() instead of author.book_set.all()

    isbn = models.CharField(max_length=13, unique=True, help_text="Enter a valid ISBN (10 or 13 digits)")
    publication_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)

    summary = models.TextField(blank=True, null=True)
    number_of_pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    #cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, blank=True) # implied that blank is true
    created_at = models.DateTimeField(auto_now_add=True) # auto field user/admin need not provide any info
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title