import sys
from ecm_functions import add_document, get_document, list_documents, remove_documents

def print_usage():
    print("Usage:")
    print("  python main.py add <title> <author> <department> <classification> <lifecycle_stage> [file_path]")
    print("  python main.py get <title> [version]")
    print("  python main.py list [author] [department]")
    print("  python main.py remove <title> [version]")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 7:
            print("Error: missing required arguments for add")
            print_usage()
            return
        
        title = sys.argv[2]
        author = sys.argv[3]
        department = sys.argv[4]
        classification = sys.argv[5]
        lifecycle_stage = int(sys.argv[6])
        file_path = sys.argv[7] if len(sys.argv) > 7 else None

        doc_id, version = add_document(title, author, department, classification, lifecycle_stage, file_path)
        print(f"Document added: I {doc_id} | Version: {version}")
        return
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("Error: Improper no# of arguments.")
            print_usage()
            return
        
        title = sys.argv[2]
        version = sys.argv[3] if len(sys.argv) == 4 else None

        try:
            row = get_document(title, version)
        except Exception as e:
            print(f"{e}")
            return

        col_names = ["id", "version", "title", "author", "upload_date",
                    "classification", "department", "lifecycle_stage",
                    "is_deleted", "file_path"]

        for col, value in zip(col_names, row):
            print(f"{col}: {value}")
        return

    elif command == "list":
        # list
        # python main.py list
        # python main.py list <author>
        # python main.py list <author> <department>

        author = None
        department = None

        if len(sys.argv) >= 3:
            author = sys.argv[2]
        if len(sys.argv) == 4:
            department = sys.argv[3]
        if len(sys.argv) > 4:
            print("Error: too many arguments for list")
            print_usage()
            return

        rows = list_documents(author, department)

        if not rows:
            print("No documents match the given filters.")
            return

        # Nice formatted display
        for row in rows:
            doc_id, version, title, author, department, classification, lifecycle_stage, upload_date = row
            print(f"{title} (v{version})")
            print(f"  ID: {doc_id}")
            print(f"  Author: {author}")
            print(f"  Department: {department}")
            print(f"  Classification: {classification}")
            print(f"  Stage: {lifecycle_stage}")
            print(f"  Uploaded: {upload_date}")
            print("-" * 40)

        return

    elif command == "remove":
        # remove
        # python main.py remove <title>
        # python main.py remove <title> <version>

        if len(sys.argv) < 3:
            print("Error: missing title for remove")
            print_usage()
            return

        title = sys.argv[2]
        version = None

        if len(sys.argv) == 4:
            version = sys.argv[3]
        elif len(sys.argv) > 4:
            print("Error: too many arguments for remove")
            print_usage()
            return

        try:
            remove_document(title, version)
            if version:
                print(f"Document '{title}' version {version} marked as deleted.")
            else:
                print(f"Latest version of '{title}' marked as deleted.")
        except Exception as e:
            print(f"Error: {str(e)}")

        return

    else:
        print_usage()

if __name__ == "__main__":
    main()
