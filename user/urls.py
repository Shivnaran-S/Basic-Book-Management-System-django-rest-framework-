from django.urls import path
from .views import UserView, UserViewWithIds

urlpatterns = [
    path("",UserView.as_view(), name="user-list"),
    path("<int:id>", UserViewWithIds.as_view(), name="user-get")
]