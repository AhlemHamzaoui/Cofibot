from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.universal_llm_service import UniversalEnergyLLM
from database.sqlite_db import SQLiteEnergyDB
from database.mongo_db import MongoEnergyDB
from core.models import ChatMessage, DatabaseType
from datetime import datetime
import os

# Configuration
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")  # ou "mongodb"

# Initialiser la base selon le type
if DATABASE_TYPE == "mongodb":
    database = MongoEnergyDB()
else:
    database = SQLiteEnergyDB()

# Initialiser l'application
app = FastAPI(
    title="CofiBot Energy Manager Universal API",
    description=f"Assistant IA avec base {DATABASE_TYPE.upper()}",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service LLM universel
energy_service = UniversalEnergyLLM(database)

@app.get("/")
async def root():
    return {
        "message": "🔋 CofiBot Energy Manager Universal API",
        "version": "3.0.0",
        "database": DATABASE_TYPE.upper(),
        "lignes": database.get_lignes_production()
    }

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    if not message.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")
    
    if message.user_role not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Accès réservé aux managers")
    
    result = energy_service.generate_response(message.message, message.user_id)
    
    if not result["success"]:
        raise HTTPException(status_code=503, detail=result["error"])
    
    return result

@app.get("/health")
async def health_check():
    try:
        lignes = database.get_lignes_production()
        return {
            "status": "healthy",
            "database": DATABASE_TYPE,
            "lignes_count": len(lignes),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Lancement avec base {DATABASE_TYPE.upper()}...")
    uvicorn.run("main_universal:app", host="127.0.0.1", port=8004, reload=True)
