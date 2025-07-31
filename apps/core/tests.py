from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CoreViewsTest(TestCase):
    """Tests pour les vues principales"""

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpass123',
            role=User.Role.ADMIN
        )
        self.cashier_user = User.objects.create_user(
            username='cashier',
            password='testpass123',
            role=User.Role.CASHIER
        )

    def test_dashboard_access_admin(self):
        """Test d'accès au dashboard pour admin"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tableau de bord')

    def test_dashboard_access_cashier_denied(self):
        """Test de refus d'accès au dashboard pour caissier"""
        self.client.login(username='cashier', password='testpass123')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirection

    def test_caisse_access_authenticated(self):
        """Test d'accès à la caisse pour utilisateur authentifié"""
        self.client.login(username='cashier', password='testpass123')
        response = self.client.get(reverse('core:caisse'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Caisse')

    def test_home_redirect_admin(self):
        """Test redirection home pour admin"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('core:home'))
        self.assertRedirects(response, reverse('core:dashboard'))

    def test_home_redirect_cashier(self):
        """Test redirection home pour caissier"""
        self.client.login(username='cashier', password='testpass123')
        response = self.client.get(reverse('core:home'))
        self.assertRedirects(response, reverse('core:caisse'))
