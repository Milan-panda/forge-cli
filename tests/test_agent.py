import pytest
from unittest.mock import MagicMock, patch
from forge.agent import ForgeAgent

@pytest.fixture
def mock_openai():
    with patch("forge.agent.OpenAI") as mock:
        yield mock

def test_agent_run_stream(mock_openai):
    # Mock response chunks
    mock_chunk1 = MagicMock()
    mock_chunk1.choices[0].delta.content = "Hello"
    mock_chunk1.choices[0].delta.tool_calls = None
    
    mock_chunk2 = MagicMock()
    mock_chunk2.choices[0].delta.content = " World"
    mock_chunk2.choices[0].delta.tool_calls = None
    
    # Mock client.chat.completions.create return value (iterable)
    mock_client_instance = mock_openai.return_value
    mock_client_instance.chat.completions.create.return_value = [mock_chunk1, mock_chunk2]
    
    with patch("forge.agent.load_config") as mock_config:
        mock_config.return_value = {"api_key": "fake", "model": "fake"}
        agent = ForgeAgent()
    
    output = list(agent.run("Hi"))
    
    assert ("content", "Hello") in output
    assert ("content", " World") in output
    assert agent.messages[-1]["content"] == "Hello World"
