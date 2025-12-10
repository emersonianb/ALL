import pytest
import json
from pathlib import Path
from agent.material_manager import MaterialManager, MaterialFormatter

@pytest.fixture
def material_manager(tmp_path):
    # Cria um MaterialManager com pasta temporária e formatter fake
    class FakeFormatter:
        def format(self, text):
            return {"tema": "Teste", "conteudo": text}

    return MaterialManager(base_folder=tmp_path, formatter=FakeFormatter())

@pytest.fixture
def user_id():
    return "user123"

def test_material_addition(material_manager, user_id):
    # Adiciona material
    file_path = material_manager.add_material(user_id, "conversacao", "Conteúdo de teste")

    # Verifica se o arquivo foi criado
    assert file_path.exists()

    # Lê o arquivo e confere se o material está lá
    data = json.loads(file_path.read_text(encoding="utf-8"))
    assert len(data["items"]) == 1
    assert data["items"][0]["tema"] == "Teste"
    assert data["items"][0]["conteudo"] == "Conteúdo de teste"

def test_material_formatting(material_manager, user_id):
    # Adiciona material com texto que será "formatado"
    material_manager.add_material(user_id, "gramatica", "Outro conteúdo")

    file_path = material_manager.get_user_folder(user_id) / "Gramatica.json"
    data = json.loads(file_path.read_text(encoding="utf-8"))

    assert len(data["items"]) == 1
    assert data["items"][0]["tema"] == "Teste"
    assert data["items"][0]["conteudo"] == "Outro conteúdo"