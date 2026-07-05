"""
Day 17 - AI Refactoring

Generates AI-suggested refactorings that improve readability,
maintainability and performance without changing behavior. Returns
both the refactored code and a plain-language explanation of what
changed and why.
"""

import re

from backend import groq_client

MAX_CODE_CHARS = 6000

SYSTEM_PROMPT = (
    "You are a senior software engineer specializing in refactoring. "
    "Improve the given code's readability, maintainability and performance "
    "WITHOUT changing its external behavior. "
    'Respond with exactly two sections in this format, nothing else: '
    "a fenced code block with the refactored code, followed by a section "
    "titled 'Explanation:' listing the key changes as short bullet points."
)


class CodeRefactorer:

    def __init__(self, filepath, language="python"):
        self.filepath = filepath
        self.language = language

    def refactor(self):
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()

        if not groq_client.is_configured():
            return {
                "available": False,
                "message": (
                    "AI refactoring is disabled because GROQ_API_KEY is not "
                    "configured. Add a free Groq API key to .env to enable this."
                ),
                "refactored_code": None,
                "explanation": None,
            }

        truncated = code[:MAX_CODE_CHARS]
        truncated_note = "\n\n[...truncated...]" if len(code) > MAX_CODE_CHARS else ""

        prompt = f"""Refactor this {self.language} code for readability,
maintainability and performance, keeping behavior identical:

```{self.language}
{truncated}{truncated_note}
```"""

        try:
            raw = groq_client.chat(prompt, system=SYSTEM_PROMPT, temperature=0.2, max_tokens=2000)
            refactored_code, explanation = self._split_response(raw)
            return {
                "available": True,
                "message": None,
                "refactored_code": refactored_code,
                "explanation": explanation,
            }
        except Exception as e:
            return {
                "available": False,
                "message": f"AI refactoring request failed: {e}",
                "refactored_code": None,
                "explanation": None,
            }

    @staticmethod
    def _split_response(raw):
        code_match = re.search(r"```(?:\w+)?\n(.*?)```", raw, re.DOTALL)
        refactored_code = code_match.group(1).strip() if code_match else raw.strip()

        explanation_match = re.search(r"Explanation:(.*)", raw, re.DOTALL | re.IGNORECASE)
        explanation = explanation_match.group(1).strip() if explanation_match else (
            "No structured explanation was returned by the model."
        )

        return refactored_code, explanation
