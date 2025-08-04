from django.db import models

# Modèles pour les futures fonctionnalités
# (Catégories, Produits, Ventes, etc.)
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

class Supplier(models.Model):
    """Modèle pour gérer les fournisseurs"""
    
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Actif"
        INACTIVE = "INACTIVE", "Inactif"
        SUSPENDED = "SUSPENDED", "Suspendu"
    
    # Informations de base
    name = models.CharField(
        max_length=200,
        verbose_name="Nom du fournisseur",
        help_text="Nom complet de l'entreprise fournisseur"
    )
    
    contact_person = models.CharField(
        max_length=150,
        verbose_name="Personne de contact",
        help_text="Nom de la personne responsable"
    )
    
    # Coordonnées
    email = models.EmailField(
        verbose_name="Email",
        help_text="Adresse email principale"
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro doit être au format: '+999999999'. 15 chiffres maximum."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name="Téléphone",
        help_text="Numéro de téléphone principal"
    )
    
    # Adresse
    address = models.TextField(
        verbose_name="Adresse complète",
        help_text="Adresse physique du fournisseur"
    )
    
    city = models.CharField(
        max_length=100,
        verbose_name="Ville"
    )
    
    postal_code = models.CharField(
        max_length=20,
        verbose_name="Code postal"
    )
    
    country = models.CharField(
        max_length=100,
        default="France",
        verbose_name="Pays"
    )
    
    # Informations commerciales
    tax_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Numéro TVA",
        help_text="Numéro d'identification fiscale"
    )
    
    payment_terms = models.CharField(
        max_length=100,
        default="30 jours",
        verbose_name="Conditions de paiement",
        help_text="Ex: 30 jours, paiement comptant, etc."
    )
    
    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name="Limite de crédit (€)",
        help_text="Limite de crédit accordée au fournisseur"
    )
    
    # Statut et métadonnées
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Statut"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Notes",
        help_text="Notes internes sur le fournisseur"
    )
    
    # Horodatage
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Modifié le"
    )
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    def get_absolute_url(self):
        return reverse('core:supplier_detail', kwargs={'pk': self.pk})
    
    def is_active(self):
        """Vérifie si le fournisseur est actif"""
        return self.status == self.Status.ACTIVE
    
    def get_status_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        status_classes = {
            self.Status.ACTIVE: "badge-success",
            self.Status.INACTIVE: "badge-secondary", 
            self.Status.SUSPENDED: "badge-warning"
        }
        return status_classes.get(self.status, "badge-secondary")


#categories
class Category(models.Model):
    """Modèle pour les catégories de produits"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la catégorie"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name


#produits
class Product(models.Model):
    """Modèle pour les produits"""
    
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Actif"
        INACTIVE = "INACTIVE", "Inactif"
        OUT_OF_STOCK = "OUT_OF_STOCK", "Rupture de stock"
    
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name="Catégorie"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Prix (€)"
    )
    stock_quantity = models.PositiveIntegerField(
        default=0, 
        verbose_name="Quantité en stock"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Description"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Statut"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['name']

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock_quantity > 0 and self.status == self.Status.ACTIVE
