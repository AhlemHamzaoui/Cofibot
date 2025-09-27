import requests
import json
from datetime import datetime

def test_ollama_connection():
    """Test de connexion avec Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("✅ Ollama est connecté !")
            print("📋 Modèles disponibles:")
            for model in models:
                print(f"  - {model['name']} ({model['size']} bytes)")
            return True
        else:
            print("❌ Problème de connexion avec Ollama")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama n'est pas en marche. Lance 'ollama serve' dans un terminal.")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def chat_with_llama(message, model="llama3.2:3b"):
    """Chat simple avec Llama"""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": message,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 300
        }
    }
    
    try:
        print("🤖 Llama réfléchit...")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"❌ Erreur HTTP: {response.status_code}"
            
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

def chat_streaming(message, model="llama3.2:3b"):
    """Chat avec réponse en temps réel"""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": message,
        "stream": True
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        
        print("🤖 Llama: ", end="", flush=True)
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
        
        return full_response
                    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return ""

# Tests
if __name__ == "__main__":
    print("🧪 Test de Llama 3.2 3B")
    print("=" * 50)
    
    # Test de connexion
    if not test_ollama_connection():
        exit()
    
    print("\n🎯 Test 1: Question simple")
    response = chat_with_llama("Bonjour ! Peux-tu te présenter en français ?")
    print(f"Réponse: {response}")
    
    print("\n🎯 Test 2: Question sur Coficab")
    response = chat_with_llama("Que sais-tu sur l'industrie automobile et les câbles électriques ?")
    print(f"Réponse: {response}")
    
    print("\n🎯 Test 3: Streaming (temps réel)")
    chat_streaming("Explique-moi en 3 points ce qu'est un chatbot.")
    
    print("\n✅ Tests terminés !")
