import sqlite3

print("🔧 Starting DB initialization...")

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

print("📦 Creating table: users")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully!")
