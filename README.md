# 🏪 Store Manager - Application de Gestion de Magasin

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Application Django moderne et responsive pour la gestion complète de magasin avec interface utilisateur glassmorphism et système complet de récupération de mot de passe.

## ✨ Fonctionnalités

### 🔐 Authentification Complète
- ✅ **Connexion sécurisée** avec redirection intelligente par rôle
- ✅ **Inscription** des nouveaux utilisateurs avec validation
- ✅ **Récupération de mot de passe** par email avec tokens sécurisés
- ✅ **Déconnexion** avec confirmation et nettoyage de session
- ✅ **Gestion des rôles** : Administrateur / Caissier

### 📧 Système Email Intégré
- ✅ **Configuration SMTP** pour Gmail et autres fournisseurs
- ✅ **Templates HTML** professionnels pour les emails
- ✅ **Tokens de sécurité** avec expiration (24h)
- ✅ **Mode développement** avec affichage console
- ✅ **Validation anti-spam** et protection

### 🎨 Interface Moderne
- ✅ **Design glassmorphism** avec effets de transparence
- ✅ **100% responsive** : PC, Tablette, Mobile
- ✅ **Animations fluides** CSS et JavaScript
- ✅ **Thème cohérent** avec palette de couleurs professionnelle
- ✅ **Accessibilité** optimisée

### 🏗️ Architecture Robuste
- ✅ **Django 5.2** avec modèle User personnalisé
- ✅ **SQLite optimisé** avec mode WAL pour les performances
- ✅ **Logging avancé** avec rotation des fichiers
- ✅ **Tests unitaires** complets
- ✅ **Documentation** détaillée

## 🚀 Installation Rapide

### Méthode Automatique (Recommandée)

**Windows :**
```bash
# Double-cliquez sur start.bat ou dans PowerShell :
./start.bat
```

**Linux/macOS :**
```bash
chmod +x start.sh
./start.sh
```

### Méthode Manuelle

1. **Créer un environnement virtuel :**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Configurer la base de données :**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Créer un superutilisateur :**
```bash
python manage.py createsuperuser
```

5. **Lancer le serveur :**
```bash
python manage.py runserver
```

## 🔧 Configuration Email

### Pour Gmail (Production)

1. **Activez l'authentification à 2 facteurs** sur votre compte Gmail
2. **Générez un mot de passe d'application** :
   - Accédez à votre compte Google
   - Sécurité → Mots de passe d'applications
   - Sélectionnez "Autre (nom personnalisé)"
   - Nommez "Store Manager"
   - Copiez le mot de passe généré

3. **Modifiez `settings.py` :**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-app'  # Mot de passe d'application
DEFAULT_FROM_EMAIL = 'Store Manager <votre-email@gmail.com>'
```

### Pour le Développement

Décommentez cette ligne pour afficher les emails dans la console :
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 📱 Accès à l'Application

| Page | URL | Description |
|------|-----|-------------|
| **Connexion** | `http://127.0.0.1:8000/login/` | Page de connexion principale |
| **Inscription** | `http://127.0.0.1:8000/register/` | Création de nouveaux comptes |
| **Mot de passe oublié** | `http://127.0.0.1:8000/password-reset/` | Récupération par email |
| **Dashboard Admin** | `http://127.0.0.1:8000/dashboard/` | Interface administrateur |
| **Caisse** | `http://127.0.0.1:8000/caisse/` | Interface point de vente |
| **Admin Django** | `http://127.0.0.1:8000/admin/` | Interface d'administration |

## 👥 Gestion des Rôles

### 🔑 Administrateur
- ✅ Accès au **tableau de bord** complet
- ✅ Gestion des **employés, fournisseurs, produits**
- ✅ **Rapports et statistiques** (Phase 2+)
- ✅ **Configuration système**
- ❌ Pas d'accès direct à la caisse

### 💰 Caissier
- ✅ Accès à l'**interface de caisse** uniquement
- ✅ **Vente de produits** et gestion du panier
- ✅ **Modes de paiement** (Espèces, Carte)
- ✅ **Impression des factures** (Phase 2+)
- ❌ Pas d'accès au dashboard administratif

## 🔄 Processus de Récupération de Mot de Passe

1. **Demande de réinitialisation** : L'utilisateur saisit son email
2. **Génération du token** : Django crée un token sécurisé unique
3. **Envoi de l'email** : Email HTML avec lien de réinitialisation
4. **Validation du lien** : Vérification du token et de l'expiration
5. **Nouveau mot de passe** : Saisie et confirmation
6. **Confirmation** : Notification de succès et redirection

### 🔒 Sécurité
- **Tokens uniques** générés avec HMAC
- **Expiration automatique** après 24 heures
- **Usage unique** des tokens
- **Validation des données** utilisateur
- **Protection CSRF** sur tous les formulaires

## 🧪 Test du Système

### Test de Connexion
```bash
# Administrateur
Username: admin
Password: [votre mot de passe]
→ Redirection vers /dashboard/

# Caissier  
Username: caissier
Password: [votre mot de passe]
→ Redirection vers /caisse/
```

### Test de Récupération de Mot de Passe
1. Accédez à `/password-reset/`
2. Saisissez un email valide
3. Vérifiez votre boîte email (ou console en mode dev)
4. Cliquez sur le lien de réinitialisation
5. Saisissez un nouveau mot de passe
6. Connectez-vous avec le nouveau mot de passe

## 📊 Structure du Projet

```
store_manager_project_with_password_reset/
├── manage.py                           # Point d'entrée Django
├── start.bat / start.sh               # Scripts de démarrage automatique
├── requirements.txt                   # Dépendances Python
├── store_manager/                     # Configuration principale
│   ├── settings.py                    # Paramètres (Email, DB, etc.)
│   ├── urls.py                        # Routing avec password reset
│   └── wsgi.py / asgi.py             # Serveurs de déploiement
├── apps/                              # Applications Django
│   ├── accounts/                      # Authentification & utilisateurs
│   │   ├── models.py                  # Modèle User personnalisé
│   │   ├── forms.py                   # Formulaires Login/Register
│   │   ├── views.py                   # Vues d'authentification
│   │   ├── urls.py                    # Routes accounts
│   │   └── templates/accounts/        # Templates auth
│   └── core/                          # Fonctionnalités principales
│       ├── views.py                   # Dashboard & Caisse
│       ├── urls.py                    # Routes core
│       └── templates/core/            # Templates principales
├── templates/                         # Templates globaux
│   ├── base.html                      # Template de base
│   └── registration/                  # Templates password reset
│       ├── password_reset_form.html   # Demande de réinitialisation
│       ├── password_reset_done.html   # Confirmation d'envoi
│       ├── password_reset_confirm.html # Saisie nouveau mot de passe
│       ├── password_reset_complete.html # Confirmation finale
│       ├── password_reset_email.html  # Template email HTML
│       └── password_reset_subject.txt # Objet de l'email
├── static/                            # Assets CSS/JS
│   ├── css/style.css                  # Styles personnalisés
│   └── js/main.js                     # JavaScript interactif
└── logs/                              # Fichiers de logs
    └── app.log                        # Logs de l'application
```

## 🛠️ Technologies Utilisées

| Composant | Technologie | Version | Utilisation |
|-----------|------------|---------|-------------|
| **Backend** | Django | 5.2 | Framework web Python |
| **Base de données** | SQLite | 3.x | Base de données locale |
| **Frontend** | Bootstrap | 5.3 | Framework CSS responsive |
| **Styles** | CSS3 | - | Glassmorphism et animations |
| **JavaScript** | Vanilla JS | ES6+ | Interactions dynamiques |
| **Email** | SMTP | - | Envoi d'emails |
| **Formulaires** | Crispy Forms | 2.0 | Rendu Bootstrap automatique |
| **Icons** | Font Awesome | 6.5 | Icônes vectorielles |
| **Fonts** | Google Fonts | - | Police Poppins |

## 📋 Feuille de Route

### ✅ Phase 1 : Authentification (TERMINÉE)
- [x] Connexion/Déconnexion sécurisée
- [x] Inscription des utilisateurs
- [x] Récupération de mot de passe par email
- [x] Gestion des rôles (Admin/Caissier)
- [x] Interface moderne responsive
- [x] Tests unitaires complets

### 🔄 Phase 2 : Gestion des Catégories (À venir)
- [ ] CRUD complet des catégories
- [ ] Recherche et filtrage
- [ ] Pagination des résultats
- [ ] Import/Export CSV
- [ ] Validation des doublons
- [ ] Images de catégories

### 🔄 Phase 3 : Gestion des Produits (À venir)
- [ ] CRUD des produits avec images
- [ ] Gestion des stocks et alertes
- [ ] Code-barres et SKU
- [ ] Prix et promotions
- [ ] Fournisseurs associés
- [ ] Catégorisation

### 🔄 Phase 4 : Gestion des Fournisseurs (À venir)
- [ ] Base de données fournisseurs
- [ ] Commandes et réceptions
- [ ] Suivi des livraisons
- [ ] Factures fournisseurs
- [ ] Évaluation performance

### 🔄 Phase 5 : Module de Ventes (À venir)
- [ ] Historique des ventes
- [ ] Factures PDF automatiques
- [ ] Rapports de performance
- [ ] Statistiques détaillées
- [ ] Export comptable

### 🔄 Phase 6 : Caisse Temps Réel (À venir)
- [ ] Interface POS complète
- [ ] Scanner de codes-barres
- [ ] Modes de paiement multiples
- [ ] Impression thermique
- [ ] Tiroir-caisse connecté

### 🔄 Phase 7 : Analytics & Reporting (À venir)
- [ ] Dashboard avec KPIs temps réel
- [ ] Graphiques interactifs (Chart.js)
- [ ] Alertes automatiques
- [ ] Rapports planifiés
- [ ] Business Intelligence

### 🔄 Phase 8 : Fonctionnalités Avancées (À venir)
- [ ] API REST complète
- [ ] Application mobile
- [ ] Synchronisation multi-magasins
- [ ] Intégration comptable
- [ ] Sauvegarde automatique

## 🧪 Tests

```bash
# Exécuter tous les tests
python manage.py test

# Tests spécifiques
python manage.py test apps.accounts
python manage.py test apps.core

# Avec couverture
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🚀 Déploiement

### Variables d'Environnement (Production)
```bash
export DEBUG=False
export SECRET_KEY=your-secret-key
export EMAIL_HOST_USER=your-email@gmail.com
export EMAIL_HOST_PASSWORD=your-app-password
export ALLOWED_HOSTS=yourdomain.com
```

### Serveur de Production
```bash
# Collecte des fichiers statiques
python manage.py collectstatic

# Utilisation avec Gunicorn
pip install gunicorn
gunicorn store_manager.wsgi:application
```

## 🤝 Contribution

1. **Fork** le projet
2. **Créez** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrez** une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- 📧 **Email** : support@storemanager.com
- 📚 **Documentation** : Voir le dossier `docs/`
- 🐛 **Issues** : Créez une issue sur GitHub
- 💬 **Discussions** : Utilisez les GitHub Discussions

## 🙏 Remerciements

- **Django Community** pour le framework exceptionnel
- **Bootstrap Team** pour les composants UI
- **Font Awesome** pour les icônes
- **Google Fonts** pour la typographie Poppins

---

**Store Manager** - *La solution complète pour votre magasin* 🏪✨
