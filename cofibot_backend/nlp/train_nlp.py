import json
import random
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os

def train_nlp_model():
    """Entraîne le modèle NLP pour la classification d'intentions"""
    
    # Charger les données d'intentions
    with open("nlp/intents.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    texts = []
    labels = []
    
    # Préparer les données d'entraînement
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            texts.append(pattern.lower())  # Normaliser en minuscules
            labels.append(intent["tag"])
    
    print(f"📊 Données chargées : {len(texts)} exemples, {len(set(labels))} intentions")
    
    # Vectorisation TF-IDF
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),  # Unigrammes et bigrammes
        max_features=1000,
        stop_words=None  # Pas de stop words pour le français
    )
    
    X = vectorizer.fit_transform(texts)
    y = labels
    
    # Division train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Entraînement du modèle
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Évaluation
    accuracy = model.score(X_test, y_test)
    print(f"🎯 Précision du modèle : {accuracy:.2%}")
    
    # Sauvegarde
    os.makedirs("nlp", exist_ok=True)
    joblib.dump((vectorizer, model), "nlp/model.pkl")
    
    print("✅ Modèle NLP entraîné et sauvegardé dans nlp/model.pkl")
    return vectorizer, model

if __name__ == "__main__":
    train_nlp_model()
