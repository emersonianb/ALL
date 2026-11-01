from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import json, os
from pathlib import Path


class MaterialFormatter:
    def __init__(self, model="openai/gpt-oss-120b"):
        self.llm = ChatGroq(
            model=model,
            temperature=0.0,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def format(self, raw_text):
        prompt = f"""
        Você é um formatador de conteúdo. Extraia do texto abaixo:

        - "tema": uma frase curta explicando o tema.
        - "conteudo": o conteúdo puro.

        Retorne SOMENTE um JSON válido:
        {{
        "tema": "...",
        "conteudo": "..."
        }}

        Texto:
        {raw_text}
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()

        try:
            return json.loads(content)
        except:
            start = content.find("{")
            end = content.rfind("}") + 1
            return json.loads(content[start:end])

class MaterialManager:
    def __init__(self, base_folder="data/users", formatter=None):
        self.base_folder = Path(base_folder)
        self.formatter = formatter  # << adicionar

    def get_user_folder(self, user_id):
        user_path = self.base_folder / str(user_id)
        user_path.mkdir(parents=True, exist_ok=True)

        for file in ["Conversacao.json", "Gramatica.json", "Vocabulario.json"]:
            path = user_path / file
            if not path.exists():
                path.write_text(json.dumps({"items": []}, indent=2), encoding="utf-8")

        return user_path

    def add_material(self, user_id, category, raw_text):
        folder = self.get_user_folder(user_id)

        file_map = {
            "conversacao": "Conversacao.json",
            "gramatica": "Gramatica.json",
            "vocabulario": "Vocabulario.json"
        }

        file_path = folder / file_map[category]
        data = json.loads(file_path.read_text(encoding="utf-8"))

        # FORMATADOR ENTRA AQUI 🔥
        if self.formatter:
            structured = self.formatter.format(raw_text)
        else:
            structured = {"tema": "Indefinido", "conteudo": raw_text}

        data["items"].append(structured)

        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return file_path
