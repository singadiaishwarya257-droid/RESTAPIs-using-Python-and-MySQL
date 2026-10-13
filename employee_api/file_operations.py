# file_operations.py - File Handling Operations
# This module handles text, CSV, JSON file operations and file uploads/downloads
# Functions for creating, reading, writing, appending, deleting files and data import/export

import os
import shutil
import csv
import json
from pathlib import Path
from datetime import datetime

# Configuration
UPLOADS_DIR = "uploads"
REPORTS_DIR = "reports"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Ensure directories exist
Path(UPLOADS_DIR).mkdir(exist_ok=True)
Path(REPORTS_DIR).mkdir(exist_ok=True)

# ============================================================================
# TEXT FILE OPERATIONS
# ============================================================================

def create_text_file(filename, content=""):
    """
    Creates a new text file with optional initial content.
    
    Args:
        filename (str): Name of file to create (in uploads/)
        content (str): Initial content to write
        
    Returns:
        dict: {"success": True/False, "path": "...", "message": "..."}
        
    Example:
        result = create_text_file("notes.txt", "Hello World")
    """
    try:
        if not filename or len(filename) == 0:
            return {"success": False, "error": "Filename cannot be empty"}
        
        # Security: prevent directory traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            return {"success": False, "error": "File already exists"}
        
        # Create file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "path": filepath,
            "message": f"File '{filename}' created successfully"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error creating file: {str(e)}"}

def write_text_file(filename, content):
    """
    Writes content to a text file (overwrites if exists).
    
    Args:
        filename (str): Name of file to write
        content (str): Content to write
        
    Returns:
        dict: {"success": True/False, "message": "..."}
        
    Example:
        result = write_text_file("data.txt", "New content")
    """
    try:
        if not filename or not isinstance(content, str):
            return {"success": False, "error": "Invalid filename or content"}
        
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {"success": True, "message": f"Content written to '{filename}'"}
        
    except Exception as e:
        return {"success": False, "error": f"Error writing file: {str(e)}"}

def append_text_file(filename, content):
    """
    Appends content to an existing text file.
    
    Args:
        filename (str): Name of file to append to
        content (str): Content to append
        
    Returns:
        dict: {"success": True/False, "message": "..."}
        
    Example:
        result = append_text_file("log.txt", "New log entry")
    """
    try:
        if not filename or not isinstance(content, str):
            return {"success": False, "error": "Invalid filename or content"}
        
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        if not os.path.exists(filepath):
            return {"success": False, "error": "File does not exist"}
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content)
        
        return {"success": True, "message": f"Content appended to '{filename}'"}
        
    except Exception as e:
        return {"success": False, "error": f"Error appending to file: {str(e)}"}

def read_text_file(filename):
    """
    Reads complete content of a text file.
    
    Args:
        filename (str): Name of file to read
        
    Returns:
        dict: {"success": True/False, "content": "...", "message": "..."}
        
    Example:
        result = read_text_file("data.txt")
        if result["success"]:
            print(result["content"])
    """
    try:
        if not filename:
            return {"success": False, "error": "Filename cannot be empty"}
        
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        if not os.path.exists(filepath):
            return {"success": False, "error": "File does not exist"}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {"success": True, "content": content}
        
    except Exception as e:
        return {"success": False, "error": f"Error reading file: {str(e)}"}

def read_text_file_lines(filename):
    """
    Reads a text file line by line.
    
    Args:
        filename (str): Name of file to read
        
    Returns:
        dict: {"success": True/False, "lines": [...], "line_count": N}
        
    Example:
        result = read_text_file_lines("log.txt")
        for line in result["lines"]:
            print(line)
    """
    try:
        if not filename:
            return {"success": False, "error": "Filename cannot be empty"}
        
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        if not os.path.exists(filepath):
            return {"success": False, "error": "File does not exist"}
        
        lines = []
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        return {
            "success": True,
            "lines": lines,
            "line_count": len(lines)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error reading file: {str(e)}"}

def file_exists(filename):
    """
    Checks if a file exists.
    
    Args:
        filename (str): Name of file to check
        
    Returns:
        dict: {"exists": True/False, "path": "..."}
        
    Example:
        result = file_exists("data.txt")
    """
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"exists": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        exists = os.path.exists(filepath)
        
        return {"exists": exists, "path": filepath if exists else None}
        
    except Exception as e:
        return {"exists": False, "error": str(e)}

def get_file_size(filename):
    """
    Gets the size of a file in bytes.
    
    Args:
        filename (str): Name of file
        
    Returns:
        dict: {"success": True/False, "size_bytes": N, "size_kb": X.XX}
        
    Example:
        result = get_file_size("data.txt")
        print(f"File size: {result['size_kb']} KB")
    """
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        if not os.path.exists(filepath):
            return {"success": False, "error": "File does not exist"}
        
        size_bytes = os.path.getsize(filepath)
        size_kb = size_bytes / 1024
        
        return {
            "success": True,
            "size_bytes": size_bytes,
            "size_kb": round(size_kb, 2)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_file(filename):
    """
    Safely deletes a file.
    
    Args:
        filename (str): Name of file to delete
        
    Returns:
        dict: {"success": True/False, "message": "..."}
        
    Example:
        result = delete_file("old_data.txt")
    """
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        if not os.path.exists(filepath):
            return {"success": False, "error": "File does not exist"}
        
        os.remove(filepath)
        
        return {"success": True, "message": f"File '{filename}' deleted successfully"}
        
    except Exception as e:
        return {"success": False, "error": f"Error deleting file: {str(e)}"}

def rename_file(old_filename, new_filename):
    """
    Renames a file.
    
    Args:
        old_filename (str): Current filename
        new_filename (str): New filename
        
    Returns:
        dict: {"success": True/False, "message": "..."}
        
    Example:
        result = rename_file("old.txt", "new.txt")
    """
    try:
        if ".." in old_filename or "/" in old_filename or "\\" in old_filename:
            return {"success": False, "error": "Invalid old filename"}
        if ".." in new_filename or "/" in new_filename or "\\" in new_filename:
            return {"success": False, "error": "Invalid new filename"}
        
        old_path = os.path.join(UPLOADS_DIR, old_filename)
        new_path = os.path.join(UPLOADS_DIR, new_filename)
        
        if not os.path.exists(old_path):
            return {"success": False, "error": "Source file does not exist"}
        
        if os.path.exists(new_path):
            return {"success": False, "error": "Destination file already exists"}
        
        os.rename(old_path, new_path)
        
        return {
            "success": True,
            "message": f"File renamed from '{old_filename}' to '{new_filename}'"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def copy_file(source_filename, dest_filename):
    """
    Copies a file.
    
    Args:
        source_filename (str): File to copy from
        dest_filename (str): File to copy to
        
    Returns:
        dict: {"success": True/False, "message": "..."}
        
    Example:
        result = copy_file("original.txt", "backup.txt")
    """
    try:
        if ".." in source_filename or "/" in source_filename or "\\" in source_filename:
            return {"success": False, "error": "Invalid source filename"}
        if ".." in dest_filename or "/" in dest_filename or "\\" in dest_filename:
            return {"success": False, "error": "Invalid destination filename"}
        
        source_path = os.path.join(UPLOADS_DIR, source_filename)
        dest_path = os.path.join(UPLOADS_DIR, dest_filename)
        
        if not os.path.exists(source_path):
            return {"success": False, "error": "Source file does not exist"}
        
        if os.path.exists(dest_path):
            return {"success": False, "error": "Destination file already exists"}
        
        shutil.copy2(source_path, dest_path)
        
        return {
            "success": True,
            "message": f"File copied from '{source_filename}' to '{dest_filename}'"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============================================================================
# CSV FILE OPERATIONS
# ============================================================================

def read_csv_file(filename):
    """
    Reads a CSV file and returns all rows.
    
    Args:
        filename (str): Name of CSV file to read
        
    Returns:
        dict: {"success": True/False, "data": [...], "row_count": N}
        
    Example:
        result = read_csv_file("employees.csv")
        for row in result["data"]:
            print(row)
    """
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        if not os.path.exists(filepath):
            return {"success": False, "error": "File does not exist"}
        
        if not filename.lower().endswith('.csv'):
            return {"success": False, "error": "File must be a CSV file"}
        
        rows = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        
        return {
            "success": True,
            "data": rows,
            "row_count": len(rows)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error reading CSV: {str(e)}"}

def write_csv_file(filename, headers, rows):
    """
    Writes data to a CSV file.
    
    Args:
        filename (str): Name of CSV file to create
        headers (list): Column headers
        rows (list): List of dictionaries with row data
        
    Returns:
        dict: {"success": True/False, "message": "..."}
        
    Example:
        headers = ["id", "name", "email", "department", "salary"]
        rows = [
            {"id": 1, "name": "John", "email": "john@co.com", ...},
            {"id": 2, "name": "Jane", "email": "jane@co.com", ...}
        ]
        result = write_csv_file("employees.csv", headers, rows)
    """
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        if not filename.lower().endswith('.csv'):
            filename += '.csv'
        
        filepath = os.path.join(REPORTS_DIR, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        
        return {
            "success": True,
            "path": filepath,
            "message": f"CSV file '{filename}' created with {len(rows)} rows"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error writing CSV: {str(e)}"}

# ============================================================================
# JSON FILE OPERATIONS
# ============================================================================

def read_json_file(filename):
    """
    Reads a JSON file and returns parsed data.
    
    Args:
        filename (str): Name of JSON file
        
    Returns:
        dict: {"success": True/False, "data": {...} or [...], "message": "..."}
        
    Example:
        result = read_json_file("config.json")
        if result["success"]:
            data = result["data"]
    """
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        if not os.path.exists(filepath):
            return {"success": False, "error": "File does not exist"}
        
        if not filename.lower().endswith('.json'):
            return {"success": False, "error": "File must be a JSON file"}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {"success": True, "data": data}
        
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid JSON format"}
    except Exception as e:
        return {"success": False, "error": f"Error reading JSON: {str(e)}"}

def write_json_file(filename, data):
    """
    Writes data to a JSON file.
    
    Args:
        filename (str): Name of JSON file
        data (dict or list): Data to write
        
    Returns:
        dict: {"success": True/False, "path": "...", "message": "..."}
        
    Example:
        data = {
            "employees": [
                {"id": 1, "name": "John", "salary": 50000},
                {"id": 2, "name": "Jane", "salary": 55000}
            ]
        }
        result = write_json_file("employees.json", data)
    """
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return {"success": False, "error": "Invalid filename"}
        
        if not filename.lower().endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(REPORTS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        return {
            "success": True,
            "path": filepath,
            "message": f"JSON file '{filename}' created successfully"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error writing JSON: {str(e)}"}

# ============================================================================
# FILE UPLOAD/DOWNLOAD UTILITIES
# ============================================================================

def validate_upload_file(filename, file_size, allowed_extensions=None):
    """
    Validates uploaded file extension and size.
    
    Args:
        filename (str): Name of uploaded file
        file_size (int): Size of file in bytes
        allowed_extensions (list): List of allowed extensions (e.g., ['txt', 'csv', 'json'])
        
    Returns:
        dict: {"valid": True/False, "error": "..."}
        
    Example:
        validation = validate_upload_file("data.csv", 5000, ['csv', 'txt'])
    """
    if allowed_extensions is None:
        allowed_extensions = ['txt', 'csv', 'json']
    
    try:
        # Check file size
        if file_size > MAX_FILE_SIZE:
            return {
                "valid": False,
                "error": f"File size exceeds maximum of {MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
            }
        
        # Check extension
        file_ext = filename.rsplit('.', 1)[-1].lower()
        if file_ext not in allowed_extensions:
            return {
                "valid": False,
                "error": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            }
        
        return {"valid": True}
        
    except Exception as e:
        return {"valid": False, "error": str(e)}

def list_uploaded_files():
    """
    Lists all uploaded files.
    
    Returns:
        dict: {"success": True, "files": [...], "count": N}
    """
    try:
        files = []
        for filename in os.listdir(UPLOADS_DIR):
            filepath = os.path.join(UPLOADS_DIR, filename)
            if os.path.isfile(filepath):
                files.append({
                    "name": filename,
                    "size_bytes": os.path.getsize(filepath),
                    "size_kb": round(os.path.getsize(filepath) / 1024, 2)
                })
        
        return {"success": True, "files": files, "count": len(files)}
        
    except Exception as e:
        return {"success": False, "error": str(e)}
