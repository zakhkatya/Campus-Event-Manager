from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = "userauth/auth_home.html"
    redirect_authenticated_user = True
