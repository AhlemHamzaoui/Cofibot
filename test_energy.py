from services.energy_llm import EnergyLLMService
from models.energy_models import ChatMessage
import json

def test_energy_chatbot():
    """Test du chatbot énergie"""
    service = EnergyLLMService()
    
    test_questions = [
        "Bonjour, peux-tu me donner la consommation électrique du mois dernier ?",
        "Quelle est la facture de gaz du site PROD_A en janvier ?",
        "Analyse de la consommation cette semaine vs semaine dernière",
        "Quels sont les pics de consommation cette année ?",
        "Recommandations pour optimiser notre consommation énergétique",
        "Coût total de l'électricité sur les 3 derniers mois",
        "Comparaison consommation Production vs Administration"
    ]
    
    print("🔋 TEST COFIBOT ENERGY MANAGER")
    print("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 50)
        
        result = service.generate_response(question, "test_manager")
        
        if result["success"]:
            print(f"✅ Réponse: {result['response']}")
            
            if result.get("data"):
                print(f"📊 Données: {len(result['data'])} éléments trouvés")
            
            if result.get("charts"):
                print(f"📈 Graphiques: {len(result['charts'])} disponibles")
            
            if result.get("files"):
                print(f"📄 Fichiers: {result['files']}")
        else:
            print(f"❌ Erreur: {result['error']}")
        
        print()

if __name__ == "__main__":
    test_energy_chatbot()
