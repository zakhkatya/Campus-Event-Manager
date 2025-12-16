# userauth/views.py

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect 
from django.contrib.auth import logout 
from .forms import CustomRegistrationForm

class CustomLoginView(LoginView):
    template_name = "userauth/login.html"
    redirect_authenticated_user = True 

class RegisterView(CreateView):
    template_name = "userauth/register.html"
    form_class = CustomRegistrationForm
    success_url = reverse_lazy("userauth:login")

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user.is_authenticated:
            logout(self.request) 

        return HttpResponseRedirect(self.get_success_url())