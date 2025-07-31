# 📋 Guide d'Installation Détaillé - Store Manager

## 🎯 Prérequis

### Système d'exploitation
- ✅ **Windows** 10/11
- ✅ **macOS** 10.15+
- ✅ **Linux** Ubuntu 18.04+/Fedora 30+/CentOS 7+

### Logiciels requis
- **Python** 3.8 ou supérieur
- **pip** (gestionnaire de paquets Python)
- **Git** (optionnel, pour le développement)

## 🔧 Étape 1 : Vérification de l'environnement

### Vérifier Python
```bash
python --version
# ou
python3 --version
```
**Sortie attendue :** `Python 3.8.x` ou supérieur

### Vérifier pip
```bash
pip --version
# ou
pip3 --version
```

### Installer Python (si nécessaire)
- **Windows** : Téléchargez depuis [python.org](https://python.org)
- **macOS** : `brew install python3` ou depuis python.org
- **Linux** : `sudo apt-get install python3 python3-pip`

## 🚀 Étape 2 : Installation Automatique (Recommandée)

### Windows
1. **Extraire** l'archive `store_manager_project_with_password_reset.zip`
2. **Ouvrir** l'invite de commande dans le dossier extrait
3. **Double-cliquer** sur `start.bat` ou exécuter :
```cmd
start.bat
```

### Linux/macOS
1. **Extraire** l'archive
2. **Ouvrir** un terminal dans le dossier extrait
3. **Exécuter** :
```bash
chmod +x start.sh
./start.sh
```

Le script automatique va :
- ✅ Créer l'environnement virtuel
- ✅ Installer toutes les dépendances
- ✅ Configurer la base de données
- ✅ Vous demander de créer un compte administrateur
- ✅ Démarrer le serveur de développement

## 🔧 Étape 3 : Installation Manuelle (Alternative)

### 3.1 Extraction et navigation
```bash
# Extraire l'archive (Windows : clic droit > Extraire)
unzip store_manager_project_with_password_reset.zip
cd store_manager_project_with_password_reset
```

### 3.2 Environnement virtuel
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows :
venv\Scripts\activate
# Linux/macOS :
source venv/bin/activate
```

**Vérification :** Votre invite de commande doit afficher `(venv)` au début.

### 3.3 Installation des dépendances
```bash
# Mise à jour de pip
pip install --upgrade pip

# Installation des dépendances
pip install -r requirements.txt
```

**Packages installés :**
- Django 5.2
- django-crispy-forms 2.0
- crispy-bootstrap5 0.7
- Pillow ≥11.0.0

### 3.4 Configuration de la base de données
```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 3.5 Création du superutilisateur
```bash
python manage.py createsuperuser
```

**Informations demandées :**
- **Nom d'utilisateur** : `admin` (recommandé)
- **Email** : votre adresse email
- **Mot de passe** : mot de passe sécurisé (8+ caractères)

### 3.6 Démarrage du serveur
```bash
python manage.py runserver
```

**Message de succès :**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 5.2, using settings 'store_manager.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## 📧 Étape 4 : Configuration Email (IMPORTANTE)

### 4.1 Configuration Gmail (Production)

1. **Activer l'authentification à 2 facteurs** :
   - Allez sur [myaccount.google.com](https://myaccount.google.com)
   - Sécurité → Authentification à 2 facteurs

2. **Créer un mot de passe d'application** :
   - Sécurité → Mots de passe d'applications
   - Sélectionner "Autre (nom personnalisé)"
   - Nom : "Store Manager"
   - **COPIER** le mot de passe généré (16 caractères)

3. **Modifier `store_manager/settings.py`** :
```python
# Remplacer ces lignes (lignes 120-126 environ)
EMAIL_HOST_USER = 'votre-email@gmail.com'  # Votre vraie adresse Gmail
EMAIL_HOST_PASSWORD = 'abcd efgh ijkl mnop'  # Le mot de passe d'application (16 chars)
DEFAULT_FROM_EMAIL = 'Store Manager <votre-email@gmail.com>'
```

### 4.2 Configuration pour tests (Développement)
Pour tester sans envoyer de vrais emails, **décommentez cette ligne** :
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Les emails apparaîtront dans la console au lieu d'être envoyés.

## 🧪 Étape 5 : Vérification de l'installation

### 5.1 Accès à l'application
Ouvrez votre navigateur et accédez à :
- **Page de connexion** : http://127.0.0.1:8000/login/
- **Inscription** : http://127.0.0.1:8000/register/
- **Récupération** : http://127.0.0.1:8000/password-reset/

### 5.2 Test de connexion
1. **Connectez-vous** avec votre compte admin
2. **Vérifiez la redirection** vers `/dashboard/`
3. **Testez la déconnexion**

### 5.3 Test de récupération de mot de passe
1. Cliquez sur **"Mot de passe oublié ?"**
2. Saisissez votre email
3. **Vérifiez** votre boîte email (ou la console si mode dev)
4. **Cliquez** sur le lien de réinitialisation
5. **Saisissez** un nouveau mot de passe

### 5.4 Test responsive
1. **Redimensionnez** la fenêtre du navigateur
2. **Testez** sur mobile (F12 → mode mobile)
3. **Vérifiez** que l'interface s'adapte

## ❌ Résolution des Problèmes Courants

### Erreur : "Python n'est pas reconnu"
**Solution :** Ajouter Python au PATH système
- Windows : Réinstaller Python en cochant "Add to PATH"
- Linux/macOS : Utiliser `python3` à la place de `python`

### Erreur : "No module named 'django'"
**Solution :** Environnement virtuel non activé
```bash
# Vérifiez que (venv) apparaît dans votre invite
# Si non, réactivez :
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

### Erreur : "Permission denied" (Linux/macOS)
**Solution :** Permissions du script
```bash
chmod +x start.sh
sudo chown -R $USER:$USER .
```

### Erreur : "Port already in use"
**Solution :** Port 8000 occupé
```bash
# Utiliser un autre port
python manage.py runserver 8001
# Ou identifier le processus qui utilise le port 8000
```

### Erreur : Email non reçu
**Vérifications :**
1. ✅ Mot de passe d'application Gmail correct
2. ✅ Authentification à 2 facteurs activée
3. ✅ Vérifier le dossier spam
4. ✅ Adresse email correcte dans settings.py

### Erreur : "CSRF token missing"
**Solution :** Vider le cache du navigateur
```bash
# Ou en mode navigation privée
Ctrl+Shift+N (Chrome)
Ctrl+Shift+P (Firefox)
```

## 🔒 Configuration de Sécurité

### Variables d'environnement (Production)
Créer un fichier `.env` :
```bash
DEBUG=False
SECRET_KEY=votre-clé-secrète-très-longue-et-aléatoire
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
ALLOWED_HOSTS=127.0.0.1,localhost,votre-domaine.com
```

### Modifier settings.py pour la production
```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'True') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

## 📊 Vérification des Performances

### Tests de charge basiques
```bash
# Installer Apache Bench (optionnel)
# Windows : via Apache HTTP Server
# Linux : sudo apt-get install apache2-utils
# macOS : brew install httpie

# Test basique
ab -n 100 -c 10 http://127.0.0.1:8000/login/
```

### Monitoring des logs
```bash
# Surveiller les logs en temps réel
tail -f logs/app.log
```

## 🎉 Installation Réussie !

Si tout fonctionne :
- ✅ Serveur démarré sur port 8000
- ✅ Page de connexion accessible
- ✅ Récupération de mot de passe fonctionnelle
- ✅ Interface responsive
- ✅ Emails envoyés/reçus

**Votre installation de Store Manager est terminée !**

## 📞 Support

En cas de problème persistant :
1. **Vérifiez** ce guide étape par étape
2. **Consultez** les logs : `logs/app.log`
3. **Testez** en mode développement avec `DEBUG=True`
4. **Contactez** le support technique

---

**Bonne utilisation de Store Manager !** 🎉🏪
