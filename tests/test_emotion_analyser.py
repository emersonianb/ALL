def test_emotion_detection(emotion_analyser):
    result = emotion_analyser.analyse("Estou muito triste hoje")
    assert isinstance(result, dict)
    assert "emotion" in result