from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cofibot_llama import CofiBotLlama
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Modèles Pydantic
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    model: str
    timestamp: str
    success: bool

# Initialiser FastAPI
app = FastAPI(
    title="CofiBot LLM Local API",
    description="API CofiBot avec Llama 3.2 3B local",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser CofiBot
cofibot = CofiBotLlama()

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    available, message = cofibot.is_available()
    
    return {
        "message": "🤖 CofiBot LLM Local API",
        "version": "2.0.0",
        "model": cofibot.model,
        "status": "ready" if available else "error",
        "details": message,
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "stats": "/stats"
        }
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état"""
    available, message = cofibot.is_available()
    
    return {
        "status": "healthy" if available else "unhealthy",
        "model": cofibot.model,
        "available": available,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Endpoint de chat principal"""
    if not message.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")
    
    result = cofibot.chat(message.message)
    
    if not result["success"]:
        raise HTTPException(status_code=503, detail=result["error"])
    
    return ChatResponse(
        response=result["response"],
        model=result["model"],
        timestamp=result["timestamp"],
        success=True
    )

@app.get("/stats")
async def get_stats():
    """Statistiques de l'API"""
    stats = cofibot.get_stats()
    available, message = cofibot.is_available()
    
    return {
        **stats,
        "api_status": "ready" if available else "error",
        "api_message": message
    }

@app.post("/clear")
async def clear_history():
    """Effacer l'historique"""
    cofibot.clear_history()
    return {"message": "Historique effacé avec succès"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Lancement de CofiBot LLM Local API...")
    uvicorn.run("api_with_llama:app", host="127.0.0.1", port=8001, reload=True)
