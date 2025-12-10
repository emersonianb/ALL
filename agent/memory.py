# agent/memory.py
import json
from datetime import datetime
from pathlib import Path

class MemoryManager:
    def __init__(self, path="data/memory.json"):
        self.path = Path(path)
        if not self.path.exists():
            self.path.write_text(json.dumps({}))

    def load(self):
        return json.loads(self.path.read_text())

    def save(self, data):
        self.path.write_text(json.dumps(data, indent=2))

    # ----------------------------------------
    # HISTÓRICO DO BOT
    # ----------------------------------------
    def update_history(self, user_id, message, emotion):
        data = self.load()
        if user_id not in data:
            data[user_id] = {
                "history": [],
                "profile": {},
                "learning_state": {},
                "taught_words": [],
                "taught_topics": []
            }

        data[user_id]["history"].append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "emotion": emotion
        })

        self.save(data)

    def get_context(self, user_id):
        data = self.load()
        if user_id in data:
            return data[user_id].get("history", [])[-5:]
        return []

    # ----------------------------------------
    # PERFIL DO USUÁRIO
    # ----------------------------------------
    def set_user_profile(self, user_id, nivel, modulo):
        data = self.load()
        if user_id not in data:
            data[user_id] = {
                "history": [],
                "profile": {},
                "learning_state": {}
            }

        data[user_id]["profile"].update({
            "nivel": nivel,
            "modulo": modulo,
            "created_at": datetime.now().isoformat()
        })

        self.save(data)

    def get_user_profile(self, user_id):
        data = self.load()
        if user_id in data:
            return data[user_id].get("profile", {})
        return {}

    # ----------------------------------------
    # ESTADO DE APRENDIZADO (LEARNING STATE)
    # ----------------------------------------
    def get_learning_state(self, user_id):
        data = self.load()
        if user_id in data:
            return data[user_id].get("learning_state", {})
        return {}

    def update_learning_state(self, user_id, nivel=None, modulo_atual=None, ultimo_topico=None, emocao_recente=None, categoria_atual=None, **kwargs):
        data = self.load()

        # 🔹 Garante que toda a estrutura exista
        if user_id not in data:
            data[user_id] = {
                "history": [],
                "profile": {},
                "learning_state": {}
            }

        learning_state = data[user_id]["learning_state"]

        # 🔹 Atualiza somente os valores enviados
        if nivel is not None:
            learning_state["nivel"] = nivel
        if modulo_atual is not None:
            learning_state["modulo_atual"] = modulo_atual
        if ultimo_topico is not None:
            learning_state["ultimo_topico"] = ultimo_topico
        if emocao_recente is not None:
            learning_state["emocao_recente"] = emocao_recente
        if categoria_atual is not None:
            learning_state["categoria_atual"] = categoria_atual

        # 🔹 Atualiza quaisquer campos extras passados via kwargs
        for key, value in kwargs.items():
            learning_state[key] = value

        # 🔹 Atualiza sempre a última modificação
        learning_state["updated_at"] = datetime.now().isoformat()

        self.save(data)
    
    def add_taught_word(self, user_id, word):
        data = self.load()
        if user_id not in data:
            return
        if "taught_words" not in data[user_id]:
            data[user_id]["taught_words"] = []

        if word.lower() not in [w.lower() for w in data[user_id]["taught_words"]]:
            data[user_id]["taught_words"].append(word)

        self.save(data)

    def add_taught_topic(self, user_id, topic):
        data = self.load()
        if user_id not in data:
            return
        if "taught_topics" not in data[user_id]:
            data[user_id]["taught_topics"] = []

        if topic.lower() not in [t.lower() for t in data[user_id]["taught_topics"]]:
            data[user_id]["taught_topics"].append(topic)

        self.save(data)

    def get_taught_words(self, user_id):
        data = self.load()
        return data.get(user_id, {}).get("taught_words", [])

    def get_taught_topics(self, user_id):
        data = self.load()
        return data.get(user_id, {}).get("taught_topics", [])
