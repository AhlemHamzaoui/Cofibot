from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import json
import random
import os
from typing import Dict, Any, List
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if not load_model():
        print("⚠️ Impossible de charger le modèle. Certaines fonctionnalités ne marcheront pas.")
    yield
    # Shutdown (si nécessaire)

# Initialisation de l'application FastAPI avec lifespan
app = FastAPI(
    title="CofiBot API",
    description="Chatbot intelligent pour Coficab",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS pour admin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
class Question(BaseModel):
    message: str

class ChatResponse(BaseModel):
    intent: str
    response: str
    confidence: float

class Intent(BaseModel):
    tag: str
    patterns: List[str]
    responses: List[str]

class IntentUpdate(BaseModel):
    tag: str
    patterns: List[str]
    responses: List[str]

# Variables globales pour le modèle
vectorizer = None
model = None
intents_data = None
conversation_history = []

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

def save_intents():
    """Sauvegarde les intentions dans le fichier JSON"""
    try:
        data = {"intents": intents_data}
        with open("nlp/intents.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde : {e}")
        return False

def retrain_model():
    """Réentraîne le modèle avec les nouvelles données"""
    try:
        import subprocess
        result = subprocess.run(["python", "nlp/train_nlp.py"], capture_output=True, text=True)
        if result.returncode == 0:
            # Recharger le modèle
            load_model()
            return True
        return False
    except Exception as e:
        print(f"❌ Erreur réentraînement : {e}")
        return False

# Routes existantes
@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "🤖 CofiBot API est en ligne !",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chatbot",
            "health": "/health",
            "admin": "/admin"
        }
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    model_loaded = vectorizer is not None and model is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "intents_loaded": intents_data is not None,
        "total_intents": len(intents_data) if intents_data else 0
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
                
                # Sauvegarder dans l'historique
                conversation_history.append({
                    "id": len(conversation_history) + 1,
                    "timestamp": datetime.now().isoformat(),
                    "user_message": query.message,
                    "bot_response": response,
                    "intent": prediction,
                    "confidence": round(confidence, 2)
                })
                
                return ChatResponse(
                    intent=prediction,
                    response=response,
                    confidence=round(confidence, 2)
                )
        
        # Intention non trouvée
        response = "Je ne comprends pas ta demande 😕. Peux-tu reformuler ?"
        conversation_history.append({
            "id": len(conversation_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "user_message": query.message,
            "bot_response": response,
            "intent": "unknown",
            "confidence": 0.0
        })
        
        return ChatResponse(
            intent="unknown",
            response=response,
            confidence=0.0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")

# 🆕 Routes d'administration
@app.get("/admin/stats")
async def get_admin_stats():
    """Statistiques pour l'interface admin"""
    if not intents_data:
        raise HTTPException(status_code=503, detail="Données non chargées")
    
    total_patterns = sum(len(intent["patterns"]) for intent in intents_data)
    total_responses = sum(len(intent["responses"]) for intent in intents_data)
    
    # Statistiques des conversations
    intent_usage = {}
    for conv in conversation_history:
        intent = conv["intent"]
        intent_usage[intent] = intent_usage.get(intent, 0) + 1
    
    return {
        "total_intents": len(intents_data),
        "total_patterns": total_patterns,
        "total_responses": total_responses,
        "total_conversations": len(conversation_history),
        "intent_usage": intent_usage,
        "model_accuracy": "75%" if model else "N/A"
    }

@app.get("/admin/intents")
async def get_intents():
    """Récupérer toutes les intentions"""
    if not intents_data:
        raise HTTPException(status_code=503, detail="Données non chargées")
    
    return {"intents": intents_data}

@app.post("/admin/intents")
async def create_intent(intent: Intent):
    """Créer une nouvelle intention"""
    if not intents_data:
        raise HTTPException(status_code=503, detail="Données non chargées")
    
    # Vérifier si l'intention existe déjà
    for existing_intent in intents_data:
        if existing_intent["tag"] == intent.tag:
            raise HTTPException(status_code=400, detail="Cette intention existe déjà")
    
    # Ajouter la nouvelle intention
    new_intent = {
        "tag": intent.tag,
        "patterns": intent.patterns,
        "responses": intent.responses
    }
    
    intents_data.append(new_intent)
    
    # Sauvegarder
    if save_intents():
        # Réentraîner le modèle
        if retrain_model():
            return {"message": "Intention créée et modèle réentraîné avec succès"}
        else:
            return {"message": "Intention créée, mais erreur lors du réentraînement"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de la sauvegarde")

@app.put("/admin/intents/{intent_tag}")
async def update_intent(intent_tag: str, intent: IntentUpdate):
    """Modifier une intention existante"""
    if not intents_data:
        raise HTTPException(status_code=503, detail="Données non chargées")
    
    # Trouver l'intention à modifier
    for i, existing_intent in enumerate(intents_data):
        if existing_intent["tag"] == intent_tag:
            intents_data[i] = {
                "tag": intent.tag,
                "patterns": intent.patterns,
                "responses": intent.responses
            }
            
            # Sauvegarder
            if save_intents():
                if retrain_model():
                    return {"message": "Intention modifiée et modèle réentraîné avec succès"}
                else:
                    return {"message": "Intention modifiée, mais erreur lors du réentraînement"}
            else:
                raise HTTPException(status_code=500, detail="Erreur lors de la sauvegarde")
    
    raise HTTPException(status_code=404, detail="Intention non trouvée")

@app.delete("/admin/intents/{intent_tag}")
async def delete_intent(intent_tag: str):
    """Supprimer une intention"""
    if not intents_data:
        raise HTTPException(status_code=503, detail="Données non chargées")
    
    # Trouver et supprimer l'intention
    for i, intent in enumerate(intents_data):
        if intent["tag"] == intent_tag:
            del intents_data[i]
            
            # Sauvegarder
            if save_intents():
                if retrain_model():
                    return {"message": "Intention supprimée et modèle réentraîné avec succès"}
                else:
                    return {"message": "Intention supprimée, mais erreur lors du réentraînement"}
            else:
                raise HTTPException(status_code=500, detail="Erreur lors de la sauvegarde")
    
    raise HTTPException(status_code=404, detail="Intention non trouvée")

@app.get("/admin/conversations")
async def get_conversations():
    """Récupérer l'historique des conversations"""
    return {"conversations": conversation_history[-50:]}  # 50 dernières conversations

@app.post("/admin/retrain")
async def retrain_model_endpoint():
    """Réentraîner le modèle manuellement"""
    if retrain_model():
        return {"message": "Modèle réentraîné avec succès"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors du réentraînement")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
