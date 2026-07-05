"""
SQLite persistence layer for the AI Code Reviewer.

Stores one row per analyzed file so the app can show a searchable
history and a trend graph across sessions.
"""

import sqlite3

DATABASE = "code_review.db"


def _connect():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_table():
    """Create the history table if it doesn't exist yet, and migrate
    older databases (from earlier versions of this project) that are
    missing the newer columns used by the multi-language / AI review
    features.
    """

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        language TEXT,
        functions INTEGER,
        classes INTEGER,
        imports INTEGER,
        warnings INTEGER,
        bugs INTEGER,
        security_issues INTEGER,
        complexity TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Lightweight migration for databases created by earlier versions
    # of this project that only had the original 7 columns.
    cursor.execute("PRAGMA table_info(analysis_history)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    migrations = {
        "language": "TEXT DEFAULT 'python'",
        "bugs": "INTEGER DEFAULT 0",
        "security_issues": "INTEGER DEFAULT 0",
    }

    for column, definition in migrations.items():
        if column not in existing_columns:
            cursor.execute(
                f"ALTER TABLE analysis_history ADD COLUMN {column} {definition}"
            )

    conn.commit()
    conn.close()


def insert_analysis(
    filename,
    functions,
    classes,
    imports,
    warnings,
    complexity,
    language="python",
    bugs=0,
    security_issues=0,
):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analysis_history(
        filename, language, functions, classes,
        imports, warnings, bugs, security_issues, complexity
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        filename, language, functions, classes,
        imports, warnings, bugs, security_issues, complexity
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, filename, language, functions, classes,
           imports, warnings, bugs, security_issues, complexity, created_at
    FROM analysis_history
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def clear_history():
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analysis_history")
    conn.commit()
    conn.close()
