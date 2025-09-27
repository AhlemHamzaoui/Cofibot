@echo off
echo 🚀 Configuration de CofiBot Energy Manager
echo.

echo 📁 Création des dossiers nécessaires...
python create_directories.py

echo.
echo 🔧 Vérification des dépendances...
python test_installation.py

echo.
echo 🎯 Lancement de CofiBot Energy Manager...
echo API disponible sur: http://127.0.0.1:8002
echo Documentation: http://127.0.0.1:8002/docs
echo.

python main_energy.py

pause
