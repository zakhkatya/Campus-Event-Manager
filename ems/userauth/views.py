# userauth/views.py

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect 
from django.contrib.auth import logout 
from .forms import CustomRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CustomLoginView(LoginView):
    template_name = "userauth/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User Login"
        return context


class RegisterView(CreateView):
    template_name = "userauth/register.html"
    form_class = CustomRegistrationForm
    success_url = reverse_lazy("userauth:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User Registration"
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user.is_authenticated:
            logout(self.request)
        return HttpResponseRedirect(self.get_success_url())
    
@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            changed_fields = form.changed_data
            user = form.save(commit=False)
            new_pwd = form.cleaned_data.get('new_password')
            
            if new_pwd:
                try:
                    validate_password(new_pwd, user)
                    user.set_password(new_pwd)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.info(request, "Your password has been successfully updated.")
                except ValidationError as e:
                    for error in e.messages:
                        messages.error(request, error)
                    return render(request, "userauth/edit_profile.html", {"form": form})
            
            elif 'avatar' in changed_fields:
                user.save()
                messages.info(request, "Your profile photo has been updated.")
            
            elif any(field in changed_fields for field in ['first_name', 'last_name', 'email']):
                user.save()
                messages.info(request, "Your profile information has been updated.")
            
            else:
                user.save()
            
            return redirect("userauth:edit-profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, "userauth/edit_profile.html", {"form": form})