import requests
import json
import time

def chat_ancien_cofibot(message):
    """Chat avec l'ancien système NLP"""
    try:
        response = requests.post("http://127.0.0.1:8000/chatbot", json={
            "message": message
        })
        if response.status_code == 200:
            data = response.json()
            return data["response"], data["confidence"]
        else:
            return "Erreur ancien système", 0.0
    except:
        return "Ancien système non disponible", 0.0

def chat_nouveau_llm(message):
    """Chat avec le nouveau LLM"""
    system_context = """Tu es CofiBot, l'assistant de Coficab (fabricant de câbles automobiles français). 
    Réponds de manière professionnelle et concise."""
    
    full_prompt = f"{system_context}\n\nEmployé: {message}\nCofiBot: "
    
    try:
        start_time = time.time()
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:3b",
            "prompt": full_prompt,
            "stream": False,
            "options": {"temperature": 0.7, "max_tokens": 200}
        })
        end_time = time.time()
        
        if response.status_code == 200:
            return response.json()["response"], end_time - start_time
        else:
            return "Erreur LLM", 0.0
    except:
        return "LLM non disponible", 0.0

def comparer_systemes():
    """Compare les deux systèmes"""
    questions_test = [
        "Bonjour",
        "Quels sont les horaires ?",
        "Comment faire une demande de congés ?",
        "Qu'est-ce qu'un câble automobile ?",
        "Peux-tu m'expliquer les normes ISO ?",
        "Comment contacter le service RH ?"
    ]
    
    print("🔄 COMPARAISON DES SYSTÈMES COFIBOT")
    print("=" * 60)
    
    for i, question in enumerate(questions_test, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 40)
        
        # Ancien système
        print("🔹 ANCIEN (NLP classique):")
        ancien_response, confidence = chat_ancien_cofibot(question)
        print(f"   Réponse: {ancien_response}")
        print(f"   Confiance: {confidence:.2f}")
        
        # Nouveau système
        print("🔹 NOUVEAU (LLM local):")
        nouveau_response, temps = chat_nouveau_llm(question)
        print(f"   Réponse: {nouveau_response}")
        print(f"   Temps: {temps:.2f}s")
        
        print()

if __name__ == "__main__":
    comparer_systemes()
