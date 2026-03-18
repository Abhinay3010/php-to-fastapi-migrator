import os
import re

PHP_DIR = "php_app"
OUTPUT_FILE = "fastapi_app/generated.py"

print("🚀 Starting PHP → FastAPI conversion...")


def extract_sql(content):
    # Extract SQL without trailing semicolon
    match = re.search(r'(SELECT .* FROM .*|INSERT INTO .* VALUES .*)', content, re.IGNORECASE)
    if match:
        sql = match.group(1).strip().rstrip(";")
        return sql
    return None


def generate_code():
    code = """
from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_db():
    return sqlite3.connect("test.db")
"""

    files = os.listdir(PHP_DIR)
    print(f"📂 Found PHP files: {files}")

    for file in files:
        print(f"🔍 Processing file: {file}")

        with open(f"{PHP_DIR}/{file}") as f:
            content = f.read()
            sql = extract_sql(content)

            if not sql:
                print(f"⚠️ No SQL found in {file}")
                continue

            print(f"🧠 Clean SQL: {sql}")

            endpoint = file.replace(".php", "")

            # ================= GET =================
            if sql.upper().startswith("SELECT"):
                print(f"➡️ Generating GET endpoint: /{endpoint}")

                code += f"""
@app.get("/{endpoint}")
def {endpoint}():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(\"\"\"{sql}\"\"\")
    rows = cursor.fetchall()
    return [list(row) for row in rows]
"""

            # ================= POST =================
            elif sql.upper().startswith("INSERT"):
                print(f"➡️ Generating POST endpoint: /{endpoint}")

                code += f"""
@app.post("/{endpoint}")
def {endpoint}(name: str, email: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(\"\"\"INSERT INTO users (name, email) VALUES (?, ?)\"\"\", (name, email))
    conn.commit()
    return {{"message": "created"}}
"""

            else:
                print(f"⚠️ Unsupported SQL type in {file}")

    os.makedirs("fastapi_app", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        f.write(code)

    print(f"✅ FastAPI code generated at: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_code()
