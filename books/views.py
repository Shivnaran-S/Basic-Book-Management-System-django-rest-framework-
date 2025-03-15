from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Author, Genre, Book
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_object_by_isbn(self, isbn):
        """
        Retrieve a book instance based on the isbn.
        """
        try:
            return Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            raise NotFound(f"Book with ISBN {isbn} not found.")
        
    def update(self, request, *args, **kwargs):
        isbn = request.data.get('isbn')
        
        if not isbn:
            return Response({"detail": "ISBN is required to update a book."}, status=status.HTTP_400_BAD_REQUEST)

        book = self.get_object_by_isbn(isbn)
        
        # If a book is found by ISBN, update it
        serializer = BookSerializer(book, data=request.data)  # partial=True allows for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # detail=True: The action is related to a specific object, and the URL expects an object identifier (like /books/<id>/)
    # # detail=False: The action will be applied to the collection of resources (i.e., the endpoint /books/), not to a specific resource (like /books/<id>/) 
    @action(detail=False, methods=['delete'], url_path='delete_by_isbn') 
    def delete_by_isbn(self, request):
        """
        Custom DELETE action to delete a book based on ISBN.
        """
        isbn = request.data.get('isbn')
        
        if not isbn:
            return Response({"detail": "ISBN is required to delete a book."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book = self.get_object_by_isbn(isbn)
            book.delete()
            return Response({"detail": f"Book with ISBN {isbn} deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"detail": "Book not found with the provided ISBN."}, status=status.HTTP_404_NOT_FOUND)