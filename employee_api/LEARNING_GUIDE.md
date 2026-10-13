# Employee Management REST API - Learning Guide

Complete learning resource with interview questions, practice tasks, and concept explanations.

---

## 🎓 Interview Questions & Answers

### PART 1: REST API Concepts

#### Q1: What is a REST API and what do the HTTP methods do?

**Answer:**

REST (Representational State Transfer) is an architectural style for web APIs that uses standard HTTP methods:

- **GET** - Retrieve/read data (idempotent, safe)
  - Example: `GET /employees` → returns list of employees
  - Safe: Doesn't modify data
  - Idempotent: Calling multiple times gives same result

- **POST** - Create new data
  - Example: `POST /employees` with name, email, etc. → creates new employee
  - Not idempotent: Each call creates new record
  - Not safe: Modifies data

- **PUT** - Update existing data
  - Example: `PUT /employees/1` → updates employee with ID 1
  - Idempotent: Multiple calls have same effect
  - Complete replacement of resource

- **DELETE** - Remove data
  - Example: `DELETE /employees/5` → deletes employee with ID 5
  - Idempotent: Calling again returns 404
  - Removes resource permanently

**Example REST API Call:**
```bash
# GET - Retrieve all employees
curl http://localhost:8000/employees

# POST - Create new employee
curl -X POST "http://localhost:8000/employees?name=John&email=john@co.com&department=IT&salary=75000"

# PUT - Update employee salary
curl -X PUT "http://localhost:8000/employees/1?salary=80000"

# DELETE - Remove employee
curl -X DELETE "http://localhost:8000/employees/1"
```

**Key Concepts:**
- Stateless: Each request is independent
- Client-Server: Separate concerns
- Cacheable: GET requests can be cached
- Uniform interface: Consistent endpoint structure

---

#### Q2: Explain HTTP status codes and when to use them.

**Answer:**

HTTP status codes indicate the result of an API request:

**2xx - Success (Request successful)**
- `200 OK` - Request succeeded, data returned
  - Usage: GET /employees (returns list)
  - Meaning: Success, no resource created

- `201 Created` - Resource successfully created
  - Usage: POST /employees (new employee added)
  - Meaning: Success + new resource created
  - Should return URL of new resource

**3xx - Redirection (Further action needed)**
- `301 Moved Permanently` - Resource moved permanently
- `302 Found` - Temporary redirect
- Usage: Not common in APIs, more for web pages

**4xx - Client Error (Request problem)**
- `400 Bad Request` - Invalid request data
  - Example: Missing required parameter
  - Fix: Check request parameters

- `401 Unauthorized` - Authentication required
  - Example: No API key provided
  - Fix: Provide authentication token

- `403 Forbidden` - Authenticated but no permission
  - Example: User lacks admin role
  - Fix: Use account with proper permissions

- `404 Not Found` - Resource doesn't exist
  - Example: GET /employees/999 (employee doesn't exist)
  - Fix: Check if resource exists before accessing

- `409 Conflict` - Request conflicts with current state
  - Example: POST /employees with duplicate email
  - Fix: Check for duplicates first

**5xx - Server Error (Server problem)**
- `500 Internal Server Error` - Unexpected server error
  - Example: Database connection failed
  - Fix: Check server logs, restart service

- `503 Service Unavailable` - Server temporarily unavailable
  - Example: Server maintenance
  - Fix: Retry later

**Status Code Map for Our API:**

```python
# Employee operations
POST /employees
  → 201 Created (success)
  → 400 Bad Request (invalid data)
  → 409 Conflict (duplicate email)

GET /employees/1
  → 200 OK (found)
  → 404 Not Found (employee doesn't exist)

PUT /employees/1
  → 200 OK (updated)
  → 404 Not Found (employee doesn't exist)

DELETE /employees/1
  → 200 OK (deleted)
  → 404 Not Found (already deleted)
```

---

#### Q3: What is the difference between authentication and authorization?

**Answer:**

**Authentication** - Verifying WHO you are
- Question: "Who are you?"
- Process: Checking credentials
- Example: Login with username/password
- Result: You prove identity
- Token: JWT token issued after login

**Authorization** - Verifying WHAT you can do
- Question: "What can you access?"
- Process: Checking permissions
- Example: Admin can delete, user cannot
- Result: You get specific permissions
- Rule: Only admins can DELETE /employees

**Real-World Example:**

```
1. Authentication:
   - User enters username: "john@company.com"
   - User enters password: "secure123"
   - API validates credentials
   - Result: ✅ You are John (authenticated)
   - API issues JWT token

2. Authorization:
   - User tries to DELETE /employees/1
   - API checks user role in database
   - John is "USER" role (not admin)
   - Result: ❌ Denied (not authorized)
   - Response: 403 Forbidden

3. Admin case:
   - Admin tries to DELETE /employees/1
   - Admin is "ADMIN" role
   - Result: ✅ Allowed (authorized)
   - Employee deleted successfully
```

**In Our Current API:**
- We don't implement authentication yet (all endpoints public)
- Next step: Add JWT token authentication
- Then: Add role-based authorization

---

### PART 2: Database Concepts

#### Q4: Explain primary keys, unique constraints, and indexes.

**Answer:**

**Primary Key**
- Purpose: Uniquely identify each row
- Characteristics:
  - Must be unique (no duplicates)
  - Cannot be NULL
  - Only one per table
  - Automatically indexed
- Example in our table:
  ```sql
  id INT AUTO_INCREMENT PRIMARY KEY
  ```
- Why: Fast lookups, data integrity, relationships

**Unique Constraint**
- Purpose: Prevent duplicate values in specific column
- Characteristics:
  - Must be unique (no duplicates)
  - Can be NULL (multiple NULLs allowed)
  - Multiple per table possible
  - Automatically indexed
- Example in our table:
  ```sql
  email VARCHAR(100) UNIQUE NOT NULL
  ```
- Why: Prevent duplicate emails, business rule enforcement

**Index**
- Purpose: Speed up queries
- How it works: Like book index - jumps to location instead of reading all pages
- Characteristics:
  - Faster searches
  - Slower inserts (must update index)
  - Consumes storage
  - Automatically created for PRIMARY KEY and UNIQUE
- Performance impact:
  ```
  Without index: Check all 1,000,000 rows = 1 second
  With index: Find directly = 0.001 seconds = 1000x faster!
  ```
- Example in our setup script:
  ```sql
  CREATE INDEX idx_name ON employees(name);
  CREATE INDEX idx_department ON employees(department);
  ```

**Visual Comparison:**

```
PRIMARY KEY (id):
  Row 1: id=1 ← Can search instantly
  Row 2: id=2 ← No duplicates allowed
  Row 3: id=3 ← Automatically indexed

UNIQUE CONSTRAINT (email):
  Row 1: email=john@co.com ← No duplicates
  Row 2: email=jane@co.com ← Automatically indexed
  Row 3: NULL ← Multiple NULLs allowed!

INDEX (name):
  search_for: "John" ← Jumps to location, doesn't read all rows
  Result: Fast!
```

---

#### Q5: What is SQL injection and how do we prevent it?

**Answer:**

**SQL Injection**
- Attack: Inserting malicious SQL code into user input
- Result: Attacker can steal data, delete database, etc.
- Severity: ⚠️ CRITICAL vulnerability

**Example Attack:**

```python
# VULNERABLE CODE (DO NOT USE):
user_input = "John'; DROP TABLE employees; --"
query = f"SELECT * FROM employees WHERE name = '{user_input}'"
# Results in: SELECT * FROM employees WHERE name = 'John'; DROP TABLE employees; --'
# This DELETES the entire employees table!
```

**Prevention: Parameterized Queries**

```python
# SECURE CODE (USE THIS):
user_input = "John'; DROP TABLE employees; --"
query = "SELECT * FROM employees WHERE name = %s"
cursor.execute(query, (user_input,))
# Input treated as VALUE, not code
# Results in: SELECT * FROM employees WHERE name = 'John''; DROP TABLE employees; --'
# The dangerous code is escaped and treated as literal text
```

**How We Implement It:**

In `database.py`:
```python
def fetch_query(query, params=None):
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)  # ✅ Secure - parameterized
    return cursor.fetchall()
```

In `employee_queries.py`:
```python
def add_employee(name, email, department, salary):
    query = "INSERT INTO employees (name, email, department, salary) VALUES (%s, %s, %s, %s)"
    execute_query(query, (name, email, department, salary))  # ✅ Secure - params separate
```

**Key Rules:**
1. Never concatenate user input into SQL strings
2. Always use %s placeholders
3. Always pass parameters separately
4. Let database library escape dangerous characters

---

### PART 3: Python & FastAPI Concepts

#### Q6: Explain decorators in Python and how FastAPI uses them.

**Answer:**

**What are Decorators?**
- Function that modifies another function
- Syntax: `@decorator_name`
- Adds functionality without changing original function

**Simple Example:**

```python
# Without decorator:
def greet():
    print("Hello!")

# With decorator:
def add_greeting(func):
    def wrapper():
        print("Starting...")
        func()
        print("Done!")
    return wrapper

@add_greeting
def greet():
    print("Hello!")

greet()
# Output:
# Starting...
# Hello!
# Done!
```

**FastAPI Uses Decorators for Routing:**

```python
from fastapi import FastAPI

app = FastAPI()

# Decorator tells FastAPI this is a GET endpoint at /employees
@app.get("/employees")
def get_employees():
    return {"employees": [...]}

# Decorator for POST endpoint
@app.post("/employees")
def create_employee(name: str, email: str):
    return {"id": 1, "name": name}

# Decorator with path parameter
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    return {"id": employee_id}
```

**How FastAPI Decorators Work:**

```
@app.get("/employees")
↓
1. FastAPI sees decorator
2. Creates route mapping
3. Listens for GET requests to /employees
4. When request comes: calls function
5. Function returns data
6. FastAPI converts to JSON response
7. Sends HTTP 200 back to client
```

**Multiple Decorators Possible:**

```python
@app.get("/employees")
@app.get("/staff")  # Same function for two URLs
def get_employees():
    return {"employees": [...]}
```

---

#### Q7: What is the difference between path parameters and query parameters?

**Answer:**

**Path Parameters** - Part of URL path
- Syntax: `@app.get("/employees/{employee_id}")`
- In URL: `/employees/1`
- Mandatory: Must be provided
- Example: `/employees/1`, `/employees/5`
- Use when: Identifying resource

```python
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    return {"id": employee_id}

# Request: GET /employees/1
# Response: {"id": 1}

# Request: GET /employees/5
# Response: {"id": 5}
```

**Query Parameters** - After ? in URL
- Syntax: `?key=value`
- In URL: `/employees?name=John`
- Optional: Can be omitted
- Example: `/employees?name=John`, `/employees?department=IT`
- Use when: Filtering, searching, sorting

```python
@app.get("/employees/search/name")
def search_by_name(value: str):
    return {"search": value}

# Request: GET /employees/search/name?value=John
# Response: {"search": "John"}

# Request: GET /employees/search/name?value=Jane
# Response: {"search": "Jane"}
```

**Comparison Table:**

| Feature | Path Parameter | Query Parameter |
|---------|---|---|
| Syntax | `{variable}` | `?key=value` |
| In URL | Part of path | After ? |
| Mandatory | Yes | No (optional) |
| Example | `/employees/1` | `/employees?dept=IT` |
| Use case | Identify resource | Filter/search |
| Multiple | Less common | Common |

**Combined Example:**

```python
@app.get("/employees/search/salary-range")
def search_salary(min_sal: float, max_sal: float):
    return {"min": min_sal, "max": max_sal}

# Request: GET /employees/search/salary-range?min_sal=50000&max_sal=80000
# Response: {"min": 50000, "max": 80000}
```

---

### PART 4: File Operations

#### Q8: Explain the difference between reading, writing, and appending to files.

**Answer:**

**Read Mode (`'r'`) - Opening existing file to read**
```python
with open("data.txt", "r") as f:
    content = f.read()  # Read entire file
    # OR
    lines = f.readlines()  # Read as list of lines
```
- Purpose: View file contents
- File must exist (error if not)
- Cannot modify file
- Pointer moves from start to end
- Common use: Loading config, reading logs

**Write Mode (`'w') - Creating file or overwriting**
```python
with open("data.txt", "w") as f:
    f.write("New content")
```
- Purpose: Create new file or replace contents
- Creates file if doesn't exist
- Overwrites if file exists (deletes old content!)
- Pointer starts at beginning
- Common use: Save report, create backup

**Append Mode (`'a') - Adding to existing file**
```python
with open("data.txt", "a") as f:
    f.write("New line\n")
```
- Purpose: Add to end of file
- Creates file if doesn't exist
- Preserves existing content
- Pointer jumps to end
- Common use: Log entries, accumulating data

**Visual Comparison:**

```
Original file:
┌─────────────────┐
│ Line 1          │
│ Line 2          │
└─────────────────┘

Read mode ('r'):
├─ Read Line 1 ✓
├─ Read Line 2 ✓
└─ Return content

Write mode ('w'):
├─ DELETE all content
├─ Write "Hello"
└─ File now: "Hello"

Append mode ('a'):
├─ Keep Line 1
├─ Keep Line 2
├─ ADD "Line 3"
└─ File now: Line 1, Line 2, Line 3
```

**Best Practices:**

```python
# Always use 'with' statement (auto-closes file)
with open("file.txt", "r") as f:
    content = f.read()

# Never do this (file not closed):
f = open("file.txt", "r")
content = f.read()
# File stays open! Memory leak!

# Specify encoding (UTF-8 recommended):
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

---

#### Q9: How do you safely delete files and prevent disasters?

**Answer:**

**Dangers of File Deletion:**
- Permanent: No undo button
- Lost data: Gone forever (unless backup)
- Cascade: Might break dependent systems
- Accidental: User clicks wrong button

**Safe Deletion Pattern:**

```python
import os
from pathlib import Path

def safe_delete_file(filename):
    """Safe file deletion with checks"""
    
    # Check 1: Validate filename (prevent path traversal)
    if ".." in filename or "/" in filename or "\\" in filename:
        return {"error": "Invalid filename"}
    
    # Check 2: Security - only allow certain directories
    allowed_dir = "uploads"
    filepath = os.path.join(allowed_dir, filename)
    
    # Check 3: Verify file exists
    if not os.path.exists(filepath):
        return {"error": "File does not exist"}
    
    # Check 4: Verify is file (not directory)
    if not os.path.isfile(filepath):
        return {"error": "Target is directory, not file"}
    
    # Check 5: Backup before delete (optional)
    backup_path = filepath + ".backup"
    shutil.copy(filepath, backup_path)
    
    # Check 6: Delete
    try:
        os.remove(filepath)
        return {"success": True, "backup": backup_path}
    except Exception as e:
        return {"error": f"Delete failed: {str(e)}"}
```

**In Our API:**

```python
def delete_file(filename):
    # Check 1: Filename validation
    if ".." in filename or "/" in filename or "\\" in filename:
        return {"success": False, "error": "Invalid filename"}
    
    # Check 2: Path construction (safe)
    filepath = os.path.join(UPLOADS_DIR, filename)
    
    # Check 3: Existence verification
    if not os.path.exists(filepath):
        return {"success": False, "error": "File does not exist"}
    
    # Check 4: Safe deletion
    try:
        os.remove(filepath)
        return {"success": True, "message": "File deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Security Rules:**

1. **Never allow root directory access:**
   ```python
   # BAD:
   delete(filename)  # Can delete system files!
   
   # GOOD:
   delete(filename)  # Only in uploads/ folder
   ```

2. **Always validate filename:**
   ```python
   # Bad characters to check:
   if ".." in filename:  # Prevents ../../etc/passwd
   if "/" in filename:   # Prevents /etc/
   if "\\" in filename:  # Prevents C:\Windows\
   ```

3. **Require confirmation for important files:**
   ```python
   # For API, require explicit user action
   # For CLI, ask before deleting
   if filename in CRITICAL_FILES:
       require_user_confirmation()
   ```

4. **Log deletions:**
   ```python
   logger.info(f"File deleted: {filename} by user {user_id}")
   ```

5. **Use soft delete initially:**
   ```python
   # Instead of immediate delete:
   file.deleted = True
   file.deleted_at = datetime.now()
   
   # Can restore within 30 days
   # Then permanently delete
   ```

---

#### Q10: Explain error handling with try-except-finally.

**Answer:**

**Error Handling Purpose:**
- Prevent crashes
- Recover gracefully
- Show helpful messages
- Log problems
- Maintain data integrity

**Three Components:**

**1. Try Block - Code that might fail**
```python
try:
    file = open("data.txt")  # Might fail if file doesn't exist
    content = file.read()    # Might fail if permission denied
```

**2. Except Block - Handle specific errors**
```python
except FileNotFoundError:
    print("File doesn't exist")
except PermissionError:
    print("No permission to read")
except Exception as e:  # Catch-all
    print(f"Unexpected error: {e}")
```

**3. Finally Block - Always executes**
```python
finally:
    if file:
        file.close()  # Cleanup, even if error occurred
```

**Complete Example:**

```python
def read_employee_file(filename):
    """Read employee data with error handling"""
    file = None
    try:
        # Try to open and read
        file = open(filename, 'r')
        data = file.read()
        return {"success": True, "data": data}
        
    except FileNotFoundError:
        # Handle missing file
        return {"success": False, "error": "File not found"}
        
    except PermissionError:
        # Handle permission denied
        return {"success": False, "error": "Permission denied"}
        
    except Exception as e:
        # Handle unexpected errors
        return {"success": False, "error": f"Error: {str(e)}"}
        
    finally:
        # ALWAYS runs - cleanup
        if file:
            file.close()  # Close file no matter what
            print("File closed (cleanup)")
```

**Error Hierarchy:**

```
Exception (base)
├── FileNotFoundError    # File doesn't exist
├── PermissionError      # No read/write permission
├── IsADirectoryError    # Path is directory, not file
├── ValueError           # Wrong value type
├── KeyError             # Dictionary key missing
├── IndexError           # List index out of range
└── ... many more
```

**Real API Example from Our Code:**

```python
def add_employee(name, email, department, salary):
    try:
        # Input validation
        if not name:
            return {"success": False, "error": "Name required"}
        
        # Check for duplicates
        existing = fetch_one("SELECT id FROM employees WHERE email = %s", (email,))
        if existing:
            return {"success": False, "error": "Email exists"}
        
        # Insert into database
        query = "INSERT INTO employees ..."
        affected_rows = execute_query(query, (name, email, department, salary))
        
        if affected_rows > 0:
            return {"success": True, "id": new_id}
        else:
            return {"success": False, "error": "Insert failed"}
            
    except Exception as e:
        # Log error, return safe message
        print(f"Error: {e}")
        return {"success": False, "error": "Database error"}
```

**Exception Handling Strategy:**

```
1. TRY: Attempt the operation
   ↓
2. CATCH: Handle known errors specifically
   - FileNotFoundError → "File not found"
   - PermissionError → "No permission"
   - ValueError → "Invalid data"
   ↓
3. CATCH-ALL: Handle unexpected errors
   - Exception → "Something went wrong"
   ↓
4. FINALLY: Always cleanup
   - Close files
   - Release resources
   - Log results
```

---

## 📝 Practice Tasks

### Task 1: Add Phone Field to Employees

**Objective:** Extend the employee table with a phone number field.

**Difficulty:** ⭐ Easy

**Steps:**

1. **Modify Database:**
```sql
ALTER TABLE employees ADD COLUMN phone VARCHAR(20) UNIQUE;
```

2. **Update `employee_queries.py`:**
```python
def add_employee(name, email, department, salary, phone=None):  # Add phone parameter
    # ... validation ...
    query = """
        INSERT INTO employees (name, email, department, salary, phone)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (name, email, department, salary, phone))
```

3. **Update `main.py`:**
```python
@app.post("/employees")
def create_employee(name: str, email: str, department: str, salary: float, phone: str = None):
    result = employee_queries.add_employee(name, email, department, salary, phone)
    # ... rest of code
```

4. **Test:**
```bash
curl -X POST "http://localhost:8000/employees?name=John&email=john@co.com&department=IT&salary=75000&phone=1234567890"
```

---

### Task 2: Create Salary Range Search

**Objective:** Add endpoint to search employees by salary range.

**Difficulty:** ⭐⭐ Medium

**Steps:**

1. **Add to `employee_queries.py`:**
```python
def search_by_salary_range(min_salary, max_salary):
    """Search employees by salary range"""
    try:
        if min_salary < 0 or max_salary < 0:
            return {"error": "Salary must be positive"}
        
        if min_salary > max_salary:
            return {"error": "Min salary cannot exceed max"}
        
        query = """
            SELECT id, name, email, department, salary 
            FROM employees 
            WHERE salary BETWEEN %s AND %s 
            ORDER BY salary ASC
        """
        results = fetch_query(query, (min_salary, max_salary))
        
        employees = []
        for row in results:
            employees.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "department": row[3],
                "salary": float(row[4])
            })
        
        return {"success": True, "count": len(employees), "data": employees}
        
    except Exception as e:
        return {"error": f"Error: {str(e)}"}
```

2. **Add to `main.py`:**
```python
@app.get("/employees/filter/salary-range")
def search_salary_range(min_sal: float, max_sal: float):
    result = employee_queries.search_by_salary_range(min_sal, max_sal)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result
```

3. **Test:**
```bash
# Get employees earning between 60000 and 80000
curl "http://localhost:8000/employees/filter/salary-range?min_sal=60000&max_sal=80000"
```

4. **Expected Response:**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {"id": 1, "name": "John", "email": "john@co.com", "department": "IT", "salary": 75000},
    {"id": 2, "name": "Jane", "email": "jane@co.com", "department": "HR", "salary": 65000}
  ]
}
```

---

### Task 3: Create Backup Feature

**Objective:** Add automatic backup of database to JSON file.

**Difficulty:** ⭐⭐ Medium

**Steps:**

1. **Add to `file_operations.py`:**
```python
def backup_employees_to_json(backup_name="backup.json"):
    """Create JSON backup of all employees"""
    try:
        import employee_queries
        from datetime import datetime
        
        # Get all employees
        employees = employee_queries.get_all_employees()
        
        if not employees:
            return {"success": False, "error": "No employees to backup"}
        
        # Add backup metadata
        backup_data = {
            "backup_date": str(datetime.now()),
            "total_employees": len(employees),
            "employees": employees
        }
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.json"
        
        # Write to backups folder
        backup_dir = "backups"
        Path(backup_dir).mkdir(exist_ok=True)
        
        filepath = os.path.join(backup_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        return {
            "success": True,
            "message": "Backup created successfully",
            "filename": filename,
            "path": filepath
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}
```

2. **Add to `main.py`:**
```python
@app.post("/employees/backup")
def backup_employees():
    result = file_operations.backup_employees_to_json()
    
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=500, detail=result["error"])
```

3. **Test:**
```bash
curl -X POST "http://localhost:8000/employees/backup"
```

---

### Task 4: Add Department Statistics

**Objective:** Create endpoint showing salary info per department.

**Difficulty:** ⭐⭐⭐ Hard

**Steps:**

1. **Add to `employee_queries.py`:**
```python
def get_department_statistics():
    """Get salary statistics per department"""
    try:
        query = """
            SELECT 
                department,
                COUNT(*) as employee_count,
                AVG(salary) as average_salary,
                MIN(salary) as min_salary,
                MAX(salary) as max_salary,
                SUM(salary) as total_salary
            FROM employees
            GROUP BY department
            ORDER BY average_salary DESC
        """
        
        results = fetch_query(query)
        
        stats = []
        for row in results:
            stats.append({
                "department": row[0],
                "employee_count": row[1],
                "average_salary": float(row[2]) if row[2] else 0,
                "min_salary": float(row[3]) if row[3] else 0,
                "max_salary": float(row[4]) if row[4] else 0,
                "total_salary": float(row[5]) if row[5] else 0
            })
        
        return {"success": True, "departments": stats}
        
    except Exception as e:
        return {"success": False, "error": str(e)}
```

2. **Add to `main.py`:**
```python
@app.get("/employees/stats/by-department")
def department_statistics():
    result = employee_queries.get_department_statistics()
    
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=500, detail=result["error"])
```

3. **Test:**
```bash
curl "http://localhost:8000/employees/stats/by-department"
```

4. **Expected Response:**
```json
{
  "success": true,
  "departments": [
    {
      "department": "IT",
      "employee_count": 2,
      "average_salary": 77500,
      "min_salary": 75000,
      "max_salary": 80000,
      "total_salary": 155000
    },
    {
      "department": "HR",
      "employee_count": 1,
      "average_salary": 65000,
      "min_salary": 65000,
      "max_salary": 65000,
      "total_salary": 65000
    }
  ]
}
```

---

## 🎯 Learning Checkpoints

### After Task 1:
✅ You can modify database schema  
✅ You understand ALTER TABLE  
✅ You can update multiple files together  

### After Task 2:
✅ You understand BETWEEN in SQL  
✅ You can create advanced queries  
✅ You know how to handle complex filtering  

### After Task 3:
✅ You can create backup systems  
✅ You understand file organization  
✅ You know metadata concepts  

### After Task 4:
✅ You can use GROUP BY and aggregates  
✅ You understand complex SQL queries  
✅ You can create analytical endpoints  

---

## 📚 Advanced Learning Topics

### Topic 1: Authentication with JWT

**Concept:** Secure endpoints with tokens

**Implementation:**
1. User logs in → get JWT token
2. User sends token with request
3. API validates token
4. Allow/deny based on token

### Topic 2: Database Migrations

**Concept:** Version control for database

**Implementation:**
1. Use Alembic to track schema changes
2. Roll forward/backward through versions
3. Keep track of all modifications

### Topic 3: Caching

**Concept:** Speed up repeated queries

**Implementation:**
1. Store frequently accessed data in memory
2. Invalidate when data changes
3. Reduce database load

### Topic 4: Rate Limiting

**Concept:** Prevent API abuse

**Implementation:**
1. Limit requests per user/IP
2. Return 429 Too Many Requests
3. Protect against DDoS

### Topic 5: API Documentation

**Concept:** Auto-generate API docs

**Implementation:**
1. FastAPI already generates /docs
2. Add detailed docstrings
3. Document request/response examples

---

## ✨ Conclusion

You've learned:

✅ REST API design  
✅ HTTP methods & status codes  
✅ Database design & SQL  
✅ Python file handling  
✅ FastAPI routing & decorators  
✅ Error handling patterns  
✅ Security best practices  
✅ API testing  

**Next Steps:**
- Deploy to production
- Add authentication
- Build frontend
- Scale the application

**Happy Learning!** 🚀
