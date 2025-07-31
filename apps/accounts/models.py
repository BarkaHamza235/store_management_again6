from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle utilisateur personnalisé avec rôles"""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        CASHIER = "CASHIER", "Caissier"

    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.CASHIER,
        help_text="Rôle de l'utilisateur dans le système"
    )

    email = models.EmailField(
        unique=True,
        help_text="Adresse email unique requise pour la récupération de mot de passe"
    )

    def is_admin(self):
        """Vérifie si l'utilisateur est administrateur"""
        return self.role == self.Role.ADMIN

    def is_cashier(self):
        """Vérifie si l'utilisateur est caissier"""
        return self.role == self.Role.CASHIER

    def get_role_display_verbose(self):
        """Retourne l'affichage détaillé du rôle"""
        return self.get_role_display()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
