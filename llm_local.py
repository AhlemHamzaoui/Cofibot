from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class LocalLLM:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        """
        Modèles recommandés :
        - microsoft/DialoGPT-medium (anglais, léger)
        - microsoft/DialoGPT-large (anglais, plus lourd)
        - bigscience/bloom-560m (multilingue, léger)
        - bigscience/bloom-1b7 (multilingue, moyen)
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        
    def load_model(self):
        """Charge le modèle depuis Hugging Face"""
        print(f"📥 Téléchargement du modèle {self.model_name}...")
        
        try:
            # Charger le tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Charger le modèle
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Créer le pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
            
            print("✅ Modèle chargé avec succès !")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement : {e}")
            return False
    
    def generate_response(self, prompt, max_length=100):
        """Génère une réponse à partir d'un prompt"""
        if not self.pipeline:
            return "Modèle non chargé"
        
        try:
            # Générer la réponse
            response = self.pipeline(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extraire le texte généré
            generated_text = response[0]["generated_text"]
            
            # Retourner seulement la partie générée (sans le prompt)
            return generated_text[len(prompt):].strip()
            
        except Exception as e:
            return f"Erreur lors de la génération : {e}"

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialiser le LLM
    llm = LocalLLM("microsoft/DialoGPT-medium")
    
    # Charger le modèle
    if llm.load_model():
        # Tester
        response = llm.generate_response("Bonjour, comment allez-vous ?")
        print(f"Réponse : {response}")
