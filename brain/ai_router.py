import os
import requests
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
ANTHROPIC_MODEL = os.getenv(
    "ANTHROPIC_MODEL",
    "claude-sonnet-4-5"
)

DEFAULT_PROVIDER = os.getenv(
    "DEFAULT_PROVIDER",
    "openai"
).lower()


def ask_openai(prompt):
    if not OPENAI_API_KEY:
        return "OpenAI API key is not configured."

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": OPENAI_MODEL,
            "input": prompt
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    return data.get("output_text", "No response from OpenAI.")


def ask_gemini(prompt):
    if not GEMINI_API_KEY:
        return "Gemini API key is not configured."

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json"
        },
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    return (
        data["candidates"][0]["content"]["parts"][0]["text"]
    )


def ask_claude(prompt):
    if not ANTHROPIC_API_KEY:
        return "Claude API key is not configured."

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        },
        json={
            "model": ANTHROPIC_MODEL,
            "max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    return data["content"][0]["text"]


def ask_ai(prompt, provider=None):
    provider = (
        provider or DEFAULT_PROVIDER
    ).lower().strip()

    if provider == "openai":
        return ask_openai(prompt)

    if provider == "gemini":
        return ask_gemini(prompt)

    if provider in ("claude", "anthropic"):
        return ask_claude(prompt)

    return f"Unknown AI provider: {provider}"
