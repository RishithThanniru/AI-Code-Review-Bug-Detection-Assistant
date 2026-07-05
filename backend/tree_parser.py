"""
Multi-language source code parsing powered by Tree-sitter.

Day 12 - Multi-Language Support
    * Automatic language detection from file extension
    * Tree-sitter parsing for Java, C, C++, JavaScript, TypeScript,
      Go, Rust and Kotlin (Python continues to use the built-in `ast`
      module via backend/parser.py, which is faster and needs no
      extra grammar).

Day 13 - Multi-Language Code Analysis
    * Extraction of functions, classes, imports, loops and
      conditional statements for every supported language, used to
      power the dashboards / charts / AI explanations.
"""

import os
import tree_sitter_languages as tsl

# --------------------------------------------------------------------
# Extension -> language name
# --------------------------------------------------------------------

EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".java": "java",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".kt": "kotlin",
    ".kts": "kotlin",
}

# Tree-sitter grammar names differ slightly from our language ids.
GRAMMAR_NAME_MAP = {
    "python": "python",
    "java": "java",
    "c": "c",
    "cpp": "cpp",
    "javascript": "javascript",
    "typescript": "typescript",
    "go": "go",
    "rust": "rust",
    "kotlin": "kotlin",
}

# Node type names, per language, that represent each construct we
# care about. Tree-sitter grammars are independently authored so the
# node names are not identical across languages, hence the mapping.
LANGUAGE_NODE_TYPES = {
    "python": {
        "function": ["function_definition"],
        "class": ["class_definition"],
        "import": ["import_statement", "import_from_statement"],
        "loop": ["for_statement", "while_statement"],
        "condition": ["if_statement"],
    },
    "java": {
        "function": ["method_declaration", "constructor_declaration"],
        "class": ["class_declaration", "interface_declaration", "enum_declaration"],
        "import": ["import_declaration"],
        "loop": ["for_statement", "while_statement", "enhanced_for_statement", "do_statement"],
        "condition": ["if_statement"],
    },
    "c": {
        "function": ["function_definition"],
        "class": ["struct_specifier"],
        "import": ["preproc_include"],
        "loop": ["for_statement", "while_statement", "do_statement"],
        "condition": ["if_statement"],
    },
    "cpp": {
        "function": ["function_definition"],
        "class": ["class_specifier", "struct_specifier"],
        "import": ["preproc_include"],
        "loop": ["for_statement", "while_statement", "do_statement", "for_range_loop"],
        "condition": ["if_statement"],
    },
    "javascript": {
        "function": ["function_declaration", "method_definition", "arrow_function", "function_expression"],
        "class": ["class_declaration"],
        "import": ["import_statement"],
        "loop": ["for_statement", "while_statement", "for_in_statement", "do_statement"],
        "condition": ["if_statement"],
    },
    "typescript": {
        "function": ["function_declaration", "method_definition", "arrow_function", "function_expression"],
        "class": ["class_declaration", "interface_declaration"],
        "import": ["import_statement"],
        "loop": ["for_statement", "while_statement", "for_in_statement", "do_statement"],
        "condition": ["if_statement"],
    },
    "go": {
        "function": ["function_declaration", "method_declaration"],
        "class": ["type_spec"],
        "import": ["import_spec"],
        "loop": ["for_statement"],
        "condition": ["if_statement"],
    },
    "rust": {
        "function": ["function_item"],
        "class": ["struct_item", "enum_item", "impl_item"],
        "import": ["use_declaration"],
        "loop": ["for_expression", "while_expression", "loop_expression"],
        "condition": ["if_expression"],
    },
    "kotlin": {
        "function": ["function_declaration"],
        "class": ["class_declaration", "object_declaration"],
        "import": ["import_header"],
        "loop": ["for_statement", "while_statement", "do_while_statement"],
        "condition": ["if_expression"],
    },
}

# Node types that can hold a readable "name" for a declaration, in
# priority order.
NAME_NODE_TYPES = (
    "identifier",
    "field_identifier",
    "simple_identifier",
    "type_identifier",
    "property_identifier",
)


def detect_language(filename):
    """Return the language id for a filename, defaulting to 'python'."""
    ext = os.path.splitext(filename)[1].lower()
    return EXTENSION_LANGUAGE_MAP.get(ext, "python")


def is_tree_sitter_language(language):
    return language in GRAMMAR_NAME_MAP and language != "python"


class TreeParser:
    """Parses source code for a given language using Tree-sitter and
    extracts functions, classes, imports, loops and conditionals.
    """

    def __init__(self, language):
        self.language = language
        grammar = GRAMMAR_NAME_MAP.get(language, "python")
        self.parser = tsl.get_parser(grammar)
        self.node_types = LANGUAGE_NODE_TYPES.get(language, LANGUAGE_NODE_TYPES["python"])

    def parse(self, code):
        """Parse source text and return the Tree-sitter tree object."""
        if isinstance(code, str):
            code = code.encode("utf-8", errors="ignore")
        return self.parser.parse(code)

    @staticmethod
    def _find_name(node, source_bytes):
        for child in node.children:
            if child.type in NAME_NODE_TYPES:
                return source_bytes[child.start_byte:child.end_byte].decode("utf-8", errors="ignore")
        return "<anonymous>"

    def extract(self, code):
        """Parse the code and return a structured dict compatible with
        the Python AST parser's output, plus loop/condition counts and
        the raw Tree-sitter tree (for the syntax-tree viewer).
        """

        if isinstance(code, str):
            source_bytes = code.encode("utf-8", errors="ignore")
        else:
            source_bytes = code

        tree = self.parser.parse(source_bytes)

        functions = []
        classes = []
        imports = []
        loops = 0
        conditions = 0

        function_types = set(self.node_types["function"])
        class_types = set(self.node_types["class"])
        import_types = set(self.node_types["import"])
        loop_types = set(self.node_types["loop"])
        condition_types = set(self.node_types["condition"])

        def walk(node):
            nonlocal loops, conditions

            if node.type in function_types:
                functions.append(self._find_name(node, source_bytes))

            elif node.type in class_types:
                classes.append(self._find_name(node, source_bytes))

            elif node.type in import_types:
                text = source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")
                imports.append(text.strip().splitlines()[0][:80])

            if node.type in loop_types:
                loops += 1

            if node.type in condition_types:
                conditions += 1

            for child in node.children:
                walk(child)

        walk(tree.root_node)

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "loops": loops,
            "conditions": conditions,
            "tree": tree,
        }
