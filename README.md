🤖 AI Code Reviewer

An AI-powered, multi-language code review assistant built using Streamlit, Tree-sitter, Python, SQLite, and Groq Llama 3.3.

Analyze source code across multiple programming languages, detect bugs, scan for security vulnerabilities, generate AI-powered code reviews, compare code similarity, chat with your code, and export professional PDF reports—all from a single interactive dashboard.

🚀 Live Demo

Demo: (https://ai-code-reviewer-ezoq4xnesmqfdytcxzyir2.streamlit.app/)

GitHub Repository:
https://github.com/RishithThanniru/AI-Code-Review

✨ Features

🔍 Multi-Language Code Analysis

Supports 9 programming languages

Python
Java
C
C++
JavaScript
TypeScript
Go
Rust
Kotlin
📊 Static Code Analysis
Function extraction
Class extraction
Import detection
Loop detection
Conditional detection
Code metrics
Interactive dashboards
Plotly visualizations
⏱ Time Complexity Estimation

Automatically estimates algorithm complexity such as

O(1)
O(log n)
O(n)
O(n log n)
O(n²)
🤖 AI Code Review (Groq + Llama 3.3)

Provides AI-generated reviews including

Code quality
Bug detection
Best practices
Readability improvements
Performance optimization
Maintainability suggestions
🐞 AI Bug Detection

Detects common programming issues

Infinite loops
Dead code
Division by zero
Unused variables
Duplicate code
Logical mistakes
🔐 Security Scanner

Scans source code for security vulnerabilities

SQL Injection
Hardcoded passwords
API Keys
Weak hashing algorithms
Command Injection
Unsafe eval()
Unsafe exec()
♻ AI Refactoring

Generates cleaner code while preserving functionality.

Includes:

Better naming
Simplified logic
Reduced complexity
Improved readability
🤝 Code Similarity Checker

Compare two source files and obtain

Similarity percentage
Matching code blocks
Shared functions
Shared classes

Useful for plagiarism detection and duplicate code analysis.

💬 AI Code Chatbot

Ask questions about uploaded source code.

Example:

Explain this function
Where is the bug?
How can I optimize this?
Which function has highest complexity?
Explain this algorithm
📄 PDF Report Generation

Generate downloadable reports containing

Code statistics
AI Review
Bug Report
Security Report
Complexity Analysis
Recommendations
🗄 SQLite History

Stores previous analyses including

Filename
Language
Review history
Search
Trend graphs
Delete history


🏗 System Architecture
            Source Code
                  │
                  ▼
      Language Detection
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
 Python AST         Tree-Sitter Parser
        │                   │
        └─────────┬─────────┘
                  ▼
         Static Analysis Engine
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
 Bug Scan   Security Scan  Complexity
        │         │         │
        └─────────┼─────────┘
                  ▼
           Groq LLM Review
        (Llama 3.3 70B Model)
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
 Refactoring   Chatbot   PDF Report
                  │
                  ▼
            Streamlit UI

            
🛠 Tech Stack

Category	Technology
Frontend	Streamlit
Language	Python
Parsing	Python AST
Multi-Language Parsing	Tree-sitter
AI Model	Groq Llama 3.3
Database	SQLite
Visualization	Plotly
Data Processing	Pandas
Reports	ReportLab
Environment	dotenv

📂 Project Structure
AI-Code-Reviewer
│
├── app.py
├── requirements.txt
├── .env.example
│
├── backend
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
│   ├── explainer.py
│   ├── groq_client.py
│   └── pdf_report.py
│
├── database
│   └── database.py
│
└── samples
⚙ Installation

Clone the repository

git clone https://github.com/RishithThanniru/AI-Code-Reviewer.git

Move into the project

cd AI-Code-Reviewer

Create a virtual environment

python -m venv venv

Activate it

Windows

venv\Scripts\activate

Linux/macOS

source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Create .env

GROQ_API_KEY=your_api_key_here

Run the application

streamlit run app.py
🧪 Sample Files

Included under

samples/

Examples include

buggy.py
insecure.py
Sample.java
sample.js
sample.go
complexity.py

📈 Future Improvements

GitHub Pull Request Review
VS Code Extension
Docker Deployment
CI/CD Integration
Multi-file Project Analysis
AI Unit Test Generation
Code Quality Scoring
Git Commit Review
Support for 20+ Languages


💡 Design Decisions
Tree-sitter Version

The project intentionally uses

tree-sitter==0.21.3

to maintain compatibility with

tree-sitter-languages==1.10.2
No Vector Database

Instead of using embeddings or FAISS, the chatbot directly sends the uploaded source code to the LLM.

Benefits

Faster
Lightweight
No Torch dependency
Better live demo experience
Graceful AI Fallback

If no GROQ_API_KEY is configured,

the application still supports

Static Analysis
Complexity Analysis
Security Scan
Bug Detection
Similarity Checker
PDF Report

Only AI Review, AI Refactoring, and Chatbot require the API key.

🎯 Learning Outcomes

Through this project I gained practical experience in

Abstract Syntax Trees (AST)
Tree-sitter Parsing
Static Code Analysis
Prompt Engineering
LLM Integration
AI-powered Software Engineering
Secure Code Analysis
Streamlit Application Development
SQLite Database Management
Software Architecture
PDF Report Generation
👨‍💻 Author

Thanniru Rishith

B.Tech – Artificial Intelligence & Machine Learning
Guru Nanak Institute of Technology, Hyderabad

📧 Email: (thannirurishith25@gmail.com)

💼 LinkedIn:
https://linkedin.com/in/rishiththanniru25

💻 GitHub:
https://github.com/RishithThanniru

⭐ Support

If you found this project useful,

⭐ Star the repository to support the project and future improvements.
