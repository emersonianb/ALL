# agent/core.py
from .emotions import EmotionAnalyser
from .llm_handler import LLMHandler
from .memory import MemoryManager
from .rag import GuideRAG
from .material_manager import MaterialManager, MaterialFormatter
import re
import json
from pathlib import Path

class AgenticTutor:
    def __init__(self):
        self.emotions = EmotionAnalyser()
        self.memory = MemoryManager()
        self.llm = LLMHandler()
        self.rag = None
        self.user_welcomed = {}  # controla boas-vindas por sessão

    def interpret_student_message(self, last_question, user_message):
        """
        Mini-agente que interpreta a mensagem do aluno e indica
        ao agente principal o que ele deve responder:
        - Continuar o tópico atual (comentar resposta)
        - Introduzir novo tópico
        """
        if not last_question:
            return "new_topic", None  # sem pergunta anterior → novo tópico

        prompt = f"""
        Você é um mini-agente tutor. Analise a mensagem do aluno e indique ao tutor principal o que fazer.

        Pergunta do tutor: "{last_question}"
        Resposta do aluno: "{user_message}"

        Responda em uma linha no formato:
        <AÇÃO> | <INSTRUÇÃO>
        Onde <AÇÃO> é:
          - CONTINUAR: se a resposta do aluno é referente à última pergunta
          - NOVO_TOPICO: se é algo novo

        E <INSTRUÇÃO> é uma sugestão do que o tutor principal deve responder.
        Não inclua saudações.
        """

        result, _ = self.llm.generate(
            context="",
            message=prompt,
            emotion="neutral",
            materials_context="",
            nivel="A1",
            modulo_atual="default",
            last_topic="none",
            previous_words=[],
            previous_topics=[],
            has_previous_sessions=True
        )

        if "|" in result:
            action, instruction = result.split("|", 1)
            return action.strip().upper(), instruction.strip()
        else:
            # fallback caso o LLM não siga o formato
            return "NOVO_TOPICO", result.strip()

    def continue_mini_game(self, user_id):
        learning_state = self.memory.get_learning_state(user_id)
        categoria = learning_state.get("categoria_atual", "vocabulario")
        last_topic = learning_state.get("ultimo_topico", None)

        guides_path = Path("data/guides.json")
        guides = json.loads(guides_path.read_text()) if guides_path.exists() else {}
        category_guide = guides.get(categoria, [])

        previous_topics = self.memory.get_taught_topics(user_id)
        remaining_topics = [t for t in category_guide if t not in previous_topics]
        next_topic = remaining_topics[0] if remaining_topics else category_guide[0] if category_guide else "no available topic"

        self.memory.update_learning_state(user_id, mini_game_active=True, ultimo_topico=next_topic)
        return f"🎲 Let's start the mini-game on {categoria}! First activity is based on the topic '{next_topic}'."

    def respond(self, user_id, message):
        profile = self.memory.get_user_profile(user_id)
        if not profile or "nivel" not in profile or "modulo" not in profile:
            return "Before we start, I need to know your level and module. 🙂"

        # 1. Emotion analysis
        emotion = self.emotions.analyse(message)
        self.memory.update_history(user_id, message, emotion)
        self.memory.update_learning_state(user_id, emocao_recente=emotion)

        # 1b. Detect category
        categoria_atual = None
        msg_lower = message.lower()
        if "vocabulario" in msg_lower or "vocabulário" in msg_lower:
            categoria_atual = "vocabulario"
        elif "gramatica" in msg_lower:
            categoria_atual = "gramatica"
        elif "conversacao" in msg_lower or "conversação" in msg_lower:
            categoria_atual = "conversacao"
        if categoria_atual:
            self.memory.update_learning_state(user_id, categoria_atual=categoria_atual)

        # 2. Current user state
        context = self.memory.get_context(user_id)
        learning_state = self.memory.get_learning_state(user_id)
        last_topic = learning_state.get("ultimo_topico", None)
        modulo_atual = learning_state.get("modulo_atual", profile["modulo"])
        nivel = learning_state.get("nivel", profile["nivel"])

        if "modulo_atual" not in learning_state:
            self.memory.update_learning_state(user_id, modulo_atual=modulo_atual)
        if "nivel" not in learning_state:
            self.memory.update_learning_state(user_id, nivel=nivel)

        previous_words = [w.lower() for w in (self.memory.get_taught_words(user_id) or [])]
        previous_topics = [t.lower() for t in (self.memory.get_taught_topics(user_id) or [])]

        # --- Mini-agente interpreta a mensagem do aluno ---
        ultima_pergunta = learning_state.get("ultima_pergunta", None)
        action, instruction = self.interpret_student_message(
            last_question=ultima_pergunta,
            user_message=message
        )

        if action == "CONTINUAR":
            # continua o tópico atual
            manter_topico = True
        else:
            # novo tópico
            manter_topico = False
            self.memory.update_learning_state(user_id, ultimo_topico=message)

        # 3. Mini-game trigger
        game_in_progress = learning_state.get("mini_game_active", False)
        wants_alternative = any(x in msg_lower for x in ["outra forma", "mudar", "de outra forma", "diferente"])
        if (emotion == "negative" or wants_alternative) and not game_in_progress:
            self.memory.update_learning_state(user_id, mini_game_active=True)
            self.rag = GuideRAG(user_id, categoria=categoria_atual)
            rag_context = self.rag.query(message) if self.rag else ""

            response_text, new_word = self.llm.generate(
                context=context,
                message=instruction or message,
                emotion=emotion,
                materials_context=rag_context,
                nivel=nivel,
                modulo_atual=modulo_atual,
                last_topic=last_topic if last_topic else "none",
                previous_words=previous_words,
                previous_topics=previous_topics,
                has_previous_sessions=False
            )

            self.memory.update_learning_state(user_id, ultima_pergunta=response_text)

            if new_word:
                self.memory.add_taught_word(user_id, new_word)
                self.memory.add_taught_topic(user_id, new_word)
                self.memory.update_learning_state(user_id, ultimo_topico=new_word)

            return response_text

        # 4. RAG / materials
        self.rag = GuideRAG(user_id, categoria=categoria_atual)
        rag_context = self.rag.query(message) if self.rag else ""

        # 5. Generate response usando a instrução do mini-agente
        response, new_word = self.llm.generate(
            context=context,
            message=instruction or message,
            emotion=emotion,
            materials_context=rag_context,
            nivel=nivel,
            modulo_atual=modulo_atual,
            last_topic=last_topic if last_topic else "none",
            previous_words=previous_words,
            previous_topics=previous_topics,
            has_previous_sessions=False
        )

        self.memory.update_learning_state(user_id, ultima_pergunta=response)

        if new_word:
            if new_word.lower() not in previous_words:
                self.memory.add_taught_word(user_id, new_word)
            if new_word.lower() not in previous_topics:
                self.memory.add_taught_topic(user_id, new_word)
            self.memory.update_learning_state(user_id, ultimo_topico=new_word.lower())

        # 6. Save material
        try:
            formatter = MaterialFormatter()
            mat = MaterialManager(formatter=formatter)
            if categoria_atual:
                mat.add_material(user_id=user_id, category=categoria_atual, raw_text=response)
        except Exception as e:
            print("Error saving material automatically:", e)

        return response