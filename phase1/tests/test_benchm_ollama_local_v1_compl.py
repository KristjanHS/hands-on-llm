#
import pytest
from unittest.mock import patch, MagicMock

# This import assumes that pytest is run from the project root directory
# (e.g., /home/kristjans/projects/hands-on-llm)
from phase1.python_code.benchm_ollama_local_v1_compl import call_ollama_api


@patch("phase1.python_code.benchm_ollama_local_v1_compl.requests.post")
def test_call_ollama_api(mock_post):
    """
    Tests that call_ollama_api constructs the correct URL and payload for a
    request, calls the API, and correctly returns the parsed JSON from the response.
    This is the most critical function to test as it handles the core logic of
    communicating with the Ollama API.
    """
    # Arrange: Set up the mock for requests.post
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    expected_json = {
        "model": "mistral",
        "response": "The capital of France is Paris.",
        "done": True,
        "usage": {"prompt_tokens": 10, "completion_tokens": 20},
    }
    mock_response.json.return_value = expected_json
    mock_post.return_value = mock_response

    # Define test inputs
    host = "172.22.208.1"
    port = 11434
    model = "mistral"
    prompt = (
        """What is the capital of France? Answer like this: "The capital of France is [city]."""
    )
    temperature = 0
    num_predict = 128
    num_ctx = 2048

    # Define expected values for the call
    expected_url = f"http://{host}:{port}/v1/completions"
    expected_payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": num_predict,
        "context_window": num_ctx,
    }

    # Act: Call the function under test
    result = call_ollama_api(host, port, model, prompt, temperature, num_predict, num_ctx)

    # Assert: Verify the behavior
    mock_post.assert_called_once_with(url=expected_url, json=expected_payload)
    assert result == expected_json
