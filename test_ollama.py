import requests
import json

def chat_with_ollama(message, model="mistral:7b"):
    """
    Fonction pour discuter avec Ollama
    """
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": message,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Erreur HTTP: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "❌ Erreur: Ollama n'est pas en marche. Lance 'ollama serve' dans un terminal."
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

def chat_streaming(message, model="mistral:7b"):
    """
    Chat avec streaming (réponse en temps réel)
    """
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": message,
        "stream": True
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        
        print("🤖 Réponse: ", end="", flush=True)
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    print(data["response"], end="", flush=True)
                if data.get("done", False):
                    print("\n")
                    break
                    
    except Exception as e:
        print(f"❌ Erreur: {e}")

# Tests
if __name__ == "__main__":
    print("🧪 Test de connexion avec Ollama...")
    
    # Test simple
    response = chat_with_ollama("Bonjour ! Peux-tu te présenter en français ?")
    print(f"Réponse: {response}")
    
    print("\n" + "="*50 + "\n")
    
    # Test avec streaming
    chat_streaming("Explique-moi ce qu'est un chatbot en 3 phrases.")
