import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")

FASTFOREX_API_KEY = os.getenv("FASTFOREX_API_KEY")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"