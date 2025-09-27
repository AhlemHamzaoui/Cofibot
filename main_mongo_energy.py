from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from services.mongo_energy_llm import MongoEnergyLLMService
from models.energy_models_mongo import ChatMessage
from datetime import datetime
import os

# Initialiser l'application
app = FastAPI(
    title="CofiBot Energy Manager MongoDB API",
    description="Assistant IA pour la gestion énergétique Coficab avec MongoDB",
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

# Service LLM
energy_service = MongoEnergyLLMService()

def verify_user_role(user_role: str):
    """Vérifie les permissions utilisateur"""
    if user_role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=403, 
            detail="Accès réservé aux managers et administrateurs"
        )

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "🔋 CofiBot Energy Manager MongoDB API",
        "version": "2.0.0",
        "description": "Assistant IA pour managers énergie Coficab",
        "database": "MongoDB",
        "capabilities": [
            "Analyse consommation par ligne de production",
            "Suivi détaillé des équipements",
            "Gestion des factures mensuelles",
            "Détection d'anomalies",
            "Recommandations d'optimisation"
        ],
        "lignes_production": [
            "LIGNE_001", "LIGNE_002", "LIGNE_003", "LIGNE_004", "LIGNE_005"
        ]
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état du système"""
    try:
        # Tester la connexion MongoDB
        db_status = energy_service.db.consommations.count_documents({}) >= 0
        
        # Tester la connexion LLM
        test_response = energy_service.generate_response(
            "Test de connexion", 
            "system"
        )
        
        llm_status = test_response["success"]
        
        return {
            "status": "healthy" if (db_status and llm_status) else "degraded",
            "mongodb_available": db_status,
            "llm_available": llm_status,
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
    
    # Vérifier les permissions
    verify_user_role(message.user_role)
    
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
            "timestamp": result["timestamp"],
            "parsed_request": result.get("parsed_request")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lignes")
async def get_lignes():
    """Liste des lignes de production"""
    return {
        "lignes": [
            {"id": "LIGNE_001", "name": "Ligne Production 1", "ip": "192.168.1.10"},
            {"id": "LIGNE_002", "name": "Ligne Production 2", "ip": "192.168.1.11"},
            {"id": "LIGNE_003", "name": "Ligne Production 3", "ip": "192.168.1.12"},
            {"id": "LIGNE_004", "name": "Ligne Production 4", "ip": "192.168.1.13"},
            {"id": "LIGNE_005", "name": "Ligne Production 5", "ip": "192.168.1.14"}
        ]
    }

@app.get("/equipements")
async def get_equipements():
    """Liste des équipements surveillés"""
    top_equipements = energy_service.db.get_top_equipements(20)
    return {"equipements": top_equipements}

@app.get("/stats")
async def get_global_stats():
    """Statistiques globales"""
    analytics = energy_service.db.get_analytics()
    return analytics

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Téléchargement de fichiers (factures)"""
    file_path = f"data/factures/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        file_path,
        filename=filename,
        media_type='application/pdf'
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Lancement de CofiBot Energy Manager MongoDB...")
    uvicorn.run("main_mongo_energy:app", host="127.0.0.1", port=8003, reload=True)
