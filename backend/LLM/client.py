# LLM/client.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#Create a single OpenAI client using the API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")  # switch via env only

