import pytest
import json
from pathlib import Path
from agent.rag import GuideRAG

@pytest.fixture
def fake_material_path(tmp_path):
    path = tmp_path / "Vocabulario.json"
    material = {
        "items": [
            {"tema": "Compras", "conteudo": "I went to the supermarket yesterday."},
            {"tema": "Frutas", "conteudo": "I bought apples and bananas."}
        ]
    }
    path.write_text(json.dumps(material, indent=2), encoding="utf-8")
    return path

@pytest.fixture
def rag_system(fake_material_path, tmp_path):
    # cria pasta do usuário e copia o material
    user_folder = tmp_path / "user123"
    user_folder.mkdir()
    dest_path = user_folder / "Vocabulario.json"
    dest_path.write_text(fake_material_path.read_text(), encoding="utf-8")

    return GuideRAG(user_id="user123", categoria="vocabulario")

def test_rag_index_and_query(rag_system):
    """
    Testa se o GuideRAG consegue indexar o material e recuperar conteúdo relevante.
    """
    query = "supermarket"
    results = rag_system.query(query, k=1)

    # valida a saída (como string)
    assert isinstance(results, str), "O retorno da consulta deve ser uma string"
    assert "supermarket" in results, "O resultado deve conter o termo consultado"