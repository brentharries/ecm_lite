import sqlite3
import uuid
from datetime import datetime

def add_document(title, author, department, classification, lifecycle_stage, file_path=None):
    conn = sqlite3.connect("ecm_lite_database.db")
    cursor = conn.cursor()
    upload_date = datetime.now().isoformat()
    is_deleted = 0

    # Check if document with this title already exists
    sql = "SELECT id, version FROM documents WHERE title = ? ORDER BY version DESC LIMIT 1"
    cursor.execute(sql, (title,))
    row = cursor.fetchone()

    if row:
        doc_id = row[0]
        version = row[1] + 1
    else:
        doc_id = str(uuid.uuid4())
        version = 1

    # Insert the document
    insSql = """
    INSERT INTO documents (id, version, title, author, upload_date, classification,
                           department, lifecycle_stage, is_deleted, file_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insSql, (doc_id, version, title, author, upload_date, classification,
                            department, lifecycle_stage, is_deleted, file_path))
    conn.commit()
    conn.close()

    return doc_id, version



def get_document(title, version=None):
    conn = sqlite3.connect("ecm_lite_database.db")
    cursor = conn.cursor()

    if version:
        sql = "SELECT * FROM documents WHERE title = ? AND version = ? AND is_deleted = 0"
        cursor.execute(sql, (title, version))
    else:
        sql = "SELECT * FROM documents WHERE title = ? AND is_deleted = 0 ORDER BY version DESC LIMIT 1"
        cursor.execute(sql, (title,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise Exception("Document not found or deleted")
    
    return row

def remove_documents(title, version=None):
    conn = sqlite3.connect("ecm_lite_database.db")
    cursor = conn.cursor()

    if version:
        sql = "UPDATE documents SET is_deleted = 1 WHERE title = ? AND version = ?"
        cursor.execute(sql, (title, version))
    else:
        # Delete the latest version
        sql = "UPDATE documents SET is_deleted = 1 WHERE title = ? ORDER BY version DESC LIMIT 1"
        # SQLite does not support LIMIT in UPDATE directly; workaround:
        cursor.execute("SELECT id, version FROM documents WHERE title = ? AND is_deleted = 0 ORDER BY version DESC LIMIT 1", (title,))
        row = cursor.fetchone()
        if row:
            cursor.execute("UPDATE documents SET is_deleted = 1 WHERE id = ? AND version = ?", (row[0], row[1]))
        else:
            conn.close()
            raise Exception("Document not found")

    conn.commit()
    conn.close()

def list_documents(author=None, department=None):
    conn = sqlite3.connect("ecm_lite_database.db")
    cursor = conn.cursor()

    sql = "SELECT id, version, title, author, department, classification, lifecycle_stage, upload_date FROM documents WHERE is_deleted = 0"
    params = []

    if author:
        sql += " AND author = ?"
        params.append(author)
    if department:
        sql += " AND department = ?"
        params.append(department)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    return rows
