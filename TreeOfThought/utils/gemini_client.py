# utils/gemini_client.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_answer(prompt: str) -> str:
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.7}
        )
        return response.text.strip()
    except Exception as e:
        return f"[ERROR] {str(e)}"
