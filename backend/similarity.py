"""
Day 18 - Code Similarity Checker

Compares two source files and reports:
    * Overall similarity percentage (sequence-based, whitespace/blank
      lines/comments ignored so formatting differences don't skew results)
    * Matching / differing line blocks
    * Overlap between function and class names (using the same
      parser used for the Dashboard tab, so it works for every
      supported language)
"""

import difflib
import re


COMMENT_PATTERNS = [
    re.compile(r"#.*$"),
    re.compile(r"//.*$"),
]


def _normalize_lines(source):
    """Strip comments/blank lines so similarity reflects logic, not
    formatting or comment differences."""
    normalized = []
    for line in source.splitlines():
        stripped = line.strip()
        for pattern in COMMENT_PATTERNS:
            stripped = pattern.sub("", stripped).strip()
        if stripped:
            normalized.append(stripped)
    return normalized


class SimilarityChecker:

    def __init__(self, filepath_a, filepath_b):
        self.filepath_a = filepath_a
        self.filepath_b = filepath_b

    def compare(self):
        with open(self.filepath_a, "r", encoding="utf-8", errors="ignore") as f:
            source_a = f.read()
        with open(self.filepath_b, "r", encoding="utf-8", errors="ignore") as f:
            source_b = f.read()

        lines_a = _normalize_lines(source_a)
        lines_b = _normalize_lines(source_b)

        matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
        similarity_ratio = matcher.ratio() * 100

        matching_blocks = []
        for block in matcher.get_matching_blocks():
            if block.size >= 3:
                matching_blocks.append({
                    "a_start": block.a + 1,
                    "b_start": block.b + 1,
                    "size": block.size,
                    "lines": lines_a[block.a: block.a + block.size],
                })

        diff = list(difflib.unified_diff(
            lines_a, lines_b,
            fromfile=self.filepath_a, tofile=self.filepath_b,
            lineterm="",
        ))

        return {
            "similarity_percent": round(similarity_ratio, 2),
            "matching_blocks": matching_blocks,
            "diff": diff,
            "lines_a": len(lines_a),
            "lines_b": len(lines_b),
        }

    @staticmethod
    def compare_structures(parsed_a, parsed_b):
        """Compare extracted function/class names between two parsed
        results (as returned by CodeParser/TreeParser)."""

        funcs_a, funcs_b = set(parsed_a.get("functions", [])), set(parsed_b.get("functions", []))
        classes_a, classes_b = set(parsed_a.get("classes", [])), set(parsed_b.get("classes", []))

        return {
            "shared_functions": sorted(funcs_a & funcs_b),
            "shared_classes": sorted(classes_a & classes_b),
            "unique_to_a_functions": sorted(funcs_a - funcs_b),
            "unique_to_b_functions": sorted(funcs_b - funcs_a),
        }

    @staticmethod
    def verdict(similarity_percent):
        if similarity_percent >= 85:
            return "🔴 Very High — likely duplicate or copy-pasted code"
        if similarity_percent >= 60:
            return "🟠 High — significant shared logic, review recommended"
        if similarity_percent >= 30:
            return "🟡 Moderate — some structural overlap"
        return "🟢 Low — files are largely independent"
