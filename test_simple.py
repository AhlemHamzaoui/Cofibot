import requests
import json

def chat_cofibot(message):
    """Chat avec contexte Coficab"""
    
    # Prompt système pour CofiBot
    system_context = """Tu es CofiBot, l'assistant intelligent de Coficab.

CONTEXTE COFICAB:
- Coficab est une entreprise française leader dans la fabrication de câbles automobiles
- Spécialisée dans les faisceaux électriques pour l'industrie automobile
- Expertise en câblage haute performance, connectique et systèmes électriques
- Certifiée ISO 9001 pour la qualité
- Clients : constructeurs automobiles européens (Renault, PSA, etc.)
- Siège social en France, usines en Europe

TON RÔLE:
- Assistant professionnel et amical
- Expert en câbles automobiles et électronique
- Aide les employés avec leurs questions techniques et administratives
- Réponds toujours en français

INSTRUCTIONS:
- Présente-toi comme CofiBot de Coficab
- Utilise tes connaissances sur l'automobile et l'électronique
- Sois précis et professionnel"""

    full_prompt = f"{system_context}\n\nEmployé: {message}\nCofiBot: "
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:3b",
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 300
            }
        })
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Erreur: {response.status_code}"
            
    except Exception as e:
        return f"Erreur: {e}"

# Tests
if __name__ == "__main__":
    print("🧪 Test CofiBot avec contexte")
    print("=" * 50)
    
    # Test 1: Présentation
    print("🎯 Test 1: Présentation")
    response = chat_cofibot("Bonjour, peux-tu te présenter ?")
    print(f"CofiBot: {response}\n")
    
    # Test 2: Question technique
    print("🎯 Test 2: Question technique")
    response = chat_cofibot("Qu'est-ce qu'un faisceau électrique automobile ?")
    print(f"CofiBot: {response}\n")
    
    # Test 3: Question sur l'entreprise
    print("🎯 Test 3: Question sur Coficab")
    response = chat_cofibot("Quels sont nos principaux clients ?")
    print(f"CofiBot: {response}\n")
