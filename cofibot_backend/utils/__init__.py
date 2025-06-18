from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import json
import random
import os
from typing import Dict, Any

# Initialisation de l'application FastAPI
app = FastAPI(
    title="CofiBot API",
    description="Chatbot intelligent pour Coficab",
    version="1.0.0"
)

# Modèles Pydantic
class Question(BaseModel):
    message: str

class ChatResponse(BaseModel):
    intent: str
    response: str
    confidence: float

# Variables globales pour le modèle
vectorizer = None
model = None
intents_data = None

def load_model():
    """Charge le modèle NLP et les données d'intentions"""
    global vectorizer, model, intents_data
    
    try:
        # Charger le modèle
        if os.path.exists("nlp/model.pkl"):
            vectorizer, model = joblib.load("nlp/model.pkl")
            print("✅ Modèle NLP chargé")
        else:
            print("❌ Modèle non trouvé. Lance train_nlp.py d'abord !")
            return False
        
        # Charger les intentions
        with open("nlp/intents.json", "r", encoding="utf-8") as f:
            intents_data = json.load(f)["intents"]
            print("✅ Données d'intentions chargées")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        return False

# Charger le modèle au démarrage
@app.on_event("startup")
async def startup_event():
    if not load_model():
        print("⚠️ Impossible de charger le modèle. Certaines fonctionnalités ne marcheront pas.")

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "🤖 CofiBot API est en ligne !",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chatbot",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    model_loaded = vectorizer is not None and model is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "intents_loaded": intents_data is not None
    }

@app.post("/chatbot", response_model=ChatResponse)
async def chatbot(query: Question):
    """Endpoint principal du chatbot"""
    
    if not vectorizer or not model or not intents_data:
        raise HTTPException(
            status_code=503, 
            detail="Modèle non chargé. Contacte l'administrateur."
        )
    
    user_input = query.message.strip().lower()
    
    if not user_input:
        raise HTTPException(status_code=400, detail="Message vide")
    
    try:
        # Prédiction
        X_input = vectorizer.transform([user_input])
        prediction = model.predict(X_input)[0]
        confidence = max(model.predict_proba(X_input)[0])
        
        # Trouver la réponse correspondante
        for intent in intents_data:
            if intent["tag"] == prediction:
                response = random.choice(intent["responses"])
                return ChatResponse(
                    intent=prediction,
                    response=response,
                    confidence=round(confidence, 2)
                )
        
        # Intention non trouvée
        return ChatResponse(
            intent="unknown",
            response="Je ne comprends pas ta demande 😕. Peux-tu reformuler ?",
            confidence=0.0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
