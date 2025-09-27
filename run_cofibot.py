#!/usr/bin/env python3
"""
Script de lancement complet de CofiBot Energy Manager
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def print_banner():
    """Affiche la bannière de démarrage"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    COFIBOT ENERGY MANAGER                   ║
║                     Système de Gestion                      ║
║                    Énergétique Intelligent                  ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Vérifie la version de Python"""
    print("🔍 Vérification de Python...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        print(f"   Version actuelle: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_node_version():
    """Vérifie la version de Node.js"""
    print("🔍 Vérification de Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version}")
            return True
        else:
            print("❌ Node.js non trouvé")
            return False
    except FileNotFoundError:
        print("❌ Node.js non installé")
        print("💡 Installez Node.js depuis https://nodejs.org/")
        return False

def setup_project_structure():
    """Crée la structure du projet"""
    print("🏗️ Création de la structure du projet...")
    
    directories = [
        "backend", "backend/app", "backend/app/models", "backend/app/database",
        "backend/app/services", "backend/app/api", "backend/app/core", 
        "backend/app/utils", "backend/data", "backend/logs",
        "frontend", "frontend/public", "frontend/src", "frontend/src/components",
        "frontend/src/pages", "frontend/src/services", "frontend/src/styles"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  📁 {directory}")
    
    # Créer les __init__.py
    init_files = [
        "backend/app/__init__.py", "backend/app/models/__init__.py",
        "backend/app/database/__init__.py", "backend/app/services/__init__.py",
        "backend/app/api/__init__.py", "backend/app/core/__init__.py",
        "backend/app/utils/__init__.py"
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write("# Package initialization\n")

def install_backend_dependencies():
    """Installe les dépendances backend"""
    print("📦 Installation des dépendances backend...")
    
    if not os.path.exists("backend/requirements.txt"):
        print("❌ requirements.txt manquant")
        return False
    
    try:
        os.chdir("backend")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              check=True, capture_output=True, text=True)
        print("✅ Dépendances backend installées")
        os.chdir("..")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur installation backend: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        os.chdir("..")
        return False

def install_frontend_dependencies():
    """Installe les dépendances frontend"""
    print("📦 Installation des dépendances frontend...")
    
    if not os.path.exists("frontend/package.json"):
        print("❌ package.json manquant")
        return False
    
    try:
        os.chdir("frontend")
        result = subprocess.run(["npm", "install"], check=True, capture_output=True, text=True)
        print("✅ Dépendances frontend installées")
        os.chdir("..")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur installation frontend: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        os.chdir("..")
        return False

def start_backend():
    """Démarre le serveur backend"""
    print("🚀 Démarrage du backend...")
    
    def run_backend():
        os.chdir("backend")
        try:
            subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
        except KeyboardInterrupt:
            print("\n🛑 Backend arrêté")
        finally:
            os.chdir("..")
    
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Attendre que le backend démarre
    time.sleep(3)
    return backend_thread

def start_frontend():
    """Démarre le serveur frontend"""
    print("🚀 Démarrage du frontend...")
    
    def run_frontend():
        os.chdir("frontend")
        try:
            subprocess.run(["npm", "start"])
        except KeyboardInterrupt:
            print("\n🛑 Frontend arrêté")
        finally:
            os.chdir("..")
    
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    frontend_thread.start()
    
    return frontend_thread

def show_urls():
    """Affiche les URLs d'accès"""
    print("\n" + "="*60)
    print("🌐 URLS D'ACCÈS")
    print("="*60)
    print("📱 Frontend:      http://localhost:3000")
    print("🔧 Backend API:   http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("📊 Redoc:         http://localhost:8000/redoc")
    print("="*60)

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifications préliminaires
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    # Setup du projet
    setup_project_structure()
    
    # Installation des dépendances
    print("\n" + "="*60)
    print("📦 INSTALLATION DES DÉPENDANCES")
    print("="*60)
    
    if not install_backend_dependencies():
        print("❌ Échec installation backend")
        sys.exit(1)
    
    if not install_frontend_dependencies():
        print("❌ Échec installation frontend")
        sys.exit(1)
    
    # Démarrage des serveurs
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DES SERVEURS")
    print("="*60)
    
    backend_thread = start_backend()
    time.sleep(2)  # Laisser le temps au backend de démarrer
    
    frontend_thread = start_frontend()
    
    show_urls()
    
    print("\n💡 CONSEILS:")
    print("- Utilisez Ctrl+C pour arrêter les serveurs")
    print("- Le backend se recharge automatiquement lors des modifications")
    print("- Consultez les logs pour le débogage")
    
    try:
        # Garder le script en vie
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt de CofiBot...")
        print("👋 À bientôt!")

if __name__ == "__main__":
    main()
