from langchain_groq import ChatGroq
import os

class EmotionAnalyser:
    def __init__(self, groq_model="openai/gpt-oss-120b"):
        try:
            self.llm = ChatGroq(
                model=groq_model,
                temperature=0.0,  # respostas objetivas
                api_key=os.getenv("GROQ_API_KEY")
            )
        except Exception:
            # fallback automático
            print(f"Model {groq_model} not available, switching to default llama-3.3-70b-versatile")
            self.llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.0,
                api_key=os.getenv("GROQ_API_KEY")
            )

    def analyse(self, text):
        """
        Analisa emoção do usuário.
        Retorna: 'positive', 'neutral', 'negative', ou categorias extendidas.
        """
        prompt = (
            "You are a strict emotion analyser. Classify the user's sentiment into one of the categories: "
            "'positive', 'neutral', 'negative', 'frustrated', 'confident'. "
            "Respond ONLY with the category name. Do not add anything else. "
            f"User text: '{text}'"
        )

        try:
            response = self.llm.invoke(prompt)
            emotion = response.content.strip().lower()
            if emotion in ["positive", "neutral", "negative", "frustrated", "confident"]:
                return emotion
            return "neutral"
        except Exception as e:
            print(f"Error analyzing emotion: {e}")
            return "neutral"
