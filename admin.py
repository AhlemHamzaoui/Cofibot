from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

templates = Jinja2Templates(directory="templates")

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Interface d'administration"""
    # Charger les statistiques
    with open("nlp/intents.json", "r", encoding="utf-8") as f:
        intents = json.load(f)
    
    stats = {
        "total_intents": len(intents["intents"]),
        "total_patterns": sum(len(intent["patterns"]) for intent in intents["intents"]),
        "total_responses": sum(len(intent["responses"]) for intent in intents["intents"])
    }
    
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "stats": stats,
        "intents": intents["intents"]
    })

@app.post("/admin/add-intent")
async def add_intent(
    tag: str = Form(...),
    patterns: str = Form(...),
    responses: str = Form(...)
):
    """Ajouter une nouvelle intention"""
    # Charger les intentions existantes
    with open("nlp/intents.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Ajouter la nouvelle intention
    new_intent = {
        "tag": tag,
        "patterns": [p.strip() for p in patterns.split("\n") if p.strip()],
        "responses": [r.strip() for r in responses.split("\n") if r.strip()]
    }
    
    data["intents"].append(new_intent)
    
    # Sauvegarder
    with open("nlp/intents.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return {"message": "Intention ajoutée avec succès"}
