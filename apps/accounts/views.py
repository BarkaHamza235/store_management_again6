from django.shortcuts import redirect
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from .forms import LoginForm, RegisterForm
from .models import User
import logging

logger = logging.getLogger(__name__)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        # Adapte selon tes règles de rôles
        if hasattr(user, 'is_admin') and user.is_admin():
            return reverse_lazy('core:dashboard')
        return reverse_lazy('core:caisse')


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Compte créé avec succès, vous pouvez vous connecter.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Erreur dans le formulaire, vérifiez vos informations.")
        return super().form_invalid(form)


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        return self.logout_user(request)
    def post(self, request, *args, **kwargs):
        return self.logout_user(request)
    def logout_user(self, request):
        logout(request)
        messages.success(request, "Vous êtes bien déconnecté.")
        return redirect('accounts:login')


# ---------------------- MOT DE PASSE OUBLIÉ ------------------------

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        messages.success(self.request, "Un email de réinitialisation a été envoyé, vérifiez vos mails & spams.")
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

# Alias (important en cas d'import sauvage)
PasswordResetView = CustomPasswordResetView
PasswordResetDoneView = CustomPasswordResetDoneView
PasswordResetConfirmView = CustomPasswordResetConfirmView
PasswordResetCompleteView = CustomPasswordResetCompleteView
