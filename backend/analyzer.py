import ast


class CodeAnalyzer:
    """Static-analysis style checks for Python source using `ast`."""

    def __init__(self, filepath):
        self.filepath = filepath

    def analyze(self):

        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as file:
            source = file.read()

        tree = ast.parse(source)

        warnings = []

        # ---------- Unused Imports ----------
        imported = []
        used = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for name in node.names:
                    imported.append(name.asname or name.name.split(".")[0])

            elif isinstance(node, ast.ImportFrom):
                for name in node.names:
                    imported.append(name.asname or name.name)

            elif isinstance(node, ast.Name):
                used.append(node.id)

            elif isinstance(node, ast.Attribute):
                # covers usages like `module.func()` where only the
                # attribute access shows up, not a bare Name node
                pass

        for module in imported:
            if module not in used and module not in source:
                warnings.append(f"Unused import: {module}")

        # ---------- Dangerous Functions ----------
        for node in ast.walk(tree):

            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    if node.func.id in ("eval", "exec"):
                        warnings.append(
                            f"Dangerous function used: {node.func.id}()"
                        )

        # ---------- Missing Docstrings ----------
        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                if ast.get_docstring(node) is None:
                    warnings.append(
                        f"Missing docstring in function '{node.name}'"
                    )

        # ---------- Long Functions ----------
        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                if len(node.body) > 15:
                    warnings.append(
                        f"Function '{node.name}' is too long ({len(node.body)} statements)"
                    )

        return warnings
