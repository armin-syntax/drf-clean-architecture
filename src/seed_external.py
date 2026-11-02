import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "external.sqlite3"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS ext_users;")
cursor.execute("""
    CREATE TABLE ext_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        first_name TEXT,
        last_name TEXT
    );
""")
cursor.execute("""
    INSERT INTO ext_users (username, email, first_name, last_name) VALUES
    ('ali_ext', 'ali@external.com', 'Ali', 'Rezaei'),
    ('sara_ext', 'sara@external.com', 'Sara', 'Ahmadi'),
    ('reza_ext', 'reza@external.com', 'Reza', 'Karimi');
""")
conn.commit()
cursor.close()
conn.close()
print("External SQLite Database seeded successfully.")
