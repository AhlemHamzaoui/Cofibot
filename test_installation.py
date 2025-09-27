import sys

def test_imports():
    """Teste l'importation de tous les modules nécessaires"""
    
    modules_to_test = [
        ("sqlite3", "Base de données SQLite"),
        ("os", "Système d'exploitation"),
        ("datetime", "Gestion des dates"),
        ("random", "Génération aléatoire"),
        ("json", "Manipulation JSON")
    ]
    
    optional_modules = [
        ("fastapi", "Framework web FastAPI"),
        ("uvicorn", "Serveur ASGI"),
        ("requests", "Requêtes HTTP"),
        ("pydantic", "Validation de données"),
        ("pymongo", "MongoDB (optionnel)")
    ]
    
    print("🧪 Test des modules essentiels...")
    
    all_good = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name}: {description}")
        except ImportError as e:
            print(f"❌ {module_name}: {description} - ERREUR: {e}")
            all_good = False
    
    print("\n🔧 Test des modules optionnels...")
    
    for module_name, description in optional_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name}: {description}")
        except ImportError as e:
            print(f"⚠️  {module_name}: {description} - Non installé: {e}")
    
    print(f"\n🐍 Version Python: {sys.version}")
    
    if all_good:
        print("\n🎉 Tous les modules essentiels sont disponibles!")
        print("Vous pouvez maintenant créer les dossiers et lancer CofiBot.")
    else:
        print("\n❌ Certains modules essentiels manquent.")
        print("Veuillez installer Python correctement.")
    
    return all_good

if __name__ == "__main__":
    test_imports()
