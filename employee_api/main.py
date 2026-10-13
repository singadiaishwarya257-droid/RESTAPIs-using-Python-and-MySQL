# main.py - FastAPI Application Entry Point
# This file contains all REST API endpoints for employee management and file operations
# Includes CRUD operations, file handling, CSV/JSON import-export, and file uploads

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

# Import our modules
import database
import employee_queries
import file_operations

# ============================================================================
# FastAPI Application Setup
# ============================================================================

app = FastAPI(
    title="Employee Management REST API",
    description="Complete REST API for managing employees, files, and data import/export",
    version="1.0.0"
)

# Mount static directories for file downloads
Path("uploads").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/", tags=["Health Check"])
def read_root():
    """
    Welcome endpoint - returns API information.
    
    Returns:
        JSON with API name, version, and available endpoints
    """
    return {
        "message": "Welcome to Employee Management REST API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
        "endpoints": {
            "employees": "/employees",
            "files": "/files/text",
            "csv": "/files/csv",
            "json": "/files/json"
        }
    }

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint - verifies database connection.
    
    Returns:
        JSON with health status and database connection info
    """
    is_healthy = database.test_connection()
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "database": "connected" if is_healthy else "disconnected"
    }

# ============================================================================
# EMPLOYEE CRUD ENDPOINTS
# ============================================================================

@app.post("/employees", tags=["Employees"])
def create_employee(
    name: str,
    email: str,
    department: str,
    salary: float
):
    """
    Create a new employee.
    
    Args:
        name: Employee's full name
        email: Employee's email (must be unique)
        department: Department name
        salary: Annual salary
        
    Returns:
        JSON with success status and employee ID
        
    Example:
        POST /employees?name=John%20Doe&email=john@company.com&department=IT&salary=75000
    """
    try:
        result = employee_queries.add_employee(name, email, department, salary)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "id": result["id"],
                "status_code": 201
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/employees", tags=["Employees"])
def get_all_employees():
    """
    Retrieve all employees.
    
    Returns:
        JSON array with all employee records
        
    Example:
        GET /employees
    """
    try:
        employees = employee_queries.get_all_employees()
        return {
            "success": True,
            "count": len(employees),
            "data": employees
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/employees/{employee_id}", tags=["Employees"])
def get_employee(employee_id: int):
    """
    Retrieve a single employee by ID.
    
    Args:
        employee_id: The ID of the employee
        
    Returns:
        JSON with employee data
        
    Example:
        GET /employees/1
    """
    try:
        result = employee_queries.get_employee_by_id(employee_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return {"success": True, "data": result}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.put("/employees/{employee_id}", tags=["Employees"])
def update_employee(employee_id: int, **kwargs):
    """
    Update employee details.
    
    Args:
        employee_id: The ID of the employee
        name: (optional) New name
        email: (optional) New email
        department: (optional) New department
        salary: (optional) New salary
        
    Returns:
        JSON with success status
        
    Example:
        PUT /employees/1?name=Jane%20Doe&salary=80000
    """
    try:
        # Extract query parameters manually
        result = employee_queries.update_employee(employee_id, **kwargs)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "status_code": 200
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(employee_id: int):
    """
    Delete an employee.
    
    Args:
        employee_id: The ID of the employee to delete
        
    Returns:
        JSON with success status
        
    Example:
        DELETE /employees/5
    """
    try:
        result = employee_queries.delete_employee(employee_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "status_code": 200
            }
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/employees/search/{search_type}", tags=["Employees"])
def search_employees(search_type: str, value: str):
    """
    Search employees by name or department.
    
    Args:
        search_type: "name" or "department"
        value: Search term
        
    Returns:
        JSON array with matching employees
        
    Example:
        GET /employees/search/name?value=John
        GET /employees/search/department?value=IT
    """
    try:
        if search_type not in ["name", "department"]:
            raise HTTPException(status_code=400, detail="search_type must be 'name' or 'department'")
        
        results = employee_queries.search_employees(search_type, value)
        
        return {
            "success": True,
            "search_type": search_type,
            "search_value": value,
            "count": len(results),
            "data": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/employees/stats/summary", tags=["Employees"])
def get_employee_stats():
    """
    Get employee statistics.
    
    Returns:
        JSON with total count and salary statistics
        
    Example:
        GET /employees/stats/summary
    """
    try:
        count = employee_queries.get_employee_count()
        stats = employee_queries.get_salary_statistics()
        
        return {
            "success": True,
            "total_employees": count,
            "salary_statistics": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# ============================================================================
# TEXT FILE OPERATIONS ENDPOINTS
# ============================================================================

@app.post("/files/text/create", tags=["Text Files"])
def create_text_file(filename: str, content: str = ""):
    """
    Create a new text file.
    
    Args:
        filename: Name of file to create
        content: Initial content (optional)
        
    Example:
        POST /files/text/create?filename=notes.txt&content=Hello
    """
    try:
        result = file_operations.create_text_file(filename, content)
        
        if result["success"]:
            return {"success": True, "message": result["message"], "path": result["path"]}
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/files/text/write", tags=["Text Files"])
def write_text_file(filename: str, content: str):
    """
    Write content to a text file (overwrites).
    
    Args:
        filename: Name of file
        content: Content to write
        
    Example:
        POST /files/text/write?filename=data.txt&content=New%20content
    """
    try:
        result = file_operations.write_text_file(filename, content)
        
        if result["success"]:
            return {"success": True, "message": result["message"]}
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/files/text/append", tags=["Text Files"])
def append_text_file(filename: str, content: str):
    """
    Append content to a text file.
    
    Args:
        filename: Name of file
        content: Content to append
        
    Example:
        POST /files/text/append?filename=log.txt&content=New%20line
    """
    try:
        result = file_operations.append_text_file(filename, content)
        
        if result["success"]:
            return {"success": True, "message": result["message"]}
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/files/text/read/{filename}", tags=["Text Files"])
def read_text_file(filename: str):
    """
    Read complete content of a text file.
    
    Args:
        filename: Name of file to read
        
    Example:
        GET /files/text/read/data.txt
    """
    try:
        result = file_operations.read_text_file(filename)
        
        if result["success"]:
            return {"success": True, "content": result["content"]}
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/files/text/lines/{filename}", tags=["Text Files"])
def read_text_file_lines(filename: str):
    """
    Read a text file line by line.
    
    Args:
        filename: Name of file to read
        
    Example:
        GET /files/text/lines/log.txt
    """
    try:
        result = file_operations.read_text_file_lines(filename)
        
        if result["success"]:
            return {
                "success": True,
                "line_count": result["line_count"],
                "lines": result["lines"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/files/text/exists/{filename}", tags=["Text Files"])
def check_file_exists(filename: str):
    """
    Check if a file exists.
    
    Args:
        filename: Name of file to check
        
    Example:
        GET /files/text/exists/data.txt
    """
    try:
        result = file_operations.file_exists(filename)
        return {"exists": result["exists"], "path": result.get("path")}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/files/text/size/{filename}", tags=["Text Files"])
def get_text_file_size(filename: str):
    """
    Get the size of a file.
    
    Args:
        filename: Name of file
        
    Example:
        GET /files/text/size/data.txt
    """
    try:
        result = file_operations.get_file_size(filename)
        
        if result["success"]:
            return {
                "success": True,
                "size_bytes": result["size_bytes"],
                "size_kb": result["size_kb"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.delete("/files/text/{filename}", tags=["Text Files"])
def delete_text_file(filename: str):
    """
    Delete a text file.
    
    Args:
        filename: Name of file to delete
        
    Example:
        DELETE /files/text/old_data.txt
    """
    try:
        result = file_operations.delete_file(filename)
        
        if result["success"]:
            return {"success": True, "message": result["message"]}
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/files/text/rename", tags=["Text Files"])
def rename_text_file(old_filename: str, new_filename: str):
    """
    Rename a text file.
    
    Args:
        old_filename: Current filename
        new_filename: New filename
        
    Example:
        POST /files/text/rename?old_filename=old.txt&new_filename=new.txt
    """
    try:
        result = file_operations.rename_file(old_filename, new_filename)
        
        if result["success"]:
            return {"success": True, "message": result["message"]}
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/files/text/copy", tags=["Text Files"])
def copy_text_file(source_filename: str, dest_filename: str):
    """
    Copy a text file.
    
    Args:
        source_filename: File to copy from
        dest_filename: File to copy to
        
    Example:
        POST /files/text/copy?source_filename=original.txt&dest_filename=backup.txt
    """
    try:
        result = file_operations.copy_file(source_filename, dest_filename)
        
        if result["success"]:
            return {"success": True, "message": result["message"]}
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# ============================================================================
# CSV FILE OPERATIONS
# ============================================================================

@app.get("/files/csv/read/{filename}", tags=["CSV Files"])
def read_csv_file(filename: str):
    """
    Read and parse a CSV file.
    
    Args:
        filename: Name of CSV file
        
    Example:
        GET /files/csv/read/employees.csv
    """
    try:
        result = file_operations.read_csv_file(filename)
        
        if result["success"]:
            return {
                "success": True,
                "row_count": result["row_count"],
                "data": result["data"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/files/csv/import", tags=["CSV Files"])
def import_csv_to_database(filename: str):
    """
    Import employees from a CSV file to database.
    
    CSV must have columns: name, email, department, salary
    
    Args:
        filename: Name of CSV file to import
        
    Returns:
        JSON with import results
        
    Example:
        POST /files/csv/import?filename=employees.csv
    """
    try:
        # Read CSV file
        read_result = file_operations.read_csv_file(filename)
        
        if not read_result["success"]:
            raise HTTPException(status_code=404, detail=read_result["error"])
        
        csv_data = read_result["data"]
        imported_count = 0
        failed_count = 0
        errors = []
        
        # Import each row
        for idx, row in enumerate(csv_data, 1):
            try:
                # Validate required fields
                if not all(k in row for k in ["name", "email", "department", "salary"]):
                    failed_count += 1
                    errors.append(f"Row {idx}: Missing required fields")
                    continue
                
                # Try to import
                result = employee_queries.add_employee(
                    name=row["name"],
                    email=row["email"],
                    department=row["department"],
                    salary=float(row["salary"])
                )
                
                if result["success"]:
                    imported_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Row {idx}: {result['error']}")
                    
            except ValueError:
                failed_count += 1
                errors.append(f"Row {idx}: Invalid salary value")
            except Exception as e:
                failed_count += 1
                errors.append(f"Row {idx}: {str(e)}")
        
        return {
            "success": True,
            "total_rows": len(csv_data),
            "imported": imported_count,
            "failed": failed_count,
            "errors": errors if errors else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/files/csv/export", tags=["CSV Files"])
def export_employees_to_csv(filename: str = "employees_export.csv"):
    """
    Export all employees to a CSV file.
    
    Args:
        filename: Name of output CSV file
        
    Returns:
        JSON with export status and file path
        
    Example:
        POST /files/csv/export?filename=employees_export.csv
    """
    try:
        employees = employee_queries.get_all_employees()
        
        if not employees:
            raise HTTPException(status_code=404, detail="No employees to export")
        
        headers = ["id", "name", "email", "department", "salary", "created_at", "updated_at"]
        
        result = file_operations.write_csv_file(filename, headers, employees)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "path": result["path"],
                "row_count": len(employees)
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# ============================================================================
# JSON FILE OPERATIONS
# ============================================================================

@app.get("/files/json/read/{filename}", tags=["JSON Files"])
def read_json_file(filename: str):
    """
    Read and parse a JSON file.
    
    Args:
        filename: Name of JSON file
        
    Example:
        GET /files/json/read/data.json
    """
    try:
        result = file_operations.read_json_file(filename)
        
        if result["success"]:
            return {"success": True, "data": result["data"]}
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/files/json/import", tags=["JSON Files"])
def import_json_to_database(filename: str):
    """
    Import employees from a JSON file to database.
    
    JSON should be array of objects with: name, email, department, salary
    
    Args:
        filename: Name of JSON file to import
        
    Returns:
        JSON with import results
        
    Example:
        POST /files/json/import?filename=employees.json
    """
    try:
        # Read JSON file
        read_result = file_operations.read_json_file(filename)
        
        if not read_result["success"]:
            raise HTTPException(status_code=404, detail=read_result["error"])
        
        json_data = read_result["data"]
        
        # Ensure it's a list
        if not isinstance(json_data, list):
            if isinstance(json_data, dict) and "employees" in json_data:
                json_data = json_data["employees"]
            else:
                raise HTTPException(status_code=400, detail="JSON must be array of employees")
        
        imported_count = 0
        failed_count = 0
        errors = []
        
        # Import each employee
        for idx, emp in enumerate(json_data, 1):
            try:
                # Validate required fields
                if not all(k in emp for k in ["name", "email", "department", "salary"]):
                    failed_count += 1
                    errors.append(f"Item {idx}: Missing required fields")
                    continue
                
                # Try to import
                result = employee_queries.add_employee(
                    name=emp["name"],
                    email=emp["email"],
                    department=emp["department"],
                    salary=float(emp["salary"])
                )
                
                if result["success"]:
                    imported_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Item {idx}: {result['error']}")
                    
            except ValueError:
                failed_count += 1
                errors.append(f"Item {idx}: Invalid salary value")
            except Exception as e:
                failed_count += 1
                errors.append(f"Item {idx}: {str(e)}")
        
        return {
            "success": True,
            "total_items": len(json_data),
            "imported": imported_count,
            "failed": failed_count,
            "errors": errors if errors else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/files/json/export", tags=["JSON Files"])
def export_employees_to_json(filename: str = "employees_export.json"):
    """
    Export all employees to a JSON file.
    
    Args:
        filename: Name of output JSON file
        
    Returns:
        JSON with export status and file path
        
    Example:
        POST /files/json/export?filename=employees_export.json
    """
    try:
        employees = employee_queries.get_all_employees()
        
        if not employees:
            raise HTTPException(status_code=404, detail="No employees to export")
        
        data = {"employees": employees, "export_count": len(employees)}
        
        result = file_operations.write_json_file(filename, data)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "path": result["path"],
                "export_count": len(employees)
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# ============================================================================
# FILE UPLOAD/DOWNLOAD ENDPOINTS
# ============================================================================

@app.post("/files/upload", tags=["File Upload/Download"])
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file (text, CSV, or JSON).
    
    Args:
        file: File to upload
        
    Returns:
        JSON with upload status and file info
        
    Validation:
        - Allowed extensions: txt, csv, json
        - Max file size: 10 MB
    """
    try:
        # Get file size
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validate file
        validation = file_operations.validate_upload_file(
            file.filename, file_size, ['txt', 'csv', 'json']
        )
        
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["error"])
        
        # Save file
        filepath = os.path.join("uploads", file.filename)
        with open(filepath, "wb") as f:
            f.write(file_content)
        
        return {
            "success": True,
            "filename": file.filename,
            "size_bytes": file_size,
            "size_kb": round(file_size / 1024, 2),
            "path": filepath
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/files/download/{filename}", tags=["File Upload/Download"])
def download_file(filename: str):
    """
    Download a file from uploads folder.
    
    Args:
        filename: Name of file to download
        
    Returns:
        File content as download
        
    Example:
        GET /files/download/data.csv
    """
    try:
        # Security check
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        filepath = os.path.join("uploads", filename)
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(filepath, filename=filename)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/files/report-download/{filename}", tags=["File Upload/Download"])
def download_report(filename: str):
    """
    Download a generated report (CSV or JSON).
    
    Args:
        filename: Name of report file to download
        
    Returns:
        File content as download
        
    Example:
        GET /files/report-download/employees_export.csv
    """
    try:
        # Security check
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        filepath = os.path.join("reports", filename)
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Report not found")
        
        return FileResponse(filepath, filename=filename)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/files/list", tags=["File Upload/Download"])
def list_files():
    """
    List all uploaded files.
    
    Returns:
        JSON array with file information
        
    Example:
        GET /files/list
    """
    try:
        result = file_operations.list_uploaded_files()
        
        if result["success"]:
            return {
                "success": True,
                "count": result["count"],
                "files": result["files"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all exception handler."""
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🚀 Employee Management REST API")
    print("=" * 70)
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Alternative Docs: http://localhost:8000/redoc")
    print("=" * 70)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
