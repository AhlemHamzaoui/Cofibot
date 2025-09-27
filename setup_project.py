import os
import subprocess
import sys

def create_directory_structure():
    """Crée la structure complète du projet"""
    
    directories = [
        # Backend
        "backend",
        "backend/app",
        "backend/app/models",
        "backend/app/database",
        "backend/app/services",
        "backend/app/api",
        "backend/app/core",
        "backend/app/utils",
        "backend/data",
        "backend/data/invoices",
        "backend/logs",
        
        # Frontend
        "frontend",
        "frontend/public",
        "frontend/src",
        "frontend/src/components",
        "frontend/src/components/common",
        "frontend/src/components/dashboard",
        "frontend/src/components/chat",
        "frontend/src/pages",
        "frontend/src/services",
        "frontend/src/hooks",
        "frontend/src/utils",
        "frontend/src/styles",
        "frontend/src/assets",
        
        # Documentation
        "docs",
        "tests"
    ]
    
    print("🏗️ Création de la structure du projet...")
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ {directory}")
        except Exception as e:
            print(f"❌ Erreur {directory}: {e}")
    
    # Créer les fichiers __init__.py pour Python
    python_packages = [
        "backend/app/__init__.py",
        "backend/app/models/__init__.py",
        "backend/app/database/__init__.py",
        "backend/app/services/__init__.py",
        "backend/app/api/__init__.py",
        "backend/app/core/__init__.py",
        "backend/app/utils/__init__.py"
    ]
    
    for package in python_packages:
        try:
            with open(package, 'w') as f:
                f.write("# Package initialization\n")
            print(f"✅ {package}")
        except Exception as e:
            print(f"❌ Erreur {package}: {e}")

def create_backend_requirements():
    """Crée le fichier requirements.txt pour le backend"""
    
    requirements = """# FastAPI et serveur
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Base de données
sqlalchemy==2.0.23
sqlite3

# Validation et sérialisation
pydantic==2.5.0
pydantic-settings==2.1.0

# HTTP et CORS
requests==2.31.0
python-multipart==0.0.6

# Utilitaires
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Dates et temps
python-dateutil==2.8.2

# Logging
loguru==0.7.2

# Tests (optionnel)
pytest==7.4.3
httpx==0.25.2
"""
    
    try:
        with open("backend/requirements.txt", "w") as f:
            f.write(requirements.strip())
        print("✅ backend/requirements.txt créé")
    except Exception as e:
        print(f"❌ Erreur requirements.txt: {e}")

def create_frontend_package_json():
    """Crée le package.json pour le frontend React"""
    
    package_json = """{
  "name": "cofibot-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^14.5.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "react-router-dom": "^6.8.1",
    "axios": "^1.6.2",
    "recharts": "^2.8.0",
    "lucide-react": "^0.294.0",
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "@headlessui/react": "^1.7.17",
    "@heroicons/react": "^2.0.18",
    "clsx": "^2.0.0",
    "date-fns": "^2.30.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://localhost:8000"
}"""
    
    try:
        with open("frontend/package.json", "w") as f:
            f.write(package_json)
        print("✅ frontend/package.json créé")
    except Exception as e:
        print(f"❌ Erreur package.json: {e}")

def create_env_files():
    """Crée les fichiers d'environnement"""
    
    # Backend .env
    backend_env = """# Configuration Backend
DATABASE_URL=sqlite:///./data/cofibot.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=CofiBot Energy Manager

# Ollama Configuration (optionnel)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Logging
LOG_LEVEL=INFO
"""
    
    # Frontend .env
    frontend_env = """# Configuration Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_VERSION=v1
REACT_APP_PROJECT_NAME=CofiBot Energy Manager
"""
    
    try:
        with open("backend/.env", "w") as f:
            f.write(backend_env.strip())
        print("✅ backend/.env créé")
        
        with open("frontend/.env", "w") as f:
            f.write(frontend_env.strip())
        print("✅ frontend/.env créé")
    except Exception as e:
        print(f"❌ Erreur .env: {e}")

def main():
    """Fonction principale de setup"""
    print("🚀 SETUP COFIBOT ENERGY MANAGER")
    print("=" * 50)
    
    # 1. Créer la structure
    create_directory_structure()
    
    # 2. Créer les fichiers de configuration
    create_backend_requirements()
    create_frontend_package_json()
    create_env_files()
    
    print("\n" + "=" * 50)
    print("✅ SETUP TERMINÉ")
    print("=" * 50)
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. cd backend && pip install -r requirements.txt")
    print("2. cd frontend && npm install")
    print("3. npm run dev (pour lancer backend + frontend)")
    print("\n📍 URLs:")
    print("- Frontend: http://localhost:3000")
    print("- Backend API: http://localhost:8000")
    print("- Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
