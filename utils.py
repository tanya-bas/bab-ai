"""Utils for sending messages through Twilio API"""

import logging
from twilio.rest import Client
import os
from dotenv import load_dotenv


load_dotenv()

# env variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twillio_number = os.getenv("TWILIO_NUMBER")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Twilio Messaging API initialized")
logger.info(f"Twilio number: {twillio_number}")


# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twillio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}",
        )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")
