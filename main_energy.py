from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from services.energy_llm import EnergyLLMService
from models.energy_models import ChatMessage, ChatResponse
from datetime import datetime
import os

# Initialiser l'application
app = FastAPI(
    title="CofiBot Energy Manager API",
    description="Assistant IA pour la gestion énergétique de Coficab",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service LLM
energy_service = EnergyLLMService()

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "🔋 CofiBot Energy Manager API",
        "version": "1.0.0",
        "description": "Assistant IA pour managers énergie Coficab",
        "capabilities": [
            "Analyse de consommation énergétique",
            "Génération de rapports",
            "Accès aux factures",
            "Recommandations d'optimisation"
        ],
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "download": "/download/{filename}"
        }
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état du système"""
    try:
        # Tester la connexion LLM
        test_response = energy_service.generate_response(
            "Test de connexion", 
            "system"
        )
        
        llm_status = test_response["success"]
        
        return {
            "status": "healthy" if llm_status else "degraded",
            "llm_available": llm_status,
            "database_available": True,  # Toujours True pour SQLite
            "timestamp": datetime.now().isoformat(),
            "model": energy_service.model
        }
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    """Endpoint principal de chat"""
    if not message.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")
    
    # Vérifier les permissions (simulation)
    if message.user_role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=403, 
            detail="Accès réservé aux managers et administrateurs"
        )
    
    try:
        result = energy_service.generate_response(
            message.message, 
            message.user_id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=503, detail=result["error"])
        
        return {
            "response": result["response"],
            "data": result.get("data"),
            "charts": result.get("charts", []),
            "files": result.get("files", []),
            "timestamp": result["timestamp"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Téléchargement de fichiers (factures, rapports)"""
    file_path = f"data/files/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        file_path,
        filename=filename,
        media_type='application/pdf'
    )

@app.get("/sites")
async def get_sites():
    """Liste des sites disponibles"""
    return {
        "sites": [
            {"id": "COFICAB_MAIN", "name": "Site Principal"},
            {"id": "COFICAB_PROD_A", "name": "Production A"},
            {"id": "COFICAB_PROD_B", "name": "Production B"}
        ]
    }

@app.get("/energy-types")
async def get_energy_types():
    """Types d'énergie surveillés"""
    return {
        "energy_types": [
            {"id": "electricity", "name": "Électricité", "unit": "kWh"},
            {"id": "gas", "name": "Gaz", "unit": "kWh"},
            {"id": "water", "name": "Eau", "unit": "m³"},
            {"id": "compressed_air", "name": "Air comprimé", "unit": "kWh"},
            {"id": "steam", "name": "Vapeur", "unit": "kg"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Lancement de CofiBot Energy Manager...")
    uvicorn.run("main_energy:app", host="127.0.0.1", port=8002, reload=True)
