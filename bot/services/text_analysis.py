import requests
import json
from config import Config


async def analyze_text(text: str) -> str:
    url = "https://open-ai21.p.rapidapi.com/conversationllama"

    headers = {
        "x-rapidapi-key": Config.RAPIDAPI_KEY,
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"""
                        Проанализируйте текст и ответьте на русском языке. Включите следующие поля:
                        1. эмоции: эмоции, которые передаёт текст (радость, грусть, гнев, удивление и т.д.), в процентах.
                        2. бизнес-анализ: бизнес-анализ текста, включая:
                           - убедительность: убедительность текста (в процентах).
                           - целевая аудитория: целевая аудитория текста.
                           - рекомендации: рекомендации по улучшению текста.

                        Текст для анализа: "{text}"
                    """
            }
        ],
        "web_access": False
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['result']
    except Exception as e:
        return f"Ошибка анализа: {str(e)}"
