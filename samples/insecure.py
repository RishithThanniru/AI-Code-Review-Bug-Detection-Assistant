import hashlib
import os
import sqlite3


DB_PASSWORD = "SuperSecret123"  # hardcoded secret


def get_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # SQL injection: query built via string concatenation
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()


def hash_password(password):
    # weak hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()


def run_backup(folder_name):
    # command injection: unsanitized input passed to the shell
    os.system("tar -cvf backup.tar " + folder_name)


def load_config(user_input):
    # unsafe eval usage
    config = eval(user_input)
    return config
