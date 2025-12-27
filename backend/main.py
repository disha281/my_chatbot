from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request body
class ChatRequest(BaseModel):
    message: str

# 🧠 Conversation Memory
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

MAX_MESSAGES = 10  # keep last 10 exchanges

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Add user message
        conversation_history.append({
            "role": "user",
            "content": request.message
        })

        # Trim memory
        if len(conversation_history) > MAX_MESSAGES * 2:
            conversation_history[:] = (
                conversation_history[:1] +
                conversation_history[-MAX_MESSAGES * 2:]
            )

        # OpenAI call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )

        reply = response.choices[0].message.content

        # Add assistant reply
        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}

@app.post("/reset")
def reset_chat():
    conversation_history.clear()
    conversation_history.append({
        "role": "system",
        "content": "You are a helpful assistant."
    })
    return {"message": "Conversation reset"}

@app.get("/")
def home():
    return {"message": "Chatbot backend running 🚀"}
