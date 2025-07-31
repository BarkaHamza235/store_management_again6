from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()


class AuthViewsTest(TestCase):
    """Tests pour les vues d'authentification"""

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='testpass123',
            role=User.Role.ADMIN
        )
        self.cashier_user = User.objects.create_user(
            username='cashier_test',
            email='cashier@test.com',
            password='testpass123',
            role=User.Role.CASHIER
        )

    def test_login_admin_redirect(self):
        """Test redirection admin après connexion"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'admin_test',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:dashboard'))

    def test_login_cashier_redirect(self):
        """Test redirection caissier après connexion"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'cashier_test',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:caisse'))

    def test_register_new_user(self):
        """Test création nouveau utilisateur"""
        response = self.client.post(reverse('accounts:register'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@test.com',
            'role': User.Role.CASHIER,
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='johndoe').exists())

    def test_password_reset_form(self):
        """Test formulaire de récupération de mot de passe"""
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Récupération de mot de passe')

    def test_password_reset_email_send(self):
        """Test envoi email de récupération"""
        response = self.client.post(reverse('password_reset'), {
            'email': 'admin@test.com'
        })
        self.assertEqual(response.status_code, 302)
        # Vérifier qu'un email a été envoyé
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Store Manager', mail.outbox[0].subject)
