import os
import re

PHP_DIR = "php_app"
OUTPUT_FILE = "fastapi_app/routes/generated.py"

HEADER = """
from fastapi import APIRouter
from fastapi_app.database import SessionLocal
from fastapi_app import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

def extract_sql(content):
    match = re.search(r'(SELECT .* FROM .*|INSERT INTO .* VALUES .*);?', content)
    return match.group(1) if match else None

def generate_get(endpoint, sql):
    return f"""
@router.get("/{endpoint}")
def {endpoint}(db=next(get_db())):
    result = db.execute("{sql}").fetchall()
    return [dict(row) for row in result]
"""

def generate_post(endpoint):
    return f"""
@router.post("/{endpoint}")
def {endpoint}(name: str, email: str, db=next(get_db())):
    db.execute("INSERT INTO users (name, email) VALUES (:name, :email)", {{"name": name, "email": email}})
    db.commit()
    return {{"message": "created"}}
"""

def run():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    code = HEADER

    for file in os.listdir(PHP_DIR):
        with open(f"{PHP_DIR}/{file}") as f:
            content = f.read()
            sql = extract_sql(content)

            endpoint = file.replace(".php", "")

            if sql and sql.startswith("SELECT"):
                code += generate_get(endpoint, sql)

            elif sql and sql.startswith("INSERT"):
                code += generate_post(endpoint)

    with open(OUTPUT_FILE, "w") as f:
        f.write(code)

if __name__ == "__main__":
    run()
