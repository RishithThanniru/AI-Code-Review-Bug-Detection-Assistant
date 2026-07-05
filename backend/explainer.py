"""
Local, dependency-free code summary generator. Works off the
structural counts already produced by CodeParser/TreeParser, so it
needs no network access and works identically for every supported
language. This is shown even when the AI Review tab (Day 14, which
needs a Groq API key) isn't configured.
"""


class CodeExplainer:

    def __init__(self, parsed_result, language="python"):
        self.parsed_result = parsed_result
        self.language = language

    def explain(self):
        functions = len(self.parsed_result.get("functions", []))
        classes = len(self.parsed_result.get("classes", []))
        imports = len(self.parsed_result.get("imports", []))
        loops = self.parsed_result.get("loops", 0)
        conditions = self.parsed_result.get("conditions", 0)

        suggestions = []

        if loops > 2:
            suggestions.append("Consider reducing nested loops to improve performance.")

        if functions > 10:
            suggestions.append("Consider splitting the file into multiple modules.")

        if imports > 10:
            suggestions.append("Review imports for unused ones to keep the file clean.")

        if classes == 0 and functions > 5:
            suggestions.append("Consider grouping related functions into classes if it improves organization.")

        if not suggestions:
            suggestions.append("The overall code structure looks clean and organized.")

        explanation = f"""### 📄 Code Summary

This {self.language.capitalize()} file contains:

- {functions} function(s)
- {classes} class(es)
- {imports} import statement(s)
- {loops} loop(s)
- {conditions} conditional statement(s)

### 💡 Suggestions
"""
        for suggestion in suggestions:
            explanation += f"\n- {suggestion}"

        return explanation
