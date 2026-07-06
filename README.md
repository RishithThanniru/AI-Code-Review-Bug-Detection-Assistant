# 🤖 AI Code Reviewer

**A multi-language, AI-powered code review assistant** — built with Streamlit, Tree-sitter, and the Groq API (Llama 3.3). Upload a source file and get structural analysis, static warnings, AI-detected bugs, a security scan, a deep AI code review, refactoring suggestions, a code Q&A chatbot, a duplicate-code checker, and a downloadable PDF report — all in one app.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-F55036)
![Tree-sitter](https://img.shields.io/badge/Parsing-Tree--sitter-5C6BC0)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Try It Out](#-try-it-out)
- [Design Decisions](#-notes-on-design-decisions)
- [Roadmap](#-roadmap-recap-days-1-18)
- [Author](#-author)
- [License](#-license)

---

## 🔎 Overview

AI Code Reviewer analyzes source code across **9 languages** (Python, Java, C, C++, JavaScript, TypeScript, Go, Rust, Kotlin) and combines classic static analysis with LLM-powered review. It was built incrementally over 18 days, starting from Python-only AST parsing and growing into a full multi-language review suite with AI bug detection, security scanning, refactoring, and a code-aware chatbot — all wrapped in an interactive Streamlit dashboard with persistent history and PDF export.

## ✨ Features

### Core Analysis
- 📋 **AST-based parsing** for Python; **Tree-sitter parsing** for Java, C, C++, JavaScript, TypeScript, Go, Rust and Kotlin
- 📊 Function / class / import / loop / conditional extraction
- 📈 Interactive dashboards & charts (Plotly)
- ⏱ Time-complexity estimation
- 🗄 SQLite analysis history with search, trend graph, and clear-history
- 📄 One-click downloadable PDF report

### AI-Powered Review
| Feature | Description |
|---|---|
| Multi-Language Support | Automatic language detection + Tree-sitter parsing, highlighting, and syntax tree for 9 languages |
| Multi-Language Code Analysis | Function/class/import/loop/conditional extraction, dashboards & charts for every supported language |
| AI Code Review | Groq-powered bug detection, code smells, security analysis, performance & improvement suggestions |
| AI Bug Detection | Infinite loops, division by zero, dead code, duplicate code, unused variables |
| Security Scanner | SQL injection, hardcoded secrets, unsafe `eval()`/`exec()`, weak hashing, command injection |
| AI Refactoring | AI-generated refactored code + explanation, without changing behavior |
| Code Similarity Checker | Compare two files: similarity %, matching blocks, shared functions/classes |
| Code Q&A Chatbot | Ask questions about the uploaded file, answered with the file as live context |

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App | Streamlit |
| Parsing | Python `ast`, Tree-sitter (`tree-sitter-languages`) |
| AI | Groq API (`llama-3.3-70b-versatile`) |
| Data | SQLite, Pandas |
| Visualization | Plotly |
| Reports | ReportLab (PDF) |

## 📁 Project Structure

```
AI-Code-Reviewer/
├── app.py                       # Main Streamlit app (all tabs/UI)
├── requirements.txt
├── .env.example                 # Copy to .env and add your Groq key
├── backend/
│   ├── parser.py                # Python AST parser
│   ├── tree_parser.py           # Multi-language Tree-sitter parser
│   ├── analyzer.py              # Python static analysis
│   ├── multi_analyzer.py        # Generic static analysis for other languages
│   ├── complexity.py            # Time-complexity estimation
│   ├── bug_detector.py          # AI bug detection
│   ├── security_scanner.py      # Security scanner
│   ├── ai_reviewer.py           # AI code review via Groq
│   ├── refactorer.py            # AI refactoring via Groq
│   ├── similarity.py            # Code similarity checker
│   ├── explainer.py             # Local (offline) code summary
│   ├── chatbot.py               # Code Q&A chatbot via Groq
│   ├── groq_client.py           # Shared Groq API wrapper
│   └── pdf_report.py            # PDF report generator
├── database/
│   └── database.py              # SQLite history persistence
└── samples/                     # Example files to try the app with
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

The app works fully for static analysis, bug detection, and the security scanner **without** a Groq key. Only the AI Review, AI Refactoring, and Chatbot tabs require `GROQ_API_KEY` to be set.

## 🧪 Try It Out

Sample files are included under `samples/` — several languages, intentionally seeded with bugs and security issues so you can demo every tab:

- `samples/buggy.py` — unused variables, infinite loop, division by zero
- `samples/insecure.py` — SQL injection, hardcoded password, weak hashing
- `samples/Sample.java`, `samples/sample.js`, `samples/sample.go` — multi-language parsing demo
- `samples/complexity.py` — time-complexity estimation demo

## 📌 Notes on Design Decisions

- **`tree-sitter==0.21.3` is pinned intentionally.** Newer `tree-sitter` releases changed the `Language()` constructor signature and are incompatible with `tree-sitter-languages==1.10.2`'s prebuilt grammars — installing the latest `tree-sitter` will break multi-language parsing.
- **The chatbot sends the file directly as context** instead of using a FAISS + embeddings pipeline. A single source file comfortably fits an LLM's context window, so this avoids a heavy `torch`/`transformers` dependency and a first-run model download — much more reliable for a live demo.
- **Every AI-powered feature degrades gracefully** when `GROQ_API_KEY` isn't set: the UI shows a clear message instead of crashing, so the rest of the app (static analysis, bug detection, security scan, similarity checker, PDF report) still works out of the box.

## 🗺 Roadmap Recap (Days 1–18)

Days 1–11 established the core: AST parsing, static analysis, complexity estimation, PDF reporting, and SQLite history. Days 12–18 added multi-language support via Tree-sitter, AI-powered bug/security/refactoring analysis via Groq, and a code similarity checker.


## 🔭 Future Scope

- **CI/CD Integration** — GitHub Actions / GitLab CI plugin to run reviews automatically on every pull request and post results as PR comments
- **VS Code Extension** — bring inline AI review, bug detection, and refactoring suggestions directly into the editor
- **Multi-file / repo-level analysis** — currently single-file focused; extend to whole-repository scans with cross-file dependency and duplicate-code detection
- **Custom rule engine** — let teams define their own linting/security rules on top of the built-in checks
- **Model flexibility** — support additional LLM providers (OpenAI, Anthropic, local models via Ollama) alongside Groq, with a pluggable backend
- **Authentication & multi-user support** — user accounts so review history and reports are scoped per user/team instead of a single shared SQLite file
- **Diff-aware refactoring** — show refactored code as a side-by-side diff instead of a full rewrite, making changes easier to review
- **Test generation** — AI-generated unit tests for the analyzed file, alongside the existing bug/security findings
- **Dockerized deployment** — a `Dockerfile` + `docker-compose.yml` for one-command setup, removing the manual venv/env steps
- **Richer language coverage** — extend Tree-sitter support to PHP, Ruby, Swift, and C#
- **Team dashboards** — aggregate trends across a codebase over time (bug counts, complexity, security issues) rather than per-file history only

## 👤 Author

**Thanniru Rishith**
Final-year B.Tech (AI/ML), Guru Nanak Institute of Technology, Hyderabad

- LinkedIn: [linkedin.com/in/rishiththanniru25](https://linkedin.com/in/rishiththanniru25)
