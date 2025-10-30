import requests
import os

BASE_URL = "http://127.0.0.1:5000"

def test_upload(file_path, title, author, department, classification, lifecycle_stage):
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {
            "title": title,
            "author": author,
            "department": department,
            "classification": classification,
            "lifecycle_stage": lifecycle_stage
        }
        r = requests.post(f"{BASE_URL}/documents", files=files, data=data)
    print("UPLOAD:", r.status_code, r.json())
    return r.json()

def test_get(title, version=None):
    params = {"version": version} if version else {}
    r = requests.get(f"{BASE_URL}/documents/{title}", params=params)
    print("GET:", r.status_code, r.json())
    return r.json()

def test_download(title, version=None):
    params = {"version": version} if version else {}
    r = requests.get(f"{BASE_URL}/documents/{title}/download", params=params)
    if r.status_code == 200:
        ext = ".pdf"  # adjust if your test file has different extension
        download_name = f"{title}_v{version or 'latest'}{ext}"
        with open(download_name, "wb") as f:
            f.write(r.content)
        print(f"Downloaded file as {download_name}")
    else:
        print("DOWNLOAD:", r.status_code, r.json())

def test_list(author=None, department=None):
    params = {}
    if author: params["author"] = author
    if department: params["department"] = department
    r = requests.get(f"{BASE_URL}/documents", params=params)
    print("LIST:", r.status_code, r.json())
    return r.json()

def test_delete(title, version=None):
    params = {"version": version} if version else {}
    r = requests.delete(f"{BASE_URL}/documents/{title}", params=params)
    print("DELETE:", r.status_code, r.json())

# --------------------
# Run all tests
# --------------------
if __name__ == "__main__":
    test_file = "handbook.pdf"  # make sure this exists
    title = "Employee Handbook"
    author = "Alice"
    department = "HR"
    classification = "public"
    lifecycle_stage = 0

    # 1. Upload
    upload_info = test_upload(test_file, title, author, department, classification, lifecycle_stage)

    # 2. Get metadata
    test_get(title)
    test_get(title, version=upload_info["version"])

    # 3. Download
    test_download(title)
    test_download(title, version=upload_info["version"])

    # 4. List documents
    test_list()
    test_list(author="Alice")
    test_list(department="HR")

    # 5. Delete document
    test_delete(title)
    test_delete(title, version=upload_info["version"])
