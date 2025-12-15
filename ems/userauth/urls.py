from django.urls import path
from django.contrib.auth.views import LogoutView, RegisterView
from .views import CustomLoginView

app_name = 'userauth'
urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]