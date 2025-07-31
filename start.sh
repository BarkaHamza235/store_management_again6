#!/bin/bash

# Store Manager - Script de démarrage rapide

echo "🚀 Démarrage de Store Manager..."
echo "=================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Utiliser python3 si disponible, sinon python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    $PYTHON_CMD -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📚 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Créer le répertoire logs s'il n'existe pas
mkdir -p logs

# Appliquer les migrations
echo "🗄️  Configuration de la base de données..."
python manage.py makemigrations
python manage.py migrate

# Demander la création d'un superutilisateur
echo "👤 Création d'un compte administrateur..."
python manage.py createsuperuser

# Démarrer le serveur
echo "🌐 Démarrage du serveur de développement..."
echo "📍 Votre application sera disponible sur: http://127.0.0.1:8000/"
echo "🔑 Page de connexion: http://127.0.0.1:8000/login/"
echo "📝 Inscription: http://127.0.0.1:8000/register/"
echo "🔑 Récupération mot de passe: http://127.0.0.1:8000/password-reset/"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python manage.py runserver
