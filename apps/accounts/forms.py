from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User
import logging

logger = logging.getLogger(__name__)


class LoginForm(AuthenticationForm):
    """Formulaire de connexion personnalisé avec logging"""

    username = forms.CharField(
        label="Nom d'utilisateur ou Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Votre nom d'utilisateur ou email",
            'autofocus': True
        })
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Votre mot de passe"
        })
    )

    remember_me = forms.BooleanField(
        label="Se souvenir de moi",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    error_messages = {
        'invalid_login': 'Nom d\'utilisateur/email ou mot de passe incorrect.',
        'inactive': 'Ce compte est inactif.',
    }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Tentative d'authentification avec email si ce n'est pas un username
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                    cleaned_data['username'] = username
                except User.DoesNotExist:
                    logger.warning(f"Tentative de connexion avec email inexistant: {username}")

            # Log des tentatives de connexion échouées
            if not authenticate(username=username, password=password):
                logger.warning(f"Échec de connexion pour: {username}")

        return cleaned_data


class RegisterForm(UserCreationForm):
    """Formulaire d'inscription avec validation complète"""

    first_name = forms.CharField(
        label="Prénom",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Votre prénom"
        })
    )

    last_name = forms.CharField(
        label="Nom de famille",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Votre nom de famille"
        })
    )

    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Choisissez un nom d'utilisateur"
        })
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "votre.email@exemple.com"
        })
    )

    role = forms.ChoiceField(
        label="Rôle",
        choices=User.Role.choices,
        initial=User.Role.CASHIER,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text="Sélectionnez le rôle approprié"
    )

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Choisissez un mot de passe sécurisé"
        })
    )

    password2 = forms.CharField(
        label="Confirmation",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Confirmez votre mot de passe"
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'role', 'password1', 'password2')

    def clean_email(self):
        """Vérifier l'unicité de l'email"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Un compte avec cet email existe déjà.")
        return email

    def clean_username(self):
        """Vérifier l'unicité du nom d'utilisateur"""
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def save(self, commit=True):
        """Sauvegarder l'utilisateur avec logging"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']

        if commit:
            user.save()
            logger.info(f"Nouvel utilisateur créé: {user.username} ({user.get_role_display()})")

        return user
