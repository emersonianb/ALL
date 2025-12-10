from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path
import json

class GuideRAG:
    def __init__(self, user_id, categoria=None, max_items=5):
        # pasta do usuário
        folder = Path(f"data/users/{user_id}")

        # mapeamento da categoria para os arquivos JSON
        file_map = {
            "conversacao": "Conversacao.json",
            "gramatica": "Gramatica.json",
            "vocabulario": "Vocabulario.json"
        }

        self.documents = []

        if categoria and categoria in file_map:
            # carrega apenas o arquivo da categoria
            file_path = folder / file_map[categoria]
            if file_path.exists():
                data = json.loads(file_path.read_text(encoding="utf-8"))
                items = data.get("items", [])
                # pega apenas os últimos max_items
                last_items = items[-max_items:]
                if last_items:
                    text = ""
                    for item in last_items:
                        if isinstance(item, dict):
                            tema = item.get("tema", "Sem tema")
                            conteudo = item.get("conteudo", "")
                            text += f"\nTema: {tema}\n{conteudo}\n"
                        else:
                            text += f"\n{str(item)}\n"
                    self.documents.append(Document(page_content=text))
        else:
            # carrega todos os arquivos do usuário
            for file_path in folder.glob("*.json"):
                data = json.loads(file_path.read_text(encoding="utf-8"))
                items = data.get("items", [])
                last_items = items[-max_items:]
                if last_items:
                    text = ""
                    for item in last_items:
                        if isinstance(item, dict):
                            tema = item.get("tema", "Sem tema")
                            conteudo = item.get("conteudo", "")
                            text += f"\nTema: {tema}\n{conteudo}\n"
                        else:
                            text += f"\n{str(item)}\n"
                    self.documents.append(Document(page_content=text))

        # se não tiver nada salvo → RAG desativado
        if not self.documents:
            self.vectorstore = None
            return

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(self.documents)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = Chroma.from_documents(chunks, embeddings)

    def query(self, question, k=3):
        if not self.vectorstore:
            return ""
        results = self.vectorstore.similarity_search(question, k=k)
        text = ""
        for r in results:
            content = r.page_content if hasattr(r, "page_content") else str(r)
            try:
                parsed = json.loads(content)
                tema = parsed.get("tema", "Sem tema")
                conteudo = parsed.get("conteudo", "")
                text += f"\nTema: {tema}\n{conteudo}\n"
            except:
                text += f"\n{content}\n"
        return text.strip()