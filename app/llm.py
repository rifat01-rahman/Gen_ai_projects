import requests
from config import HF_API_KEY, MODEL

API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query_llm(prompt):

    payload = {
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    return response.json()[0]["generated_text"]