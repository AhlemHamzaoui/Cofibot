import os

def create_project_directories():
    """Crée tous les dossiers nécessaires pour le projet CofiBot"""
    
    directories = [
        "data",
        "data/files",
        "data/invoices",
        "data/reports",
        "logs",
        "temp",
        "uploads"
    ]
    
    print("🔧 Création des dossiers nécessaires...")
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Dossier créé: {directory}")
        except Exception as e:
            print(f"❌ Erreur création {directory}: {e}")
    
    # Créer des fichiers .gitkeep pour garder les dossiers vides dans git
    gitkeep_dirs = ["data/files", "data/invoices", "data/reports", "logs", "temp", "uploads"]
    
    for directory in gitkeep_dirs:
        gitkeep_path = os.path.join(directory, ".gitkeep")
        try:
            with open(gitkeep_path, 'w') as f:
                f.write("# Ce fichier permet de garder le dossier dans git\n")
            print(f"📝 .gitkeep créé dans {directory}")
        except Exception as e:
            print(f"❌ Erreur .gitkeep {directory}: {e}")
    
    print("\n🎉 Tous les dossiers ont été créés avec succès!")
    print("Vous pouvez maintenant lancer: python main_energy.py")

if __name__ == "__main__":
    create_project_directories()
