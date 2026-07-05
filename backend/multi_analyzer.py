"""
Lightweight, language-agnostic static analysis used for the languages
that don't have a native Python `ast`-style parser (Java, C, C++,
JavaScript, TypeScript, Go, Rust, Kotlin). It complements the
Tree-sitter structural extraction with pattern-based checks similar in
spirit to backend/analyzer.py's Python checks.
"""

import re


TODO_PATTERN = re.compile(r"//\s*(TODO|FIXME)|#\s*(TODO|FIXME)|/\*\s*(TODO|FIXME)", re.IGNORECASE)
DEBUG_PRINT_PATTERNS = [
    re.compile(r"\bconsole\.log\s*\("),
    re.compile(r"\bSystem\.out\.print(ln)?\s*\("),
    re.compile(r"\bprintf\s*\("),
    re.compile(r"\bfmt\.Println\s*\("),
]
EMPTY_CATCH_PATTERN = re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}")


class MultiLanguageAnalyzer:
    """Runs simple, generic quality checks over any source file."""

    def __init__(self, filepath, language):
        self.filepath = filepath
        self.language = language

    def analyze(self):
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()

        lines = source.splitlines()
        warnings = []

        for lineno, line in enumerate(lines, start=1):
            if TODO_PATTERN.search(line):
                warnings.append(f"Line {lineno}: TODO/FIXME comment left in code")

            for pattern in DEBUG_PRINT_PATTERNS:
                if pattern.search(line):
                    warnings.append(f"Line {lineno}: debug print statement left in code")
                    break

        if EMPTY_CATCH_PATTERN.search(source):
            warnings.append("Empty catch block detected — errors may be silently swallowed")

        # Very long lines hurt readability / code review speed
        for lineno, line in enumerate(lines, start=1):
            if len(line) > 120:
                warnings.append(f"Line {lineno}: line exceeds 120 characters")

        # Overly long file
        if len(lines) > 500:
            warnings.append(f"File is quite long ({len(lines)} lines) — consider splitting into modules")

        return warnings
