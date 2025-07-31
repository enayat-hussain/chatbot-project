import requests
from config import HEADERS, API_URL, get_payload

def chat_with_groq(prompt):
    try:
        payload = get_payload(prompt)
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Groq API: {str(e)}"
