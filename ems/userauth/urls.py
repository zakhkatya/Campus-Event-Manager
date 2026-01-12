from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterView, edit_profile_view 

app_name = 'userauth'
urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/edit/", edit_profile_view, name="edit-profile"), 
]