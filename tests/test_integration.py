import pytest
import json
from pathlib import Path
from agent.rag import GuideRAG

def test_full_pipeline(material_manager, memory_manager, llm_handler, emotion_analyser, fake_material_path):
    """
    Testa o fluxo completo:
    1. Carrega material
    2. Adiciona ao RAG (via arquivos JSON do usuário)
    3. Guarda informações na memória
    4. Chama LLM e EmotionAnalyser
    """
    user_id = "user123"

    # 1️⃣ Carrega material
    with open(fake_material_path, encoding="utf-8") as f:
        material_data = json.load(f)

    assert "items" in material_data
    texts = [item["conteudo"] for item in material_data["items"]]

    # 2️⃣ Salva material na pasta do usuário para que o GuideRAG consiga ler
    user_folder = Path(f"data/users/{user_id}")
    user_folder.mkdir(parents=True, exist_ok=True)
    vocab_path = user_folder / "Vocabulario.json"
    vocab_path.write_text(json.dumps(material_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 3️⃣ Inicializa o RAG (ele vai ler o arquivo e indexar)
    rag_system = GuideRAG(user_id=user_id, categoria="vocabulario")

    # 4️⃣ Consulta simples
    query = "supermarket"
    results = rag_system.query(query, k=1)
    assert isinstance(results, str)
    assert "supermarket" in results  # valida que o conteúdo foi indexado

    # 5️⃣ Guarda algo na memória
    memory_manager.update_history(user_id, "Como melhorar meu inglês?", "neutral")
    context = memory_manager.get_context(user_id)
    assert any("Como melhorar meu inglês?" in h["message"] for h in context)

    # 6️⃣ LLM responde
    response = llm_handler.generate("Explique este conteúdo")
    assert response == "Resposta simulada"

    # 7️⃣ EmotionAnalyser responde
    emotion = emotion_analyser.analyse("Estou muito feliz")
    assert emotion["emotion"] == "neutral"