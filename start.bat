@echo off
echo 🚀 Démarrage de Store Manager...
echo ==================================

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé. Veuillez l'installer d'abord.
    pause
    exit /b 1
)

REM Créer l'environnement virtuel s'il n'existe pas
if not exist "venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Installer les dépendances
echo 📚 Installation des dépendances...
pip install --upgrade pip
pip install -r requirements.txt

REM Créer le répertoire logs s'il n'existe pas
if not exist "logs" mkdir logs

REM Appliquer les migrations
echo 🗄️  Configuration de la base de données...
python manage.py makemigrations
python manage.py migrate

REM Demander la création d'un superutilisateur
echo 👤 Création d'un compte administrateur...
python manage.py createsuperuser

REM Démarrer le serveur
echo 🌐 Démarrage du serveur de développement...
echo 📍 Votre application sera disponible sur: http://127.0.0.1:8000/
echo 🔑 Page de connexion: http://127.0.0.1:8000/login/
echo 📝 Inscription: http://127.0.0.1:8000/register/
echo 🔑 Récupération mot de passe: http://127.0.0.1:8000/password-reset/
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

python manage.py runserver
pause
