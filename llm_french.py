from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class FrenchLLM:
    def __init__(self):
        # Modèle français optimisé
        self.model_name = "microsoft/DialoGPT-medium"  # Ou un modèle français spécifique
        self.tokenizer = None
        self.model = None
        
    def load_model(self):
        """Charge un modèle optimisé pour le français"""
        print("📥 Chargement du modèle français...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Ajouter un token de padding si nécessaire
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print("✅ Modèle français chargé !")
            return True
            
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return False
    
    def chat(self, message, max_length=150):
        """Chat en français"""
        if not self.model or not self.tokenizer:
            return "Modèle non chargé"
        
        # Encoder le message
        inputs = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors="pt")
        
        # Générer la réponse
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Décoder la réponse
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Retourner seulement la nouvelle partie
        return response[len(message):].strip()

# Test
if __name__ == "__main__":
    llm = FrenchLLM()
    if llm.load_model():
        response = llm.chat("Bonjour, pouvez-vous m'aider ?")
        print(f"Réponse : {response}")
