from rest_framework.urls import path
from .views import *
urlpatterns = [
    path("signup/",SignupUser.as_view(),name="user-signup"),
    path("signin/",SigninView.as_view(),name="user-signin"),
    path("details/",UserDetailsView.as_view(),name="user-detial")
]