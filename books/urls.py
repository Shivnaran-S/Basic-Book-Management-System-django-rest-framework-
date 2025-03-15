from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, GenreViewSet, BookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)

urlpatterns = router.urls
urlpatterns += [
    #path('', include(router.urls)),
    path('books/update_by_isbn/',BookViewSet.as_view({'put': 'update'}), name='update-book-by-isbn'),
]
