from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import dotenv
# Load environment variables from .env file
dotenv.load_dotenv()


# ---------------------------
# Setup and Configuration
# ---------------------------
app = FastAPI()

# Allow CORS from your Laravel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---------------------------
# Request & Response Models
# ---------------------------
class PromptRequest(BaseModel):
    query: str

class CompletionResponse(BaseModel):
    result: str

# ---------------------------
# Routes
# ---------------------------
@app.post("/generate", response_model=CompletionResponse)
def generate_response(req: PromptRequest):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": req.query}
            ]
        )
        reply = completion.choices[0].message.content.strip()
        return {"result": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/getans", response_model=CompletionResponse)
def get_ans():
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Create a mindmap in form of Json for world war 2"}
            ]
        )
        reply = completion.choices[0].message.content.strip()
        return {"result": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))