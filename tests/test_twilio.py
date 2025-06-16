import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import send_message, twillio_number
from dotenv import load_dotenv

load_dotenv()

to_number = os.getenv("TWILIO_NUMBER")


@pytest.fixture
def mock_twilio_client():
    # Mock the Client at module level where it's created
    with patch('utils.client') as mock_client:
        mock_message = MagicMock()
        mock_message.body = "Test message"
        mock_client.messages.create.return_value = mock_message
        yield mock_client

def test_send_message_success(mock_twilio_client, caplog):
    # Test data
    body_text = "Hello, test!"
    
    # Call function
    send_message(to_number, body_text)

    # Verify message creation was called with correct parameters
    mock_twilio_client.messages.create.assert_called_once_with(
        from_=f"whatsapp:{twillio_number}",
        body=body_text,
        to=f"whatsapp:{to_number}"
    )

def test_send_message_failure(mock_twilio_client, caplog):
    # Configure mock to raise an exception
    mock_twilio_client.messages.create.side_effect = Exception("Test error")
    
    # Test data
    to_number = "+1234567890"
    body_text = "Hello, test!"

    # Call function
    send_message(to_number, body_text)

    # Verify error logging
    assert "Error sending message to +1234567890: Test error" in caplog.text
