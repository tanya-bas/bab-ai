import pytest
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_app.llm_utils import (
    call_together,
    get_ambiguity_detection_response,
    get_tool_use,
    rephrase_query,
    check_response_appropriateness,
    search_pinecone,
    generate_response,
    scrape_website_content,
    get_pension_numbers
)

# Mock responses
MOCK_LLM_RESPONSE = '{"result": true, "feedback": "Test feedback"}'
MOCK_WEBSITE_CONTENT = "Test heading\nTest paragraph"

@pytest.fixture
def mock_together_response():
    class MockDelta:
        content = "test"
    
    class MockChoice:
        delta = MockDelta()
    
    class MockResponse:
        choices = [MockChoice()]
    
    return MockResponse()

@pytest.fixture
def mock_requests_response():
    mock = Mock()
    mock.status_code = 200
    mock.content = "<html><body><h1>Test heading</h1><p>Test paragraph</p></body></html>"
    return mock

# Test call_together
@patch('llm_app.llm_utils.client')
def test_call_together(mock_client, mock_together_response):
    mock_client.chat.completions.create.return_value = [mock_together_response]
    
    result = call_together("system prompt", "user prompt")
    assert result == "test"
    mock_client.chat.completions.create.assert_called_once()

# Test get_ambiguity_detection_response
@patch('llm_app.llm_utils.call_together')
def test_get_ambiguity_detection_response(mock_call):
    mock_call.return_value = MOCK_LLM_RESPONSE
    
    result = get_ambiguity_detection_response("test query")
    assert isinstance(result, dict)
    assert "result" in result
    assert "feedback" in result

# Test get_tool_use
@patch('llm_app.llm_utils.call_together')
def test_get_tool_use(mock_call):
    mock_call.return_value = MOCK_LLM_RESPONSE
    
    result = get_tool_use("test query")
    assert isinstance(result, dict)

# Test rephrase_query
@patch('llm_app.llm_utils.call_together')
def test_rephrase_query(mock_call):
    mock_call.return_value = "rephrased query"
    
    result = rephrase_query("test query", "test context")
    assert isinstance(result, str)

# Test check_response_appropriateness
@patch('llm_app.llm_utils.call_together')
def test_check_response_appropriateness(mock_call):
    mock_call.return_value = MOCK_LLM_RESPONSE
    
    result, feedback = check_response_appropriateness("test query", "test responses")
    assert isinstance(result, bool)
    assert isinstance(feedback, str)

# Test search_pinecone
@patch('llm_app.llm_utils.query_pinecone_index')
@patch('llm_app.llm_utils.rephrase_query')
def test_search_pinecone(mock_rephrase, mock_pinecone):
    mock_rephrase.return_value = "rephrased query"
    mock_pinecone.return_value = ["result1", "result2"]
    
    query_fixed, results = search_pinecone("test query")
    assert query_fixed == "rephrased query"
    assert isinstance(results, list)

# Test generate_response
@patch('llm_app.llm_utils.call_together')
def test_generate_response(mock_call):
    mock_call.return_value = "generated response"
    
    result = generate_response("test query", ["source1", "source2"])
    assert isinstance(result, str)

# Test scrape_website_content
@patch('llm_app.llm_utils.requests.get')
def test_scrape_website_content(mock_get, mock_requests_response):
    mock_get.return_value = mock_requests_response
    
    result = scrape_website_content()
    assert isinstance(result, str)
    assert "Test heading" in result
    assert "Test paragraph" in result

# Test scrape_website_content failure
@patch('llm_app.llm_utils.requests.get')
def test_scrape_website_content_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    result = scrape_website_content()
    assert "Failed to retrieve" in result

# Test get_pension_numbers
@patch('llm_app.llm_utils.call_together')
@patch('llm_app.llm_utils.scrape_website_content')
def test_get_pension_numbers(mock_scrape, mock_call):
    mock_scrape.return_value = MOCK_WEBSITE_CONTENT
    mock_call.return_value = "pension calculation result"
    
    result = get_pension_numbers("test query")
    assert isinstance(result, str)