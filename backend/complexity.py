import ast


class ComplexityAnalyzer:
    """Estimates Big-O time complexity for Python source using `ast`."""

    def __init__(self, filepath):
        self.filepath = filepath

    def analyze(self):

        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as file:
            source = file.read()

        tree = ast.parse(source)

        return estimate_from_loop_depth_and_recursion(
            max_loop_depth(tree),
            has_recursion(tree),
        )


def max_loop_depth(tree):
    """Compute the maximum nesting depth of for/while loops in an AST."""
    max_depth = 0

    def visit(node, depth=0):
        nonlocal max_depth

        if isinstance(node, (ast.For, ast.While)):
            depth += 1
            max_depth = max(max_depth, depth)

        for child in ast.iter_child_nodes(node):
            visit(child, depth)

    visit(tree)
    return max_depth


def has_recursion(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id == node.name:
                        return True
    return False


def estimate_from_loop_depth_and_recursion(max_depth, recursive):

    if recursive:
        return {
            "complexity": "O(2^n)",
            "reason": "Recursive function detected without a clear reduction pattern.",
        }

    if max_depth == 0:
        return {
            "complexity": "O(1)",
            "reason": "No loops detected.",
        }

    if max_depth == 1:
        return {
            "complexity": "O(n)",
            "reason": "One loop detected.",
        }

    if max_depth == 2:
        return {
            "complexity": "O(n\u00b2)",
            "reason": "Nested loops detected.",
        }

    return {
        "complexity": f"O(n^{max_depth})",
        "reason": f"{max_depth} nested loops detected.",
    }


def estimate_complexity_generic(loop_count, max_nesting_hint=None):
    """Heuristic complexity estimate for non-Python languages, based on
    the total loop count reported by Tree-sitter (which does not
    easily expose nesting depth without a second pass). This is
    intentionally conservative and clearly labelled as an estimate in
    the UI.
    """

    if loop_count == 0:
        return {
            "complexity": "O(1)",
            "reason": "No loops detected.",
        }

    if loop_count == 1:
        return {
            "complexity": "O(n)",
            "reason": "One loop detected.",
        }

    if loop_count == 2:
        return {
            "complexity": "O(n\u00b2) (estimate)",
            "reason": "Two loops detected — likely nested, but exact nesting isn't verified for this language.",
        }

    return {
        "complexity": f"O(n^{min(loop_count, 4)}) (estimate)",
        "reason": f"{loop_count} loops detected across the file.",
    }
