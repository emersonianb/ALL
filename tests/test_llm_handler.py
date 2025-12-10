def test_llm_handler_response(llm_handler):
    response = llm_handler.generate("contexto", "Olá")

    assert isinstance(response, str)
    assert len(response) > 0