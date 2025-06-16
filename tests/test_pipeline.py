import pytest
from pipeline import runner

# Mock the imported functions to control their behavior
@pytest.fixture
def mock_functions(mocker):
    mock_ambiguity = mocker.patch('pipeline.get_ambiguity_detection_response')
    mock_tool_use = mocker.patch('pipeline.get_tool_use')
    mock_search = mocker.patch('pipeline.search_pinecone')
    mock_generate = mocker.patch('pipeline.generate_response')
    mock_check = mocker.patch('pipeline.check_response_appropriateness')
    mock_pension = mocker.patch('pipeline.get_pension_numbers')
    
    mock_ambiguity.return_value = {'is_ambiguous': False, 'needs_clarification': False}
    mock_tool_use.return_value = {'is_irrelevant': False, 'needs_calculation': False}
    mock_search.return_value = [{'text': 'test response'}]
    mock_generate.return_value = 'generated response'
    mock_check.return_value = True
    mock_pension.return_value = {'monthly_pension': 1000}
    
    return {
        'ambiguity': mock_ambiguity,
        'tool_use': mock_tool_use,
        'search': mock_search,
        'generate': mock_generate,
        'check': mock_check,
        'pension': mock_pension
    }

def test_irrelevant_question(mock_functions):
    mock_functions['ambiguity'].return_value = {'question_irrelevant': 'yes'}
    
    response, info = runner("What's the weather like?")
    assert response == "Нерелевантен въпрос"
    assert info is None

def test_needs_clarification(mock_functions):
    mock_functions['ambiguity'].return_value = {
        'question_irrelevant': 'no',
        'clarification_needed': 'yes',
        'clarification': 'Could you please specify your age?'
    }
    
    response, info = runner("Tell me about pension")
    assert response == "Could you please specify your age?"
    assert info is None

def test_pension_calculation(mock_functions):
    mock_functions['ambiguity'].return_value = {
        'question_irrelevant': 'no',
        'clarification_needed': 'no'
    }
    mock_functions['tool_use'].return_value = {'needs_pension_calculation': 'yes'}
    mock_functions['pension'].return_value = "Your estimated pension is 500 BGN"
    
    response, info = runner("Calculate my pension if I'm 65 years old")
    assert response == "Your estimated pension is 500 BGN"
    assert info is None

def test_pension_guidance_success(mock_functions):
    # Setup mocks
    mock_functions['ambiguity'].return_value = {
        'question_irrelevant': 'no',
        'clarification_needed': 'no'
    }
    mock_functions['tool_use'].return_value = {'needs_pension_guidance': 'yes'}
    mock_functions['search'].return_value = (["relevant search result"], "rephrased query")
    mock_functions['generate'].return_value = "Here's how to apply for pension"
    mock_functions['check'].return_value = ("yes", None)
    
    response, info = runner("How do I apply for pension?")
    assert response == "Here's how to apply for pension"
    assert info is not None

def test_pension_guidance_failure(mock_functions):
    # Setup mocks for failed attempts
    mock_functions['ambiguity'].return_value = {
        'question_irrelevant': 'no',
        'clarification_needed': 'no'
    }
    mock_functions['tool_use'].return_value = {'needs_pension_guidance': 'yes'}
    mock_functions['search'].return_value = (["search result"], "rephrased query")
    mock_functions['generate'].return_value = "Generated response"
    mock_functions['check'].return_value = ("no", "Inappropriate response")
    
    response, info = runner("How do I apply for pension?")
    assert response == "Неуспешно генериране на отговор"
    assert info is not None

def test_no_available_answer(mock_functions):
    mock_functions['ambiguity'].return_value = {
        'question_irrelevant': 'no',
        'clarification_needed': 'no'
    }
    mock_functions['tool_use'].return_value = {
        'needs_pension_guidance': 'no',
        'needs_pension_calculation': 'no'
    }
    
    response, info = runner("Some unrelated question")
    assert response == "Няма наличен отговор"
    assert info is None

def test_previous_queries_tracking(mock_functions):
    # Setup mocks
    mock_functions['ambiguity'].return_value = {
        'question_irrelevant': 'no',
        'clarification_needed': 'no'
    }
    mock_functions['tool_use'].return_value = {'needs_pension_guidance': 'yes'}
    mock_functions['search'].return_value = (["search result"], "rephrased query")
    mock_functions['generate'].return_value = "Generated response"
    mock_functions['check'].return_value = ("yes", None)
    
    previous_queries = [
        {
            "original_query": "old query",
            "rephrased_query": "old rephrased query",
            "response": "old response"
        }
    ]
    
    response, info = runner("New query", previous_queries=previous_queries)
    assert len(previous_queries) == 2
    assert previous_queries[0]["original_query"] == "old query"
    assert previous_queries[1]["original_query"] == "New query"