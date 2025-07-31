from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm, RegisterForm
from .models import User
import logging

logger = logging.getLogger(__name__)


@method_decorator([csrf_protect, never_cache], name='dispatch')
class UserLoginView(LoginView):
    """Vue de connexion personnalisée avec redirection par rôle"""

    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirection selon le rôle de l'utilisateur"""
        user = self.request.user
        logger.info(f"Connexion réussie pour {user.username} ({user.get_role_display()})")

        if user.is_admin():
            messages.success(self.request, f"Bienvenue {user.get_full_name() or user.username} ! Vous êtes connecté en tant qu'administrateur.")
            return reverse_lazy('core:dashboard')
        else:
            messages.success(self.request, f"Bienvenue {user.get_full_name() or user.username} ! Vous êtes connecté à la caisse.")
            return reverse_lazy('core:caisse')

    def form_invalid(self, form):
        """Gestion des erreurs de connexion"""
        username = form.cleaned_data.get('username', 'Inconnu')
        logger.warning(f"Échec de connexion pour: {username}")
        messages.error(self.request, "Identifiants incorrects. Veuillez vérifier votre nom d'utilisateur/email et mot de passe.")
        return super().form_invalid(form)


@method_decorator([csrf_protect, never_cache], name='dispatch')
class UserRegisterView(CreateView):
    """Vue d'inscription des nouveaux utilisateurs"""

    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        """Rediriger les utilisateurs déjà connectés"""
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Traitement après inscription réussie"""
        response = super().form_valid(form)
        user = form.instance

        messages.success(
            self.request, 
            f"Compte créé avec succès pour {user.get_full_name()} ! "
            f"Vous pouvez maintenant vous connecter."
        )

        logger.info(f"Nouveau compte créé: {user.username} - {user.email} ({user.get_role_display()})")
        return response

    def form_invalid(self, form):
        """Gestion des erreurs d'inscription"""
        messages.error(self.request, "Erreur lors de la création du compte. Veuillez corriger les erreurs ci-dessous.")
        logger.warning(f"Échec de création de compte: {form.errors}")
        return super().form_invalid(form)


# SOLUTION POUR LA DÉCONNEXION
class UserLogoutView(View):
    """Vue de déconnexion personnalisée qui redirige vers la page de connexion Store Manager"""

    def get(self, request, *args, **kwargs):
        """Gérer les requêtes GET pour la déconnexion"""
        return self.logout_user(request)

    def post(self, request, *args, **kwargs):
        """Gérer les requêtes POST pour la déconnexion"""
        return self.logout_user(request)

    def logout_user(self, request):
        """Déconnecter l'utilisateur et rediriger vers la page de connexion"""
        if request.user.is_authenticated:
            username = request.user.username
            logger.info(f"Déconnexion de {username}")
            messages.success(request, f"Au revoir {username} ! Vous avez été déconnecté avec succès.")
            logout(request)

        # Redirection FORCÉE vers la page de connexion Store Manager
        return redirect('accounts:login')


# VUES POUR LA RÉCUPÉRATION DE MOT DE PASSE
class CustomPasswordResetView(PasswordResetView):
    """Vue personnalisée de demande de récupération de mot de passe"""
    template_name = 'accounts/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        """Email de récupération envoyé avec succès"""
        email = form.cleaned_data.get('email')
        logger.info(f"Demande de récupération de mot de passe pour: {email}")
        messages.success(
            self.request,
            f"Un email de récupération a été envoyé à {email}. Vérifiez votre boîte de réception et vos spams."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Erreur dans la demande de récupération"""
        logger.warning(f"Échec de demande de récupération: {form.errors}")
        messages.error(
            self.request,
            "Erreur lors de la demande de récupération. Vérifiez l'adresse email saisie."
        )
        return super().form_invalid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Vue de confirmation d'envoi de l'email de récupération"""
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Vue de saisie du nouveau mot de passe"""
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

    def form_valid(self, form):
        """Nouveau mot de passe défini avec succès"""
        user = form.user
        logger.info(f"Mot de passe réinitialisé pour l'utilisateur: {user.username}")
        messages.success(
            self.request,
            "Votre mot de passe a été modifié avec succès ! Vous pouvez maintenant vous connecter."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Erreur lors de la définition du nouveau mot de passe"""
        logger.warning(f"Échec de réinitialisation de mot de passe: {form.errors}")
        messages.error(
            self.request,
            "Erreur lors de la modification du mot de passe. Veuillez corriger les erreurs."
        )
        return super().form_invalid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Vue de confirmation de récupération réussie"""
    template_name = 'accounts/password_reset_complete.html'


# ALIAS POUR COMPATIBILITÉ
PasswordResetView = CustomPasswordResetView
PasswordResetDoneView = CustomPasswordResetDoneView
PasswordResetConfirmView = CustomPasswordResetConfirmView
PasswordResetCompleteView = CustomPasswordResetCompleteView
