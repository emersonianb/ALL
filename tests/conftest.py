import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from agent.material_manager import MaterialManager
from agent.rag import GuideRAG
from agent.memory import MemoryManager
from agent.llm_handler import LLMHandler
from agent.emotions import EmotionAnalyser


@pytest.fixture
def fake_material_path(tmp_path):
    """Cria um material JSON simples para testes."""
    material = {
        "items": [{
            "tema": "Indefinido",
            "conteudo": "Yesterday I went to the supermarket and bought some bread, milk, and vegetables. It was a sunny day so I walked instead of taking the bus.\nQueria entender melhor o vocabulario e a gramatica envolvida."
        }]
    }

    file_path = tmp_path / "sample_guide.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(material, f, indent=4)

    return file_path


@pytest.fixture
def material_manager():
    """Instancia MaterialManager real."""
    return MaterialManager()


@pytest.fixture
def rag_system(tmp_path):
    user_id = "user123"
    user_folder = tmp_path / "data" / "users" / user_id
    user_folder.mkdir(parents=True, exist_ok=True)

    # cria o arquivo de vocabulario com conteúdo conhecido
    vocab_path = user_folder / "Vocabulario.json"
    vocab_path.write_text(json.dumps({
        "items": [
            {"tema": "Compras", "conteudo": "I went to the supermarket yesterday."}
        ]
    }), encoding="utf-8")

    # Inicializa o RAG apontando para esse user_id
    return GuideRAG(user_id=str(user_folder.parts[-1]), categoria="vocabulario")

def test_rag_index_and_query(rag_system):
    query = "supermarket"
    results = rag_system.query(query, k=1)

    # valida a saída
    assert isinstance(results, str), "O retorno da consulta deve ser uma string"
    assert "supermarket" in results, "O resultado deve conter o termo consultado"


@pytest.fixture
def memory_manager():
    return MemoryManager()


@pytest.fixture
def llm_handler():
    """LLMHandler real, mas vamos mockar o método interno que chama Groq."""
    handler = LLMHandler()

    # Patch interno para evitar chamadas externas
    handler.generate = MagicMock(return_value="Resposta simulada")
    return handler


@pytest.fixture
def emotion_analyser():
    analyser = EmotionAnalyser()

    # Patch do método que chama o LLM
    analyser.analyse = MagicMock(return_value={"emotion": "neutral"})
    return analyser