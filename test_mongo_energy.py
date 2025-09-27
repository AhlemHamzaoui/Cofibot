from services.mongo_energy_llm import MongoEnergyLLMService
from models.energy_models_mongo import ChatMessage
import json

def test_mongo_energy_chatbot():
    """Test du chatbot énergie MongoDB"""
    service = MongoEnergyLLMService()
    
    test_questions = [
        "Bonjour, peux-tu me donner la consommation de la LIGNE_001 cette semaine ?",
        "Quelle est la consommation électrique d'aujourd'hui ?",
        "Montre-moi les factures du mois dernier",
        "Quel équipement consomme le plus d'énergie ?",
        "Analyse comparative entre toutes les lignes de production",
        "Y a-t-il des anomalies de consommation cette semaine ?",
        "Consommation totale LIGNE_002 vs LIGNE_003 ce mois",
        "Recommandations pour optimiser la consommation énergétique",
        "Détails des cycles de production hier",
        "Facture électricité novembre 2024"
    ]
    
    print("🔋 TEST COFIBOT ENERGY MANAGER MONGODB")
    print("=" * 70)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 60)
        
        result = service.generate_response(question, "test_manager")
        
        if result["success"]:
            print(f"✅ Réponse: {result['response']}")
            
            if result.get("data"):
                if isinstance(result["data"], list):
                    print(f"📊 Données: {len(result['data'])} éléments trouvés")
                else:
                    print(f"📊 Données: {type(result['data']).__name__} disponible")
            
            if result.get("charts"):
                print(f"📈 Graphiques: {len(result['charts'])} disponibles")
            
            if result.get("files"):
                print(f"📄 Fichiers: {result['files']}")
            
            if result.get("parsed_request"):
                parsed = result["parsed_request"]
                print(f"🔍 Analyse: Type={parsed['request_type']}, Ligne={parsed['ligne_id']}")
        else:
            print(f"❌ Erreur: {result['error']}")
        
        print()
    
    # Fermer la connexion
    service.close()

if __name__ == "__main__":
    test_mongo_energy_chatbot()
