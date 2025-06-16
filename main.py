from fastapi import FastAPI, Form
from utils import send_message

import os
from dotenv import load_dotenv
from pipeline import runner
from logging import getLogger


load_dotenv()
app = FastAPI()
whatsapp_number = os.getenv("CLIENT_NUMBER")
logger = getLogger(__name__)
logger.info(f"Phone number: {whatsapp_number}")


@app.get("/status")
async def index():
    return {"msg": "up & running"}


@app.post("/message")
async def reply(Body: str = Form()) -> str:
    """
    Endpoint to handle incoming messages, process them using the runner function,
    and send a response back via WhatsApp.
    """
    # Process the incoming message using runner
    response = runner(Body)

    # Send the response using Twilio
    logger.info(f"Phone number: {whatsapp_number}")
    send_message(whatsapp_number, response)
    return response
