import sqlite3

conn = sqlite3.connect("ecm_lite_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id TEXT NOT NULL,
    version INTEGER NOT NULL CHECK(version >= 1),
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    upload_date TEXT NOT NULL,
    classification TEXT NOT NULL CHECK(classification IN ('public', 'private', 'restricted', 'critical')),
    department TEXT NOT NULL,
    lifecycle_stage INTEGER NOT NULL CHECK(0 <= lifecycle_stage <= 3),
    is_deleted INTEGER NOT NULL CHECK(is_deleted IN (0, 1)),
    file_path TEXT,
    PRIMARY KEY (id, version)
)
""")

conn.commit()
conn.close()
print("Documents table created (if it didn't exist).")
