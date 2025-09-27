#!/bin/bash

echo "🚀 Démarrage de CofiBot Energy Manager"
echo "======================================"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trouvé"
    exit 1
fi

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js non trouvé"
    exit 1
fi

# Créer la structure si nécessaire
python3 setup_project.py

# Installer les dépendances backend
echo "📦 Installation dépendances backend..."
cd backend
pip3 install -r requirements.txt
cd ..

# Installer les dépendances frontend
echo "📦 Installation dépendances frontend..."
cd frontend
npm install
cd ..

# Démarrer les serveurs
echo "🚀 Démarrage des serveurs..."

# Backend en arrière-plan
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# Attendre que le backend démarre
sleep 3

# Frontend
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ Serveurs démarrés"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"

# Fonction de nettoyage
cleanup() {
    echo "🛑 Arrêt des serveurs..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre
wait
