import requests
import json
from datetime import datetime
from typing import List, Dict, Any

class CofiBotLlama:
    def __init__(self, model="llama3.2:3b"):
        self.model = model
        self.base_url = "http://localhost:11434"
        self.conversation_history = []
        
        # Prompt système optimisé pour CofiBot
        self.system_prompt = """Tu es CofiBot, l'assistant intelligent de Coficab.

CONTEXTE:
- Coficab est une entreprise française spécialisée dans la fabrication de câbles automobiles
- Tu aides les employés avec leurs questions professionnelles
- Tu réponds toujours en français, de manière claire et professionnelle

INSTRUCTIONS:
- Sois amical mais professionnel
- Si tu ne connais pas une information spécifique à Coficab, dis-le clairement
- Propose des solutions alternatives quand possible
- Reste dans le contexte professionnel et automobile

DOMAINES D'EXPERTISE:
- Câbles électriques automobiles
- Processus de fabrication
- Normes qualité (ISO)
- Procédures d'entreprise
- Questions RH générales"""
    
    def is_available(self):
        """Vérifie si Ollama et le modèle sont disponibles"""
        try:
            # Vérifier la connexion
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200:
                return False, "Ollama n'est pas accessible"
            
            # Vérifier si le modèle existe
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if self.model not in model_names:
                return False, f"Modèle {self.model} non trouvé. Modèles disponibles: {model_names}"
            
            return True, "OK"
            
        except Exception as e:
            return False, f"Erreur: {str(e)}"
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """Conversation avec l'utilisateur"""
        # Vérifier la disponibilité
        available, message = self.is_available()
        if not available:
            return {
                "success": False,
                "error": message,
                "response": None
            }
        
        # Construire le prompt complet
        full_prompt = self._build_prompt(user_message)
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 400,
                    "stop": ["Utilisateur:", "User:"]
                }
            })
            
            if response.status_code == 200:
                bot_response = response.json()["response"].strip()
                
                # Nettoyer la réponse
                bot_response = self._clean_response(bot_response)
                
                # Sauvegarder dans l'historique
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_message,
                    "bot": bot_response
                })
                
                return {
                    "success": True,
                    "response": bot_response,
                    "model": self.model,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Erreur HTTP: {response.status_code}",
                    "response": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de communication: {str(e)}",
                "response": None
            }
    
    def _build_prompt(self, user_message: str) -> str:
        """Construit le prompt complet avec contexte"""
        prompt = f"{self.system_prompt}\n\n"
        
        # Ajouter l'historique récent (3 derniers échanges)
        recent_history = self.conversation_history[-3:]
        for exchange in recent_history:
            prompt += f"Utilisateur: {exchange['user']}\n"
            prompt += f"CofiBot: {exchange['bot']}\n\n"
        
        prompt += f"Utilisateur: {user_message}\nCofiBot: "
        
        return prompt
    
    def _clean_response(self, response: str) -> str:
        """Nettoie la réponse du modèle"""
        # Supprimer les préfixes indésirables
        prefixes_to_remove = ["CofiBot:", "Assistant:", "Bot:", "AI:"]
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        # Supprimer les suffixes indésirables
        suffixes_to_remove = ["Utilisateur:", "User:", "Human:"]
        for suffix in suffixes_to_remove:
            if suffix in response:
                response = response.split(suffix)[0].strip()
        
        return response
    
    def get_stats(self) -> Dict[str, Any]:
        """Statistiques de conversation"""
        return {
            "total_conversations": len(self.conversation_history),
            "model_used": self.model,
            "last_conversation": self.conversation_history[-1]["timestamp"] if self.conversation_history else None
        }
    
    def clear_history(self):
        """Efface l'historique de conversation"""
        self.conversation_history = []

# Interface de test
def interactive_chat():
    """Interface de chat interactive"""
    cofibot = CofiBotLlama()
    
    print("🤖 CofiBot avec Llama 3.2 3B")
    print("=" * 50)
    
    # Vérifier la disponibilité
    available, message = cofibot.is_available()
    if not available:
        print(f"❌ {message}")
        print("\n💡 Solutions:")
        print("1. Lance 'ollama serve' dans un terminal")
        print("2. Vérifie que le modèle est installé avec 'ollama list'")
        return
    
    print("✅ CofiBot est prêt !")
    print("💬 Tape 'quit' pour quitter, 'clear' pour effacer l'historique\n")
    
    while True:
        user_input = input("👤 Toi: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Au revoir !")
            break
        
        if user_input.lower() == 'clear':
            cofibot.clear_history()
            print("🗑️ Historique effacé !")
            continue
        
        if user_input.lower() == 'stats':
            stats = cofibot.get_stats()
            print(f"📊 Statistiques: {stats}")
            continue
        
        if not user_input:
            continue
        
        print("🤖 CofiBot réfléchit...", end="", flush=True)
        result = cofibot.chat(user_input)
        print("\r" + " " * 25 + "\r", end="")  # Effacer le message "réfléchit"
        
        if result["success"]:
            print(f"🤖 CofiBot: {result['response']}\n")
        else:
            print(f"❌ Erreur: {result['error']}\n")

if __name__ == "__main__":
    interactive_chat()
