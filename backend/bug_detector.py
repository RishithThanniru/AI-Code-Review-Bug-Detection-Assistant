"""
Day 15 - AI Bug Detection

Detects common programming bugs:
    * Infinite loops (while True / while(1) with no visible break)
    * Division by zero (literal divisor of 0)
    * Dead code (unreachable statements after return/break/continue/raise)
    * Duplicate code (near-identical function/block bodies)
    * Unused variables

Python files get precise, AST-based detection. Other languages fall
back to conservative regex/heuristic detection so the feature works
across every supported language, with results always clearly labeled.
"""

import ast
import hashlib
import re


class BugDetector:

    def __init__(self, filepath, language="python"):
        self.filepath = filepath
        self.language = language

    def detect(self):
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()

        if self.language == "python":
            return self._detect_python(source)
        return self._detect_generic(source)

    # ------------------------------------------------------------------
    # Python: precise AST-based detection
    # ------------------------------------------------------------------

    def _detect_python(self, source):
        bugs = []

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return [f"Syntax error — file could not be parsed: {e}"]

        bugs += self._infinite_loops_py(tree)
        bugs += self._division_by_zero_py(tree)
        bugs += self._dead_code_py(tree)
        bugs += self._duplicate_functions_py(tree)
        bugs += self._unused_variables_py(tree)

        return bugs

    @staticmethod
    def _infinite_loops_py(tree):
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                is_always_true = (
                    isinstance(node.test, ast.Constant) and node.test.value is True
                ) or (
                    isinstance(node.test, ast.Num) and getattr(node.test, "n", None) == 1
                )
                if is_always_true:
                    has_break = any(isinstance(n, ast.Break) for n in ast.walk(node))
                    if not has_break:
                        found.append(
                            f"Line {node.lineno}: possible infinite loop "
                            f"('while True' with no 'break' statement)"
                        )
        return found

    @staticmethod
    def _division_by_zero_py(tree):
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                divisor = node.right
                if isinstance(divisor, ast.Constant) and divisor.value == 0:
                    found.append(f"Line {node.lineno}: division by zero (literal 0 divisor)")
        return found

    @staticmethod
    def _dead_code_py(tree):
        found = []
        terminators = (ast.Return, ast.Break, ast.Continue, ast.Raise)

        def check_body(body):
            for i, stmt in enumerate(body):
                if isinstance(stmt, terminators) and i < len(body) - 1:
                    next_stmt = body[i + 1]
                    found.append(
                        f"Line {next_stmt.lineno}: unreachable code after "
                        f"'{type(stmt).__name__.lower()}' statement"
                    )

        for node in ast.walk(tree):
            if hasattr(node, "body") and isinstance(node.body, list):
                check_body(node.body)

        return found

    @staticmethod
    def _duplicate_functions_py(tree):
        found = []
        seen = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                try:
                    body_dump = ast.dump(ast.Module(body=node.body, type_ignores=[]))
                except TypeError:
                    body_dump = ast.dump(node)
                digest = hashlib.md5(body_dump.encode()).hexdigest()

                if digest in seen and len(node.body) > 1:
                    found.append(
                        f"Function '{node.name}' (line {node.lineno}) looks like "
                        f"duplicate logic of '{seen[digest]}'"
                    )
                else:
                    seen[digest] = node.name

        return found

    @staticmethod
    def _unused_variables_py(tree):
        found = []

        for func in ast.walk(tree):
            if not isinstance(func, ast.FunctionDef):
                continue

            assigned = {}
            used = set()

            for node in ast.walk(func):
                if isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Store):
                        assigned.setdefault(node.id, node.lineno)
                    elif isinstance(node.ctx, ast.Load):
                        used.add(node.id)

            for name, lineno in assigned.items():
                if name in used:
                    continue
                if name.startswith("_"):
                    continue
                found.append(
                    f"Line {lineno}: variable '{name}' assigned in '{func.name}' but never used"
                )

        return found

    # ------------------------------------------------------------------
    # Generic (non-Python) heuristic detection
    # ------------------------------------------------------------------

    def _detect_generic(self, source):
        bugs = []
        lines = source.splitlines()

        infinite_pattern = re.compile(r"while\s*\(\s*(true|1)\s*\)", re.IGNORECASE)
        break_pattern = re.compile(r"\bbreak\b")
        div_zero_pattern = re.compile(r"[^/\s]\s*/\s*0(?!\d)")

        for i, line in enumerate(lines, start=1):
            if infinite_pattern.search(line):
                window = "\n".join(lines[i - 1:i + 20])
                if not break_pattern.search(window):
                    bugs.append(f"Line {i}: possible infinite loop with no visible 'break'")

            if div_zero_pattern.search(line):
                bugs.append(f"Line {i}: possible division by zero (literal 0 divisor)")

        bugs += self._dead_code_generic(lines)
        bugs += self._duplicate_blocks_generic(lines)

        return bugs

    @staticmethod
    def _dead_code_generic(lines):
        found = []
        terminator_pattern = re.compile(r"^\s*(return\b|break\s*;|continue\s*;|throw\b)")

        for i in range(len(lines) - 1):
            if terminator_pattern.match(lines[i]):
                next_line = lines[i + 1].strip()
                if next_line and next_line not in ("}", "") and not next_line.startswith(("}", "//", "/*", "*")):
                    found.append(f"Line {i + 2}: unreachable code after a return/break/throw statement")

        return found

    @staticmethod
    def _duplicate_blocks_generic(lines, block_size=5):
        found = []
        seen = {}
        stripped = [l.strip() for l in lines]

        for i in range(len(stripped) - block_size + 1):
            block = tuple(stripped[i:i + block_size])
            if all(len(l) == 0 for l in block):
                continue
            digest = hashlib.md5("\n".join(block).encode()).hexdigest()

            if digest in seen and (i - seen[digest]) >= block_size:
                found.append(
                    f"Lines {i + 1}-{i + block_size}: duplicate of lines "
                    f"{seen[digest] + 1}-{seen[digest] + block_size}"
                )
            else:
                seen[digest] = i

        return found
