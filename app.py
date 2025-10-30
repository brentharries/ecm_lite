from flask import Flask, request, jsonify, send_file, abort
import os
import uuid
from datetime import datetime
from ecm_functions import add_document, get_document, list_documents, remove_documents

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -------------------------|
# POST /documents - upload |
# -------------------------|
@app.route('/documents', methods=['POST'])
def upload_document():
    file = request.files.get('file')
    title = request.form.get('title')
    author = request.form.get('author')
    department = request.form.get('department')
    classification = request.form.get('classification')
    lifecycle_stage = int(request.form.get('lifecycle_stage', 0))

    if not all([file, title, author, department, classification]):
        return jsonify({"error": "Missing required fields"}), 400
    
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    doc_id, version = add_document(title, author, department, classification, lifecycle_stage, filepath)

    return jsonify({
        "id": doc_id,
        "version": version,
        "title": title
    }), 201


# ------------------------
# GET /documents/<title> - metadata
# ------------------------
@app.route('/documents/<title>', methods=['GET'])
def get_document_metadata(title):
    version = request.args.get('version')
    try:
        row = get_document(title, version)
        col_names = ["id", "version", "title", "author", "upload_date",
                     "classification", "department", "lifecycle_stage",
                     "is_deleted", "file_path"]
        return jsonify(dict(zip(col_names, row)))
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# ------------------------
# GET /documents/<title>/download
# ------------------------
@app.route('/documents/<title>/download', methods=['GET'])
def download_document(title):
    version = request.args.get('version')
    try:
        row = get_document(title, version)
        _, ver, _, _, _, _, _, _, _, filepath = row
        if not filepath or not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404

        ext = os.path.splitext(filepath)[1]
        download_name = f"{title}_v{ver}{ext}"
        return send_file(filepath, as_attachment=True, download_name=download_name)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# ------------------------
# GET /documents - list
# ------------------------
@app.route('/documents', methods=['GET'])
def list_docs():
    author = request.args.get('author')
    department = request.args.get('department')
    rows = list_documents(author, department)
    result = []
    for row in rows:
        doc_id, version, title, author, department, classification, lifecycle_stage, upload_date = row
        result.append({
            "id": doc_id,
            "version": version,
            "title": title,
            "author": author,
            "department": department,
            "classification": classification,
            "lifecycle_stage": lifecycle_stage,
            "upload_date": upload_date
        })
    return jsonify(result)

# ------------------------
# DELETE /documents/<title> - remove
# ------------------------
@app.route('/documents/<title>', methods=['DELETE'])
def delete_documents(title):
    version = request.args.get('version')
    try:
        remove_documents(title, version)
        return jsonify({"message": f"Document '{title}'" + (f" version {version}" if version else "") + " marked as deleted."})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# ------------------------
# Run server
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)