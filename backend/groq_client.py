"""
Small shared wrapper around the Groq API used by every AI-powered
feature (AI Review, Refactoring, Chatbot). Centralizing this means the
app degrades gracefully — with a clear message instead of a crash —
when GROQ_API_KEY isn't configured, which matters a lot for a live
placement demo.
"""

import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "llama-3.3-70b-versatile"


class GroqUnavailableError(Exception):
    pass


def is_configured():
    return bool(os.getenv("GROQ_API_KEY"))


def get_client():
    if not is_configured():
        raise GroqUnavailableError(
            "GROQ_API_KEY is not set. Add it to a .env file (see .env.example) "
            "to enable AI-powered features. Get a free key at https://console.groq.com/keys"
        )

    from groq import Groq
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def chat(prompt, system=None, model=DEFAULT_MODEL, temperature=0.3, max_tokens=1500):
    """Send a single-turn prompt to Groq and return the text response.
    Raises GroqUnavailableError if no API key is configured, and
    re-raises any API error so callers can show it to the user.
    """

    client = get_client()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content
