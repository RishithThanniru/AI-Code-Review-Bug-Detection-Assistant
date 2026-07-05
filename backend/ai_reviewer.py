"""
Day 14 - AI Code Review

Uses an LLM (Groq / Llama 3.3) to produce a holistic review that goes
beyond static analysis: bug detection, code smells, security
observations, performance suggestions and improvement recommendations.

The static findings from bug_detector.py and security_scanner.py are
passed in as context so the model grounds its answer in what was
actually found, rather than hallucinating issues.
"""

import json
import re

from backend import groq_client

MAX_CODE_CHARS = 6000  # keep prompts small & fast for a live demo

SYSTEM_PROMPT = (
    "You are a senior software engineer performing a thorough code review. "
    "Respond ONLY with a single valid JSON object — no markdown fences, no prose "
    "before or after it. The JSON object must have exactly these keys, each a list "
    "of short strings (empty list if none apply): "
    '"bugs", "code_smells", "security_issues", "performance_suggestions", "improvements".'
)


def _build_prompt(filename, language, code, static_bugs, static_security):
    truncated = code[:MAX_CODE_CHARS]
    truncated_note = "\n\n[...truncated for review...]" if len(code) > MAX_CODE_CHARS else ""

    static_context = ""
    if static_bugs:
        static_context += "\nStatic analysis already found these possible bugs:\n" + "\n".join(f"- {b}" for b in static_bugs[:15])
    if static_security:
        static_context += "\nStatic security scan already found:\n" + "\n".join(
            f"- {s['type']} (line {s['line']}): {s['message']}" for s in static_security[:15]
        )

    return f"""Review this {language} file named "{filename}".
{static_context}

Source code:
```{language}
{truncated}{truncated_note}
```

Provide a JSON object with keys: bugs, code_smells, security_issues,
performance_suggestions, improvements. Each value is a list of short,
specific, actionable strings referencing line numbers or function
names where possible."""


def _parse_json_response(text):
    # Strip markdown code fences if the model added them anyway.
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # last resort: try to find the first {...} block
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise
        data = json.loads(match.group(0))

    for key in ("bugs", "code_smells", "security_issues", "performance_suggestions", "improvements"):
        data.setdefault(key, [])

    return data


class AIReviewer:

    def __init__(self, filepath, language="python"):
        self.filepath = filepath
        self.language = language

    def review(self, static_bugs=None, static_security=None):
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()

        filename = self.filepath.split("/")[-1]

        if not groq_client.is_configured():
            return {
                "available": False,
                "message": (
                    "AI-powered review is disabled because GROQ_API_KEY is not "
                    "configured. Static analysis results are still shown in the "
                    "other tabs. Add a free Groq API key to .env to enable this."
                ),
                "bugs": [], "code_smells": [], "security_issues": [],
                "performance_suggestions": [], "improvements": [],
            }

        prompt = _build_prompt(filename, self.language, code, static_bugs or [], static_security or [])

        try:
            raw = groq_client.chat(prompt, system=SYSTEM_PROMPT, temperature=0.2, max_tokens=1500)
            data = _parse_json_response(raw)
            data["available"] = True
            data["message"] = None
            return data
        except Exception as e:
            return {
                "available": False,
                "message": f"AI review request failed: {e}",
                "bugs": [], "code_smells": [], "security_issues": [],
                "performance_suggestions": [], "improvements": [],
            }
