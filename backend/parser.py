import ast


class CodeParser:
    """Extracts functions, classes and imports from a Python file using
    the standard library `ast` module.
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):

        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as file:
            source = file.read()

        tree = ast.parse(source)

        functions = []
        classes = []
        imports = []
        loops = 0
        conditions = 0

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

            elif isinstance(node, ast.Import):
                for module in node.names:
                    imports.append(module.name)

            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)

            elif isinstance(node, (ast.For, ast.While)):
                loops += 1

            elif isinstance(node, ast.If):
                conditions += 1

        return {
            "functions": functions,
            "classes": classes,
            "imports": [i for i in imports if i],
            "loops": loops,
            "conditions": conditions,
        }
