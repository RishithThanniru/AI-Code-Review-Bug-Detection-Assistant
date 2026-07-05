import os

import pandas as pd
import plotly.express as px
import streamlit as st

from backend.parser import CodeParser
from backend.tree_parser import TreeParser, detect_language, is_tree_sitter_language
from backend.analyzer import CodeAnalyzer
from backend.multi_analyzer import MultiLanguageAnalyzer
from backend.complexity import ComplexityAnalyzer, estimate_complexity_generic
from backend.bug_detector import BugDetector
from backend.security_scanner import SecurityScanner
from backend.ai_reviewer import AIReviewer
from backend.refactorer import CodeRefactorer
from backend.similarity import SimilarityChecker
from backend.explainer import CodeExplainer
from backend.chatbot import CodeChatBot
from backend.pdf_report import PDFReport
from backend import groq_client

from database.database import (
    create_table,
    insert_analysis,
    get_history,
    clear_history,
)

# --------------------------------------------------
# Setup
# --------------------------------------------------

create_table()

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🤖",
    layout="wide",
)

SUPPORTED_TYPES = ["py", "java", "c", "h", "cpp", "cc", "hpp", "js", "jsx", "ts", "tsx", "go", "rs", "kt", "kts"]

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.title("🤖 AI Code Reviewer")
    st.caption("Multi-language static + AI-powered code review")

    st.markdown("---")
    st.write("✅ Multi-language parsing (Tree-sitter)")
    st.write("✅ Static analysis & complexity")
    st.write("✅ AI bug detection")
    st.write("✅ Security scanner")
    st.write("✅ AI code review (Groq)")
    st.write("✅ AI refactoring")
    st.write("✅ Code similarity checker")
    st.write("✅ SQLite history + PDF reports")
    st.markdown("---")

    if groq_client.is_configured():
        st.success("Groq API key detected — AI features enabled")
    else:
        st.warning("No GROQ_API_KEY found — AI Review / Refactor / Chat are disabled. See .env.example.")

    st.info("Version 3.0 — Multi-language + AI")


def analyze_file(filepath, language):
    """Run the full analysis pipeline for a single file and return a
    dict with every result the UI needs."""

    if language == "python":
        parsed_result = CodeParser(filepath).parse()
        warnings = CodeAnalyzer(filepath).analyze()
        complexity_result = ComplexityAnalyzer(filepath).analyze()
        tree = None
    else:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
        tp = TreeParser(language)
        extracted = tp.extract(code)
        tree = extracted.pop("tree")
        parsed_result = extracted
        warnings = MultiLanguageAnalyzer(filepath, language).analyze()
        complexity_result = estimate_complexity_generic(parsed_result.get("loops", 0))

    explanation = CodeExplainer(parsed_result, language).explain()
    bugs = BugDetector(filepath, language).detect()
    security_issues = SecurityScanner(filepath).scan()

    return {
        "parsed_result": parsed_result,
        "warnings": warnings,
        "complexity_result": complexity_result,
        "explanation": explanation,
        "bugs": bugs,
        "security_issues": security_issues,
        "tree": tree,
    }


st.title("🤖 AI Code Review & Bug Detection Assistant")

st.markdown("""
Upload a source file to get structural analysis, static warnings, AI-detected bugs,
a security scan, and (with a Groq API key) a deep AI review, refactoring suggestions
and a code chatbot.

**Supported languages:** Python · Java · C · C++ · JavaScript · TypeScript · Go · Rust · Kotlin
""")

uploaded_file = st.file_uploader("Upload Source Code", type=SUPPORTED_TYPES)

if uploaded_file:
    os.makedirs("uploads", exist_ok=True)
    filepath = os.path.join("uploads", uploaded_file.name)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    language = detect_language(uploaded_file.name)
    st.success(f"✅ File uploaded — detected language: **{language.capitalize()}**")

    with st.spinner("Analyzing..."):
        result = analyze_file(filepath, language)

    parsed_result = result["parsed_result"]
    warnings = result["warnings"]
    complexity_result = result["complexity_result"]
    explanation = result["explanation"]
    bugs = result["bugs"]
    security_issues = result["security_issues"]
    tree = result["tree"]

    insert_analysis(
        uploaded_file.name,
        len(parsed_result["functions"]),
        len(parsed_result["classes"]),
        len(parsed_result["imports"]),
        len(warnings),
        complexity_result["complexity"],
        language=language,
        bugs=len(bugs),
        security_issues=len(security_issues),
    )

    tabs = st.tabs([
        "📊 Dashboard",
        "⚠ Static & Bugs",
        "🔒 Security",
        "🤖 AI Review & Chat",
        "🛠 Refactor",
        "🧬 Similarity",
        "📄 Report",
    ])

    # ==================================================
    # TAB 1 — Dashboard
    # ==================================================
    with tabs[0]:
        st.header("📁 File Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Filename:**", uploaded_file.name)
            st.write("**Size:**", f"{uploaded_file.size / 1024:.2f} KB")
        with col2:
            st.write("**Language:**", language.capitalize())
            st.write("**Status:** Analyzed ✅")

        st.header("📋 Code Structure")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("Functions")
            st.write(parsed_result["functions"] or "None found")
        with c2:
            st.subheader("Classes")
            st.write(parsed_result["classes"] or "None found")
        with c3:
            st.subheader("Imports")
            st.write(parsed_result["imports"] or "None found")

        st.header("📊 Code Statistics")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Functions", len(parsed_result["functions"]))
        m2.metric("Classes", len(parsed_result["classes"]))
        m3.metric("Imports", len(parsed_result["imports"]))
        m4.metric("Warnings", len(warnings))
        m5.metric("Bugs", len(bugs))

        df = pd.DataFrame({
            "Category": ["Functions", "Classes", "Imports", "Warnings", "Bugs"],
            "Count": [
                len(parsed_result["functions"]),
                len(parsed_result["classes"]),
                len(parsed_result["imports"]),
                len(warnings),
                len(bugs),
            ],
        })

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig = px.pie(df, names="Category", values="Count", title="Code Composition")
            st.plotly_chart(fig, use_container_width=True)
        with chart_col2:
            fig2 = px.bar(df, x="Category", y="Count", text="Count", title="Project Metrics")
            st.plotly_chart(fig2, use_container_width=True)

        if tree is not None:
            with st.expander("🌳 Syntax Tree (Tree-sitter)"):
                st.code(str(tree.root_node)[:5000], language="text")

        with st.expander("📄 Source Code"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                st.code(f.read(), language=language if language != "csharp" else "text")

    # ==================================================
    # TAB 2 — Static Review + Bug Detection (Day 15)
    # ==================================================
    with tabs[1]:
        st.header("⚠ Static Code Review")
        if warnings:
            for w in warnings:
                if "Dangerous" in w or "unreachable" in w.lower():
                    st.error(w)
                elif "Unused" in w or "unused" in w:
                    st.warning(w)
                else:
                    st.info(w)
        else:
            st.success("🎉 No static warnings found!")

        st.header("⏱ Estimated Time Complexity")
        st.metric("Estimated Complexity", complexity_result["complexity"])
        st.info(complexity_result["reason"])

        st.header("🐞 AI Bug Detection")
        st.caption("Infinite loops · division by zero · dead code · duplicate code · unused variables")
        if bugs:
            for b in bugs:
                st.error(b)
        else:
            st.success("🎉 No bugs detected!")

    # ==================================================
    # TAB 3 — Security Scanner (Day 16)
    # ==================================================
    with tabs[2]:
        st.header("🔒 Security Scan Results")
        st.caption("SQL injection · hardcoded secrets · eval/exec · weak hashing · command injection")

        if security_issues:
            summary = SecurityScanner.summarize(security_issues)
            s1, s2, s3 = st.columns(3)
            s1.metric("🔴 High", summary.get("High", 0))
            s2.metric("🟠 Medium", summary.get("Medium", 0))
            s3.metric("🟡 Low", summary.get("Low", 0))

            for issue in security_issues:
                severity_icon = {"High": "🔴", "Medium": "🟠", "Low": "🟡"}.get(issue["severity"], "⚪")
                with st.expander(f"{severity_icon} Line {issue['line']} — {issue['type']}"):
                    st.write(issue["message"])
                    st.code(issue["code"], language=language)
        else:
            st.success("🎉 No security issues detected!")

    # ==================================================
    # TAB 4 — AI Review (Day 14) + Chatbot
    # ==================================================
    with tabs[3]:
        st.header("🤖 AI Code Review")
        st.caption("Bug detection, code smells, security analysis, performance & improvement suggestions — powered by Groq")

        if st.button("🚀 Run AI Review", key="run_ai_review"):
            with st.spinner("Asking the AI reviewer..."):
                ai_result = AIReviewer(filepath, language).review(
                    static_bugs=bugs, static_security=security_issues
                )
            st.session_state["ai_review_result"] = ai_result

        ai_result = st.session_state.get("ai_review_result")

        if ai_result:
            if not ai_result["available"]:
                st.warning(ai_result["message"])
            else:
                sections = [
                    ("bugs", "🐞 Bugs"),
                    ("code_smells", "👃 Code Smells"),
                    ("security_issues", "🔒 Security Issues"),
                    ("performance_suggestions", "⚡ Performance Suggestions"),
                    ("improvements", "💡 Improvements"),
                ]
                for key, label in sections:
                    st.subheader(label)
                    values = ai_result.get(key) or []
                    if values:
                        for v in values:
                            st.write(f"- {v}")
                    else:
                        st.caption("None found.")

        st.markdown("---")
        st.header("💬 Ask About Your Code")
        question = st.text_input("Ask any question about the uploaded code")

        if question:
            if not groq_client.is_configured():
                st.warning("Chat is disabled because GROQ_API_KEY is not configured.")
            else:
                with st.spinner("🤖 Thinking..."):
                    try:
                        answer = CodeChatBot(filepath, language).ask(question)
                        st.markdown("### 🤖 Answer")
                        st.markdown(answer)
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ==================================================
    # TAB 5 — AI Refactoring (Day 17)
    # ==================================================
    with tabs[4]:
        st.header("🛠 AI Refactoring Suggestions")
        st.caption("Improves readability, maintainability and performance without changing behavior")

        if st.button("✨ Generate Refactoring", key="run_refactor"):
            with st.spinner("Refactoring..."):
                refactor_result = CodeRefactorer(filepath, language).refactor()
            st.session_state["refactor_result"] = refactor_result

        refactor_result = st.session_state.get("refactor_result")

        if refactor_result:
            if not refactor_result["available"]:
                st.warning(refactor_result["message"])
            else:
                st.subheader("Refactored Code")
                st.code(refactor_result["refactored_code"], language=language)
                st.subheader("Explanation")
                st.markdown(refactor_result["explanation"])
                st.download_button(
                    "⬇ Download Refactored Code",
                    data=refactor_result["refactored_code"],
                    file_name=f"refactored_{uploaded_file.name}",
                )

    # ==================================================
    # TAB 6 — Similarity Checker (Day 18)
    # ==================================================
    with tabs[5]:
        st.header("🧬 Code Similarity Checker")
        st.caption("Compare the uploaded file above against a second file to detect duplicate or near-duplicate logic")

        second_file = st.file_uploader("Upload a second file to compare against", type=SUPPORTED_TYPES, key="second_file")

        if second_file:
            second_path = os.path.join("uploads", f"compare_{second_file.name}")
            with open(second_path, "wb") as f:
                f.write(second_file.getbuffer())

            checker = SimilarityChecker(filepath, second_path)
            comparison = checker.compare()

            st.metric("Similarity", f"{comparison['similarity_percent']}%")
            st.write(SimilarityChecker.verdict(comparison["similarity_percent"]))

            st.progress(min(int(comparison["similarity_percent"]), 100))

            second_language = detect_language(second_file.name)
            if second_language == "python":
                second_parsed = CodeParser(second_path).parse()
            else:
                with open(second_path, "r", encoding="utf-8", errors="ignore") as f:
                    second_parsed = TreeParser(second_language).extract(f.read())
                    second_parsed.pop("tree", None)

            structure_overlap = SimilarityChecker.compare_structures(parsed_result, second_parsed)

            st.subheader("Shared Structure")
            oc1, oc2 = st.columns(2)
            with oc1:
                st.write("**Shared functions:**", structure_overlap["shared_functions"] or "None")
            with oc2:
                st.write("**Shared classes:**", structure_overlap["shared_classes"] or "None")

            if comparison["matching_blocks"]:
                with st.expander(f"🔍 {len(comparison['matching_blocks'])} matching code block(s)"):
                    for block in comparison["matching_blocks"][:10]:
                        st.caption(
                            f"{uploaded_file.name} line {block['a_start']} ↔ "
                            f"{second_file.name} line {block['b_start']} "
                            f"({block['size']} lines)"
                        )
                        st.code("\n".join(block["lines"]), language="text")
        else:
            st.info("Upload a second file above to run the comparison.")

    # ==================================================
    # TAB 7 — Report
    # ==================================================
    with tabs[6]:
        st.header("📄 Download Full PDF Report")

        pdf = PDFReport()
        pdf_path = pdf.generate(
            uploaded_file.name,
            parsed_result,
            warnings,
            complexity_result,
            explanation,
            language=language,
            bugs=bugs,
            security_issues=security_issues,
            ai_review=st.session_state.get("ai_review_result"),
        )

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_file,
                file_name=f"{uploaded_file.name}_report.pdf",
                mime="application/pdf",
            )

# --------------------------------------------------
# Analysis History
# --------------------------------------------------

st.markdown("---")
st.header("🗄 Analysis History")

hist_col1, hist_col2 = st.columns([3, 1])
with hist_col1:
    search = st.text_input("🔍 Search history by filename")
with hist_col2:
    st.write("")
    if st.button("🗑 Clear History"):
        clear_history()
        st.success("History cleared!")
        st.rerun()

history = get_history()

columns = ["id", "filename", "language", "functions", "classes", "imports", "warnings", "bugs", "security_issues", "complexity", "created_at"]

filtered_history = [row for row in history if search.lower() in row[1].lower()] if search else history

if filtered_history:
    for row in filtered_history[:50]:
        record = dict(zip(columns, row))
        with st.expander(f"📄 {record['filename']} ({record['language']}) — {record['created_at']}"):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Functions", record["functions"])
            c2.metric("Classes", record["classes"])
            c3.metric("Warnings", record["warnings"])
            c4.metric("Bugs", record["bugs"])
            c5.metric("Security", record["security_issues"])
            st.write(f"**Complexity:** {record['complexity']}")

    st.header("📈 Analysis Trend")
    trend_df = pd.DataFrame(filtered_history, columns=columns)
    fig_trend = px.line(trend_df.iloc[::-1], x="filename", y="warnings", markers=True, title="Warnings per Analyzed File")
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("No history data available yet — upload a file above to get started.")
