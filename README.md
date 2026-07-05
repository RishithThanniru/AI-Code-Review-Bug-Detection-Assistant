# 🤖 AI Code Reviewer

A multi-language, AI-powered code review assistant built with **Streamlit**,
**Tree-sitter**, and **Groq (Llama 3.3)**. Upload a source file and get
structural analysis, static warnings, AI-detected bugs, a security scan,
a deep AI review, refactoring suggestions, a code Q&A chatbot, a
duplicate-code checker, and a downloadable PDF report — all in one app.

## ✨ Features

### Core Analysis
- 📋 **AST-based parsing** for Python; **Tree-sitter parsing** for Java, C,
  C++, JavaScript, TypeScript, Go, Rust and Kotlin
- 📊 Functions / classes / imports / loops / conditionals extraction
- 📈 Interactive dashboards & charts (Plotly)
- ⏱ Time-complexity estimation
- 🗄 SQLite analysis history with search, trend graph, and clear-history
- 📄 One-click downloadable PDF report

### AI-Powered Review (Day 12–18)
| Day | Feature | Description |
|-----|---------|--------------|
| 12 | Multi-Language Support | Automatic language detection + Tree-sitter parsing/highlighting/syntax tree for 9 languages |
| 13 | Multi-Language Code Analysis | Function/class/import/loop/conditional extraction, dashboards & charts for every supported language |
| 14 | AI Code Review | Groq-powered bug detection, code smells, security analysis, performance & improvement suggestions |
| 15 | AI Bug Detection | Infinite loops, division by zero, dead code, duplicate code, unused variables |
| 16 | Security Scanner | SQL injection, hardcoded secrets, unsafe `eval()`/`exec()`, weak hashing, command injection |
| 17 | AI Refactoring | AI-generated refactored code + explanation, without changing behavior |
| 18 | Code Similarity Checker | Compare two files: similarity %, matching blocks, shared functions/classes |

## 🧱 Tech Stack

- **Frontend / App:** Streamlit
- **Parsing:** Python `ast`, Tree-sitter (`tree-sitter-languages`)
- **AI:** Groq API (`llama-3.3-70b-versatile`)
- **Data:** SQLite, Pandas
- **Visualization:** Plotly
- **Reports:** ReportLab (PDF)

## 📁 Project Structure

```
AI-Code-Reviewer/
├── app.py                     # Main Streamlit app (all tabs/UI)
├── requirements.txt
├── .env.example                # Copy to .env and add your Groq key
├── backend/
│   ├── parser.py               # Python AST parser
│   ├── tree_parser.py          # Multi-language Tree-sitter parser (Day 12/13)
│   ├── analyzer.py              # Python static analysis
│   ├── multi_analyzer.py        # Generic static analysis for other languages
│   ├── complexity.py            # Time-complexity estimation
│   ├── bug_detector.py           # AI bug detection (Day 15)
│   ├── security_scanner.py       # Security scanner (Day 16)
│   ├── ai_reviewer.py            # AI code review via Groq (Day 14)
│   ├── refactorer.py             # AI refactoring via Groq (Day 17)
│   ├── similarity.py             # Code similarity checker (Day 18)
│   ├── explainer.py              # Local (offline) code summary
│   ├── chatbot.py                 # Code Q&A chatbot via Groq
│   ├── groq_client.py             # Shared Groq API wrapper
│   └── pdf_report.py              # PDF report generator
├── database/
│   └── database.py                # SQLite history persistence
└── samples/                        # Example files to try the app with
```

## 🚀 Getting Started

```bash
# 1. Clone and enter the project
git clone <your-repo-url>
cd AI-Code-Reviewer

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional but recommended) enable AI features
cp .env.example .env
# then edit .env and add a free key from https://console.groq.com/keys

# 5. Run the app
streamlit run app.py
```

The app works fully for static analysis, bug detection and the security
scanner **without** a Groq key. Only the AI Review, AI Refactoring and
Chatbot tabs require `GROQ_API_KEY` to be set.

## 🧪 Try It Out

Sample files are included under `samples/` covering several languages and
intentionally containing bugs/security issues so you can demo every tab:

- `samples/buggy.py` — unused variables, infinite loop, division by zero
- `samples/insecure.py` — SQL injection, hardcoded password, weak hashing
- `samples/Sample.java`, `samples/sample.js`, `samples/sample.go` — multi-language parsing demo

## 📌 Notes on Design Decisions

- **`tree-sitter==0.21.3` is pinned intentionally.** Newer `tree-sitter`
  releases changed the `Language()` constructor signature and are
  incompatible with `tree-sitter-languages==1.10.2`'s prebuilt grammars —
  installing the latest `tree-sitter` will break multi-language parsing.
- **The chatbot sends the file directly as context** instead of using a
  FAISS + HuggingFace embeddings pipeline. A single source file comfortably
  fits an LLM's context window, so this avoids a heavy `torch`/
  `transformers` dependency and a first-run model download — much more
  reliable for a live demo.
- **Every AI-powered feature degrades gracefully** when `GROQ_API_KEY`
  isn't set: the UI shows a clear message instead of crashing, so the rest
  of the app (static analysis, bug detection, security scan, similarity
  checker, PDF report) still works out of the box.

## 🗺 Roadmap Recap (Days 1–18)

Days 1–11 established the core: AST parsing, static analysis, complexity
estimation, PDF reporting and SQLite history. Days 12–18 (this update)
added multi-language support via Tree-sitter, AI-powered bug/security/
refactoring analysis via Groq, and a code similarity checker — see the
table above for details.
