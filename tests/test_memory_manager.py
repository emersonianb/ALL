import pytest
from agent.memory import MemoryManager

@pytest.fixture
def memory_manager(tmp_path):
    # Cria MemoryManager com arquivo temporário
    return MemoryManager(path=tmp_path / "memory.json")

@pytest.fixture
def user_id():
    return "user123"

def test_memory_add_and_retrieve(memory_manager, user_id):
    # Adiciona dados simulando "store"
    memory_manager.update_learning_state(user_id, nivel="A1")
    
    # Recupera dados simulando "retrieve"
    state = memory_manager.get_learning_state(user_id)
    
    assert state["nivel"] == "A1"

def test_memory_update(memory_manager, user_id):
    # Adiciona e atualiza dados
    memory_manager.update_learning_state(user_id, nivel="A1")
    memory_manager.update_learning_state(user_id, nivel="B1")
    
    state = memory_manager.get_learning_state(user_id)
    assert state["nivel"] == "B1"