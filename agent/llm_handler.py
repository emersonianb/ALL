from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os, re
from dotenv import load_dotenv

load_dotenv()

class LLMHandler:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.llm = ChatGroq(
            model=model,
            temperature=0.4,
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.system_prompt = """
        Você é um tutor de inglês motivador e amigável, falando principalmente em Português.

        --- Regras de Comportamento ---
        - Fale de forma clara, amigável e motivadora.
        - Use emojis apenas para reforçar emoção.
        - Responda com empatia ao estado emocional do aluno.
        - **Nunca repita tópicos ou palavras já ensinadas.**
        - Ensine apenas um novo item por vez.
        - Todo novo termo deve conter:
            1. Palavra/expressão em inglês
            2. Tradução
            3. Pronúncia simplificada (Português)
        - Faça apenas uma pergunta de cada vez.
        - Se o aluno respondeu à última pergunta → continue o mesmo tópico.
        - Se o aluno pediu um método diferente ou demonstrou negatividade → inicie mini-jogo imediatamente.
        - Não inclua saudações automáticas repetidas.
        - Siga SEMPRE a instrução do mini agente

        --- Instruções do mini-agente: ---
        {instruction}

        --- Dados da aula ---
        Level: {nivel}
        Module: {modulo_atual}
        Last topic: {last_topic}
        Previously taught topics: {previous_topics}
        Previously taught vocabulary: {previous_words}
        User emotion: {emotion}
        Has previous sessions: {has_previous_sessions}

        --- RAG Materials ---
        {materials_context}
        """

    def generate(self, context, message, emotion,
                 materials_context="",
                 nivel="A1",
                 modulo_atual="Vocabulary",
                 last_topic="none",
                 previous_topics=None,
                 previous_words=None,
                 has_previous_sessions=False,
                 instruction=""):
        try:
            previous_topics = previous_topics or []
            previous_words = previous_words or []

            previous_topics_str = ", ".join(previous_topics) if previous_topics else "none"
            previous_words_str = ", ".join(previous_words) if previous_words else "none"

            system_prompt_filled = self.system_prompt.format(
                nivel=nivel,
                modulo_atual=modulo_atual,
                emotion=emotion,
                last_topic=last_topic,
                previous_topics=previous_topics_str,
                previous_words=previous_words_str,
                has_previous_sessions=has_previous_sessions,
                instruction=instruction,
                materials_context=materials_context
            )

            dialogue_history = ""
            for entry in context:
                dialogue_history += f"User ({entry['emotion']}): {entry['message']}\n"
            dialogue_history += f"User ({emotion}): {message}"

            messages = [
                SystemMessage(content=system_prompt_filled),
                HumanMessage(content=dialogue_history)
            ]

            response = self.llm.invoke(messages)

            match_word = re.search(r'NEW_TOPIC:\s*([A-Za-z\s]+)', response.content)
            new_word = match_word.group(1).strip() if match_word else None

            user_facing_response = re.sub(r'NEW_TOPIC:\s*[A-Za-z\s]+', '', response.content).strip()
            if new_word and "?" not in user_facing_response:
                user_facing_response += f"\n\nCan you try using '{new_word}' in a sentence?"

            return user_facing_response, new_word

        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "Sorry, there was an error processing your message. Please try again.", None