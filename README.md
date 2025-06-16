# BabAI - AI-Powered WhatsApp Bot for Social Security Information

![babAI-new-version](https://github.com/user-attachments/assets/58548f85-2911-4c74-9891-1aed26163713)


🚀 **Project Overview**

BabAI is a WhatsApp chatbot that provides users with accurate, up-to-date information on social security and pension regulations in Bulgaria. It leverages AI to retrieve information directly from official sources and ensure high-quality, reliable responses. Built with convenience, accuracy, and safety in mind, BabAI empowers users to access critical information anytime, anywhere.

🎯 **Key Features**

- Seamless WhatsApp Integration: Available on a platform familiar to most Bulgarians, with a 90% adoption rate.

- Real-Time Accurate Information: Fetches and presents information from National Social Security Institute documents.

- Guardrails for Safety: Ensures responses are ethical, accurate, and compliant with legal guidelines.


🛠️**Tech Stack**

- Backend: FastAPI (Webhooks), Uvicorn, Ngrok (Reverse Proxy), Twilio API (for WhatsApp integration)

- Database: Pinecone Vector Database

- AI Frameworks: LLama, Together AI, Hugging Face

- DevOps: GitHub Actions for CI/CD, Heruko

- Other Tools: Python (Poetry for dependency management)

🏗**Project Architecture**

1. User Input: Users send questions about pensions or social security via WhatsApp
2. API Gateway: Twilio API captures and forwards user queries to Ngrok reverse proxy 
3. Reverse Proxy: Ngrok forwards payload to BabAI's FastAPI backend
4. Information Retrieval: Backend retrieves accurate, context-specific data from official documents.
5. Response Generation: The AI model generates responses, filtered by guardrails for quality and safety.
6. Output: The user receives a comprehensive, user-friendly answer directly on WhatsApp via webhook.

🚀 **Quick Start**

Prerequisites:
- Python 3.9+ installed
- Twilio Account for WhatsApp API integration
- [Ngrok](https://ngrok.com/docs/getting-started/)
- Together AI API

**Installation**

Clone repository

```
git clone https://github.com/username/babai.git
cd babai
```

Install dependencies:


```
poetry install
```

Set up environment variables:

```
cp .env.example .env

```
Populate .env with your credentials (see the Environment Variables section below).

Run the server locally:
```
uvicorn app.main:app --reload
```

Start ngrok reverse proxy:
```
ngrok http http://localhost:<port-number>
```

Start chatting with BabAI ✨✨



🙌**Team** (alphabetic order)
- Gabriela Tsvetkova
- Miray Özcan
- Saad Asad
- Tetiana Bass
- Hackathon Mentor from Meta

🗣**Acknowledgements**

Thanks to [Hack for Social Impact](https://www.hackforsocialimpact.com/) and all team members who helped make BabAI a reality! Thanks mom for giving us domain expertise on this complex topic 💗
