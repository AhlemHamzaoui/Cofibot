import requests
import json
from datetime import datetime

class OllamaCofiBot:
    def __init__(self, model="mistral:7b"):
        self.model = model
        self.base_url = "http://localhost:11434"
        self.conversation_history = []
        
        # Prompt système pour CofiBot
        self.system_prompt = """Tu es CofiBot, l'assistant intelligent de Coficab, une entreprise française spécialisée dans la fabrication de câbles automobiles.

Tes caractéristiques:
- Tu réponds en français
- Tu es professionnel mais amical
- Tu connais le domaine automobile et électrique
- Tu aides les employés de Coficab avec leurs questions

Si tu ne connais pas une information spécifique à Coficab, dis-le clairement et propose d'autres solutions."""
    
    def is_ollama_running(self):
        """Vérifie si Ollama est en marche"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def list_models(self):
        """Liste les modèles disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except:
            return []
    
    def chat(self, user_message):
        """Discute avec l'utilisateur"""
        if not self.is_ollama_running():
            return {
                "error": "❌ Ollama n'est pas en marche. Lance 'ollama serve' dans un terminal.",
                "response": None
            }
        
        # Construire le prompt avec l'historique
        full_prompt = f"{self.system_prompt}\n\n"
        
        # Ajouter l'historique récent (5 derniers échanges)
        for exchange in self.conversation_history[-5:]:
            full_prompt += f"Utilisateur: {exchange['user']}\n"
            full_prompt += f"CofiBot: {exchange['bot']}\n\n"
        
        full_prompt += f"Utilisateur: {user_message}\nCofiBot:"
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            })
            
            if response.status_code == 200:
                bot_response = response.json()["response"].strip()
                
                # Sauvegarder dans l'historique
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_message,
                    "bot": bot_response
                })
                
                return {
                    "response": bot_response,
                    "model": self.model,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "error": f"Erreur HTTP: {response.status_code}",
                    "response": None
                }
                
        except Exception as e:
            return {
                "error": f"Erreur: {str(e)}",
                "response": None
            }
    
    def chat_stream(self, user_message):
        """Chat avec streaming"""
        if not self.is_ollama_running():
            print("❌ Ollama n'est pas en marche.")
            return
        
        full_prompt = f"{self.system_prompt}\n\nUtilisateur: {user_message}\nCofiBot:"
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": True
            }, stream=True)
            
            print("🤖 CofiBot: ", end="", flush=True)
            full_response = ""
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        chunk = data["response"]
                        print(chunk, end="", flush=True)
                        full_response += chunk
                    if data.get("done", False):
                        print("\n")
                        break
            
            # Sauvegarder dans l'historique
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_message,
                "bot": full_response
            })
            
        except Exception as e:
            print(f"❌ Erreur: {e}")

# Interface de test
if __name__ == "__main__":
    cofibot = OllamaCofiBot()
    
    print("🤖 CofiBot avec Ollama")
    print("=" * 40)
    
    # Vérifier si Ollama fonctionne
    if not cofibot.is_ollama_running():
        print("❌ Ollama n'est pas en marche.")
        print("Lance 'ollama serve' dans un autre terminal.")
        exit()
    
    # Lister les modèles disponibles
    models = cofibot.list_models()
    print(f"📋 Modèles disponibles: {models}")
    
    if not models:
        print("❌ Aucun modèle trouvé. Télécharge un modèle avec 'ollama pull mistral:7b'")
        exit()
    
    print(f"🎯 Utilisation du modèle: {cofibot.model}")
    print("Tape 'quit' pour quitter\n")
    
    # Boucle de conversation
    while True:
        user_input = input("👤 Toi: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Au revoir !")
            break
        
        if not user_input:
            continue
        
        # Utiliser le streaming pour une meilleure expérience
        cofibot.chat_stream(user_input)
        print()
