# 🤖 AI Code Reviewer

An advanced **AI-powered, multi-language code review platform** built using **Python, Streamlit, Tree-sitter, and Groq Llama 3.3**. The application combines traditional static code analysis with Large Language Models (LLMs) to automate code reviews, detect bugs, identify security vulnerabilities, suggest refactoring improvements, answer code-related questions, and generate professional PDF reports.

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge)](https://ai-code-reviewer-ezoq4xnesmqfdytcxzyir2.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-F55036)
![Tree-sitter](https://img.shields.io/badge/Parsing-Tree--sitter-5C6BC0)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 🌐 Live Demo

### 🚀 Try the Application

https://ai-code-reviewer-ezoq4xnesmqfdytcxzyir2.streamlit.app/

No installation required. Simply upload a supported source code file and explore AI-powered code analysis.

---

# 📑 Table of Contents

- Overview
- Project Objective
- Key Highlights
- Features
- Tech Stack
- Project Structure
- Installation
- Usage
- Design Decisions
- Future Scope
- Author

---

# 🔎 Overview

AI Code Reviewer is a modern software engineering assistant that supports **9 programming languages** including Python, Java, C, C++, JavaScript, TypeScript, Go, Rust, and Kotlin.

The application combines:

- Static Code Analysis
- Abstract Syntax Tree (AST) Parsing
- Tree-sitter Parsing
- Large Language Models (Groq Llama 3.3)
- Natural Language Processing
- Security Analysis

to help developers write cleaner, safer, and more maintainable code.

---

# 🎯 Project Objective

The objective of this project is to automate software code reviews using Artificial Intelligence by combining traditional static analysis techniques with Large Language Models.

The system helps developers:

- Detect bugs automatically
- Identify security vulnerabilities
- Improve code quality
- Understand complex source code
- Generate professional review reports
- Reduce manual review effort

---

# ✨ Key Highlights

- ✅ AI-powered multi-language code review
- ✅ Supports 9 programming languages
- ✅ Static code analysis
- ✅ AI bug detection
- ✅ Security vulnerability scanner
- ✅ AI-powered refactoring suggestions
- ✅ Code similarity checker
- ✅ AI chatbot for source code
- ✅ Interactive Streamlit dashboard
- ✅ SQLite history tracking
- ✅ Downloadable PDF reports

---

# 🚀 Features

## 📋 Static Analysis

- Python AST Parsing
- Tree-sitter Parsing
- Function Extraction
- Class Extraction
- Import Detection
- Loop Detection
- Conditional Detection
- Time Complexity Estimation

---

## 🤖 AI Features

- AI Code Review
- AI Bug Detection
- AI Refactoring
- Code Explanation
- Code Q&A Chatbot
- Duplicate Code Detection
- Semantic Code Understanding

---

## 🔒 Security Analysis

Detects

- SQL Injection
- Hardcoded Passwords
- Weak Hashing
- Unsafe eval()
- Unsafe exec()
- Command Injection
- Dangerous Imports

---

## 📊 Analytics

- Interactive Plotly Charts
- Code Statistics
- Language Detection
- SQLite History
- Search Previous Reviews
- Trend Analysis

---

## 📄 Reports

Generate downloadable PDF reports including

- Code Statistics
- AI Review
- Security Findings
- Bug Detection
- Complexity Analysis
- Refactoring Suggestions

---

# 🛠 Tech Stack

| Category | Technology |
|------------|----------------|
| Programming Language | Python |
| Frontend | Streamlit |
| AI Model | Groq Llama 3.3 |
| Parsing | Python AST, Tree-sitter |
| Machine Learning | TF-IDF, Cosine Similarity |
| Database | SQLite |
| Visualization | Plotly |
| Reports | ReportLab |
| Version Control | Git, GitHub |

---

# 📂 Project Structure

```
AI-Code-Reviewer/
│
├── app.py
├── requirements.txt
├── backend/
│   ├── parser.py
│   ├── tree_parser.py
│   ├── analyzer.py
│   ├── multi_analyzer.py
│   ├── complexity.py
│   ├── bug_detector.py
│   ├── security_scanner.py
│   ├── ai_reviewer.py
│   ├── refactorer.py
│   ├── similarity.py
│   ├── chatbot.py
│   ├── pdf_report.py
│
├── database/
│   └── database.py
│
├── samples/
│
└── requirements.txt
```

---

# ⚙️ Installation

```bash
git clone https://github.com/RishithThanniru/AI-Code-Reviewer.git

cd AI-Code-Reviewer

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

# 💻 Usage

1. Upload a source code file.

2. Select the programming language.

3. View

- Static Analysis
- AI Review
- Security Scan
- Bug Detection
- Refactoring Suggestions
- Similarity Report
- Complexity Analysis

4. Download the generated PDF report.

---

# 📌 Design Decisions

- Tree-sitter is used for accurate multi-language parsing.
- Groq Llama 3.3 provides fast AI-powered code reviews.
- SQLite stores review history locally.
- Streamlit enables rapid interactive visualization.
- AI features degrade gracefully when no API key is configured.
- Static analysis continues to function without AI services.

---

# 📈 Project Impact

- Automated software code review using AI.
- Reduced manual review effort.
- Improved code quality and maintainability.
- Automated security vulnerability detection.
- Accelerated debugging and refactoring.
- Simplified developer onboarding using AI explanations.

---

# 🔭 Future Scope

The project is designed to be extensible for enterprise software development workflows.

### Planned Enhancements

- Repository-level analysis with cross-file dependency tracking.
- CI/CD integration using GitHub Actions, GitLab CI, and Jenkins.
- Visual Studio Code and JetBrains IDE extensions.
- Support for additional programming languages including C#, PHP, Ruby, Swift, and Dart.
- AI-generated unit test creation.
- Custom static analysis rule engine.
- Multi-LLM support (OpenAI, Claude, Gemini, Ollama).
- Docker and Kubernetes deployment.
- Team collaboration with authentication and role-based access.
- Repository health dashboard for tracking technical debt, complexity, and security trends.
- Enterprise reporting and analytics.

---

# 👨‍💻 Author

## Thanniru Rishith

**B.Tech – Artificial Intelligence & Machine Learning**

Guru Nanak Institute of Technology, Hyderabad

🔗 GitHub  
https://github.com/RishithThanniru

🔗 LinkedIn  
https://linkedin.com/in/rishiththanniru25

---

⭐ **If you found this project useful, consider giving it a Star on GitHub!**
