# LLM/client.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Make it find the .env file in backend folder
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)


#Create a single OpenAI client using the API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")  # switch via env only

