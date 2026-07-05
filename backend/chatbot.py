"""
Q&A chatbot for the uploaded source file.

The original version of this project used a FAISS vector store with
HuggingFace sentence-transformer embeddings for retrieval-augmented
generation. That pulled in a very heavy dependency chain (torch +
transformers) and needed to download a model the first time it ran,
which made the app slow to start and fragile in an offline/restricted
network — a real risk during a live placement demo.

Since a single source file comfortably fits in an LLM's context
window, this version sends the (truncated) file directly as context
instead of chunking + embedding it. Functionally this is still
context-grounded Q&A about the code, just without the extra
infrastructure and failure points.
"""

from backend import groq_client

MAX_CODE_CHARS = 8000

SYSTEM_PROMPT = (
    "You are an expert code review assistant. Answer the user's question "
    "using ONLY the provided source code as context. If the answer isn't "
    "in the code, say so clearly instead of guessing."
)


class CodeChatBot:

    def __init__(self, filepath, language="python"):
        self.filepath = filepath
        self.language = language

    def ask(self, question):
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()

        truncated = code[:MAX_CODE_CHARS]
        truncated_note = "\n\n[...truncated...]" if len(code) > MAX_CODE_CHARS else ""

        prompt = f"""Source code ({self.language}):
```{self.language}
{truncated}{truncated_note}
```

Question: {question}

Give a clear, detailed answer."""

        return groq_client.chat(prompt, system=SYSTEM_PROMPT, temperature=0.3, max_tokens=1200)
