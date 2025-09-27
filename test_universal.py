from services.universal_llm_service import UniversalEnergyLLM
from database.sqlite_db import SQLiteEnergyDB
from database.mongo_db import MongoEnergyDB
import os

def test_universal_system():
    """Test du système universel"""
    
    # Tester avec SQLite
    print("🧪 TEST AVEC SQLITE")
    print("=" * 40)
    
    sqlite_db = SQLiteEnergyDB()
    sqlite_service = UniversalEnergyLLM(sqlite_db)
    
    result = sqlite_service.generate_response(
        "Consommation cette semaine", 
        "test_user"
    )
    
    print(f"SQLite: {result['success']}")
    if result["success"]:
        print(f"Réponse: {result['response'][:100]}...")
    
    sqlite_db.close()
    
    # Tester avec MongoDB (si disponible)
    try:
        print("\n🧪 TEST AVEC MONGODB")
        print("=" * 40)
        
        mongo_db = MongoEnergyDB()
        mongo_service = UniversalEnergyLLM(mongo_db)
        
        result = mongo_service.generate_response(
            "Consommation cette semaine", 
            "test_user"
        )
        
        print(f"MongoDB: {result['success']}")
        if result["success"]:
            print(f"Réponse: {result['response'][:100]}...")
        
        mongo_db.close()
        
    except Exception as e:
        print(f"MongoDB non disponible: {e}")

if __name__ == "__main__":
    test_universal_system()
