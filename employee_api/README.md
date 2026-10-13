# Employee Management REST API - Complete Guide

A beginner-friendly, production-ready REST API built with Python, FastAPI, MySQL, and file handling. **Learn every line of code** through detailed documentation and examples.

**Author**: AI Assistant  
**Version**: 1.0.0  
**Last Updated**: 2026  
**License**: MIT

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Technologies](#technologies)
3. [Project Structure](#project-structure)
4. [Installation & Setup](#installation--setup)
5. [Database Setup](#database-setup)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)
8. [Complete Examples](#complete-examples)
9. [Testing with Postman](#testing-with-postman)
10. [Error Handling](#error-handling)
11. [Troubleshooting](#troubleshooting)
12. [Interview Questions](#interview-questions)
13. [Practice Tasks](#practice-tasks)
14. [Learning Resources](#learning-resources)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- MySQL Server 5.7+ installed and running
- Postman (for API testing)

### Setup in 5 Minutes

```bash
# 1. Navigate to project
cd employee_api

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up database (MySQL must be running)
mysql -u root -p < setup_database.sql

# 5. Update .env with your MySQL credentials
# Edit .env file and change DB_PASSWORD

# 6. Run the API server
uvicorn main:app --reload

# 7. Visit API documentation
# Browser: http://localhost:8000/docs
```

---

## 🛠️ Technologies

| Technology | Purpose | Version | Why? |
|---|---|---|---|
| **Python** | Programming language | 3.8+ | Easy to learn, great for APIs |
| **FastAPI** | Web framework | 0.143.0 | Modern, fast, auto-docs |
| **Uvicorn** | ASGI server | 0.54.0 | High-performance Python server |
| **MySQL** | Database | 5.7+ or 8.0+ | Popular, reliable relational DB |
| **mysql-connector-python** | MySQL driver | 26.7.0 | Official MySQL connector |
| **python-dotenv** | Config management | 1.2.4 | Secure credential storage |
| **Postman** | API testing | Latest | Professional API testing tool |

---

## 📁 Project Structure

```
employee_api/
├── main.py                      # FastAPI application & routes
├── database.py                  # MySQL connection management
├── employee_queries.py          # SQL queries & database functions
├── file_operations.py           # File handling (text, CSV, JSON)
├── setup_database.sql           # MySQL database initialization
├── uploads/                     # Uploaded files storage
├── reports/                     # Exported CSV/JSON files
├── venv/                        # Python virtual environment (not in git)
├── requirements.txt             # Python package dependencies
├── .env                         # Configuration (NOT in git)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

### File Responsibilities

| File | Responsibility | Lines |
|------|---|---|
| **main.py** | FastAPI application, all API routes, error handling | ~500 |
| **database.py** | MySQL connection, query execution, error handling | ~150 |
| **employee_queries.py** | CRUD functions, SQL queries, validation | ~400 |
| **file_operations.py** | Text/CSV/JSON files, uploads, validation | ~600 |
| **setup_database.sql** | Database and table creation | ~50 |

---

## 📦 Installation & Setup

### Step 1: Verify Python Installation

```bash
py --version
# Output: Python 3.14.6
```

### Step 2: Create Virtual Environment

```bash
# Windows
py -m venv venv

# Mac/Linux
python3 -m venv venv
```

**Why Virtual Environment?**
- Isolates your project's packages
- Prevents conflicts with other projects
- Keeps your system Python clean

### Step 3: Activate Virtual Environment

```bash
# Windows
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate

# You should see (venv) in your terminal
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- fastapi: Web framework for building APIs
- uvicorn: Server to run your application
- mysql-connector-python: Connect Python to MySQL
- python-dotenv: Load environment variables

### Step 5: Configure Environment Variables

Edit `.env` file:

```env
# Change these to match YOUR MySQL setup
DB_HOST=localhost        # Where MySQL runs
DB_USER=root            # MySQL username
DB_PASSWORD=your_password_here  # YOUR MySQL password
DB_NAME=employee_management  # Database name
DB_PORT=3306            # MySQL port (default)
API_PORT=8000           # FastAPI server port
```

**⚠️ IMPORTANT**: Never commit `.env` to GitHub! It contains passwords.

---

## 🗄️ Database Setup

### Step 1: Verify MySQL is Running

```bash
# Test MySQL connection
mysql -u root -p

# Type your password, then type 'exit'
exit
```

### Step 2: Create Database and Table

```bash
# Run the setup script
mysql -u root -p < setup_database.sql

# Type your MySQL password when prompted
```

**What the script does:**
1. Creates `employee_management` database
2. Creates `employees` table with columns:
   - `id` (Primary Key, Auto-Increment)
   - `name` (String, Required)
   - `email` (String, Unique, Required)
   - `department` (String, Required)
   - `salary` (Decimal, Required)
   - `created_at` (Timestamp, Auto-set)
   - `updated_at` (Timestamp, Auto-update)

### Step 3: Verify Database Setup

```bash
mysql -u root -p employee_management

# List tables
SHOW TABLES;

# View employees table structure
DESCRIBE employees;

# View sample data
SELECT * FROM employees;

# Exit MySQL
exit
```

---

## ▶️ Running the Application

### Start the Server

```bash
# Make sure venv is activated
uvicorn main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Access the API

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **API Root**: http://localhost:8000/

### What `--reload` Means

- Automatically restarts server when you edit files
- **NEVER use in production** - use for development only
- Helps during development to test changes quickly

---

## 📡 API Endpoints

### Endpoint Categories

1. **Employee Management (CRUD)**
2. **Text File Operations**
3. **CSV Import/Export**
4. **JSON Import/Export**
5. **File Upload/Download**

### Employee Management Endpoints

#### 1. Create Employee
```
POST /employees
Parameters:
  - name (string): Employee name
  - email (string): Unique email address
  - department (string): Department name
  - salary (number): Annual salary

Returns: { "success": true, "id": 1, "message": "..." }
```

#### 2. Get All Employees
```
GET /employees

Returns: { "success": true, "count": 5, "data": [...] }
```

#### 3. Get Employee by ID
```
GET /employees/{id}

Returns: { "success": true, "data": {...} }
```

#### 4. Update Employee
```
PUT /employees/{id}
Parameters:
  - name (optional)
  - email (optional)
  - department (optional)
  - salary (optional)

Returns: { "success": true, "message": "..." }
```

#### 5. Delete Employee
```
DELETE /employees/{id}

Returns: { "success": true, "message": "..." }
```

#### 6. Search Employees
```
GET /employees/search/{search_type}?value={search_term}

search_type: "name" or "department"
Examples:
  GET /employees/search/name?value=John
  GET /employees/search/department?value=IT

Returns: { "success": true, "count": N, "data": [...] }
```

#### 7. Get Employee Statistics
```
GET /employees/stats/summary

Returns: {
  "success": true,
  "total_employees": 5,
  "salary_statistics": {
    "average": 69000,
    "minimum": 55000,
    "maximum": 80000
  }
}
```

### Text File Endpoints

#### Create File
```
POST /files/text/create?filename=notes.txt&content=Hello
```

#### Write to File
```
POST /files/text/write?filename=data.txt&content=New%20content
```

#### Append to File
```
POST /files/text/append?filename=log.txt&content=New%20line
```

#### Read File
```
GET /files/text/read/data.txt
```

#### Read File Lines
```
GET /files/text/lines/log.txt
```

#### Check File Exists
```
GET /files/text/exists/data.txt
```

#### Get File Size
```
GET /files/text/size/data.txt
```

#### Delete File
```
DELETE /files/text/old_file.txt
```

#### Rename File
```
POST /files/text/rename?old_filename=old.txt&new_filename=new.txt
```

#### Copy File
```
POST /files/text/copy?source_filename=original.txt&dest_filename=backup.txt
```

### CSV Endpoints

#### Read CSV File
```
GET /files/csv/read/employees.csv
```

#### Import CSV to Database
```
POST /files/csv/import?filename=employees.csv

CSV format required:
name,email,department,salary
John Doe,john@co.com,IT,75000
Jane Smith,jane@co.com,HR,65000
```

#### Export Database to CSV
```
POST /files/csv/export?filename=employees_export.csv

Creates file in reports/ folder
```

### JSON Endpoints

#### Read JSON File
```
GET /files/json/read/data.json
```

#### Import JSON to Database
```
POST /files/json/import?filename=employees.json

JSON format required:
{
  "employees": [
    {"name": "John", "email": "john@co.com", "department": "IT", "salary": 75000},
    {"name": "Jane", "email": "jane@co.com", "department": "HR", "salary": 65000}
  ]
}
```

#### Export Database to JSON
```
POST /files/json/export?filename=employees_export.json

Creates file in reports/ folder
```

### File Upload/Download

#### Upload File
```
POST /files/upload

multipart/form-data with file
Allowed: .txt, .csv, .json
Max size: 10 MB
```

#### Download File
```
GET /files/download/filename.csv
```

#### Download Report
```
GET /files/report-download/employees_export.csv
```

#### List Uploaded Files
```
GET /files/list

Returns all files in uploads/ folder
```

---

## 💻 Complete Examples

### Example 1: Create and Retrieve Employee

**cURL Command:**
```bash
# Create employee
curl -X POST "http://localhost:8000/employees?name=John%20Doe&email=john@company.com&department=IT&salary=75000"

# Response:
# {"success":true,"message":"Employee added successfully","id":1,"status_code":201}

# Get the employee
curl -X GET "http://localhost:8000/employees/1"

# Response:
# {
#   "success": true,
#   "data": {
#     "id": 1,
#     "name": "John Doe",
#     "email": "john@company.com",
#     "department": "IT",
#     "salary": 75000.0,
#     "created_at": "2026-10-13 14:42:00",
#     "updated_at": "2026-10-13 14:42:00"
#   }
# }
```

**Python Code:**
```python
import requests

# Create employee
response = requests.post(
    "http://localhost:8000/employees",
    params={
        "name": "John Doe",
        "email": "john@company.com",
        "department": "IT",
        "salary": 75000
    }
)
print(response.json())

# Get employee
response = requests.get("http://localhost:8000/employees/1")
print(response.json())
```

### Example 2: Search Employees

```bash
# Search by name
curl "http://localhost:8000/employees/search/name?value=John"

# Search by department
curl "http://localhost:8000/employees/search/department?value=IT"

# Response:
# {
#   "success": true,
#   "search_type": "name",
#   "search_value": "John",
#   "count": 2,
#   "data": [...]
# }
```

### Example 3: Text File Operations

```bash
# Create file
curl -X POST "http://localhost:8000/files/text/create?filename=notes.txt&content=Hello%20World"

# Read file
curl "http://localhost:8000/files/text/read/notes.txt"

# Append to file
curl -X POST "http://localhost:8000/files/text/append?filename=notes.txt&content=%0ANew%20line"

# Response:
# {"success": true, "message": "Content appended to 'notes.txt'"}
```

### Example 4: CSV Import/Export

```bash
# Create CSV file content:
# name,email,department,salary
# John Doe,john@co.com,IT,75000
# Jane Smith,jane@co.com,HR,65000

# Upload file (using Postman or multipart form)
curl -F "file=@employees.csv" http://localhost:8000/files/upload

# Import CSV to database
curl -X POST "http://localhost:8000/files/csv/import?filename=employees.csv"

# Export database to CSV
curl -X POST "http://localhost:8000/files/csv/export?filename=employees_export.csv"

# Response:
# {
#   "success": true,
#   "message": "CSV file 'employees_export.csv' created with 5 rows",
#   "path": "reports/employees_export.csv",
#   "row_count": 5
# }

# Download exported file
curl "http://localhost:8000/files/report-download/employees_export.csv" -o employees.csv
```

### Example 5: JSON Operations

```bash
# Create JSON file:
# {
#   "employees": [
#     {"name": "John", "email": "john@co.com", "department": "IT", "salary": 75000},
#     {"name": "Jane", "email": "jane@co.com", "department": "HR", "salary": 65000}
#   ]
# }

# Import JSON to database
curl -X POST "http://localhost:8000/files/json/import?filename=employees.json"

# Export database to JSON
curl -X POST "http://localhost:8000/files/json/export?filename=employees_export.json"

# Response:
# {
#   "success": true,
#   "message": "JSON file 'employees_export.json' created successfully",
#   "path": "reports/employees_export.json",
#   "export_count": 5
# }
```

---

## 🧪 Testing with Postman

### Postman Setup

1. **Download Postman**: https://www.postman.com/downloads/
2. **Create New Collection**: "Employee API"
3. **Add Requests**: Create requests for each endpoint

### Sample Postman Requests

#### Request 1: Create Employee

```
Method: POST
URL: http://localhost:8000/employees
Params:
  name: John Doe
  email: john@company.com
  department: IT
  salary: 75000

Expected Response (201):
{
  "success": true,
  "message": "Employee added successfully",
  "id": 1,
  "status_code": 201
}
```

#### Request 2: Get All Employees

```
Method: GET
URL: http://localhost:8000/employees

Expected Response (200):
{
  "success": true,
  "count": 1,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@company.com",
      "department": "IT",
      "salary": 75000.0,
      "created_at": "2026-10-13 14:42:00",
      "updated_at": "2026-10-13 14:42:00"
    }
  ]
}
```

#### Request 3: Update Employee

```
Method: PUT
URL: http://localhost:8000/employees/1
Params:
  salary: 80000

Expected Response (200):
{
  "success": true,
  "message": "Employee updated successfully",
  "status_code": 200
}
```

#### Request 4: Delete Employee

```
Method: DELETE
URL: http://localhost:8000/employees/1

Expected Response (200):
{
  "success": true,
  "message": "Employee deleted successfully",
  "status_code": 200
}
```

#### Request 5: Search by Department

```
Method: GET
URL: http://localhost:8000/employees/search/department?value=IT

Expected Response (200):
{
  "success": true,
  "search_type": "department",
  "search_value": "IT",
  "count": 3,
  "data": [...]
}
```

### Postman Test Steps

1. **Create Collection**
   - Click "New" → Collection
   - Name: "Employee Management API"

2. **Add Environment**
   - Click "Environments" 
   - Create "Local Development"
   - Add variable: `base_url` = `http://localhost:8000`

3. **Create Requests**
   - Add requests for each endpoint
   - Use `{{base_url}}` in URLs
   - Save responses

4. **Run Tests**
   - Click "Send" on each request
   - Verify response status code
   - Check response body matches expected

---

## ❌ Error Handling

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK - Request succeeded | GET employee successful |
| 201 | Created - Resource created | POST new employee successful |
| 400 | Bad Request - Invalid input | Email already exists |
| 404 | Not Found - Resource doesn't exist | Employee ID not found |
| 500 | Server Error - Internal error | Database connection failed |

### Example Error Responses

#### Invalid Email (Duplicate)
```json
{
  "success": false,
  "error": "Email already exists in the system"
}
```

#### Employee Not Found
```json
{
  "success": false,
  "error": "Employee not found"
}
```

#### Invalid Salary
```json
{
  "success": false,
  "error": "Salary must be a positive number"
}
```

#### File Not Found
```json
{
  "success": false,
  "error": "File does not exist"
}
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to MySQL Server"

**Causes:**
- MySQL is not running
- Wrong credentials in .env
- Wrong host/port

**Solutions:**
```bash
# Check if MySQL is running
mysql -u root -p

# Update .env with correct credentials
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_actual_password

# Restart the application
uvicorn main:app --reload
```

### Issue: "Database 'employee_management' does not exist"

**Solutions:**
```bash
# Run setup script again
mysql -u root -p < setup_database.sql

# Or manually create in MySQL:
mysql -u root -p
CREATE DATABASE employee_management;
exit
```

### Issue: "Port 8000 already in use"

**Solutions:**
```bash
# Use different port
uvicorn main:app --reload --port 8001

# Or kill process on port 8000
# Windows: taskkill /PID <pid> /F
# Mac/Linux: kill -9 <pid>
```

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solutions:**
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies again
pip install -r requirements.txt
```

### Issue: Virtual Environment Not Activating

**Windows:**
```bash
# If execution policy error, run this ONCE:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
.\venv\Scripts\Activate.ps1
```

---

## 🎓 Interview Questions

### Question 1: What is a REST API?

**Answer:**
REST (Representational State Transfer) is an architectural style for web APIs using HTTP methods:
- **GET**: Retrieve data
- **POST**: Create data
- **PUT**: Update data
- **DELETE**: Remove data

Example: `GET /employees` retrieves all employees.

---

### Question 2: Explain the difference between GET and POST.

**Answer:**
| Aspect | GET | POST |
|--------|-----|------|
| Purpose | Retrieve data | Create/send data |
| Parameters | In URL (visible) | In body (hidden) |
| Caching | Can be cached | Usually not cached |
| Security | Less secure | More secure |
| Example | `GET /employees` | `POST /employees` with name, email, etc. |

---

### Question 3: What is a Primary Key and why is it important?

**Answer:**
A Primary Key (like `id`) is a unique identifier for each record:
- **Uniqueness**: No two rows have same ID
- **Speed**: Queries are faster with primary keys
- **Relationships**: Links records between tables
- **Integrity**: Prevents duplicate records

In SQL: `id INT AUTO_INCREMENT PRIMARY KEY`

---

### Question 4: What is a UNIQUE constraint?

**Answer:**
A UNIQUE constraint ensures no duplicate values in a column:
```sql
email VARCHAR(100) UNIQUE NOT NULL
```
- Prevents duplicate emails
- Faster searches
- Different from PRIMARY KEY (you can only have one primary key, but multiple unique constraints)

---

### Question 5: Explain virtual environments in Python.

**Answer:**
Virtual environments isolate project dependencies:
- **Before**: All packages installed globally → conflicts
- **After**: Each project has its own packages → no conflicts

Example: Project A uses Django 3.0, Project B uses Django 4.0 (no conflict).

Creation: `py -m venv venv`

---

## 📝 Practice Tasks

### Task 1: Add a New Field to Employees Table

**Objective**: Add a "phone" field to the employees table.

**Steps**:
1. Connect to MySQL:
   ```sql
   ALTER TABLE employees ADD COLUMN phone VARCHAR(20) UNIQUE;
   ```

2. Update `employee_queries.py`:
   - Add `phone` parameter to `add_employee()`
   - Update INSERT query to include phone

3. Update `main.py`:
   - Add `phone` parameter to `/employees` POST endpoint

4. Test with Postman:
   ```
   POST /employees?name=John&email=john@co.com&department=IT&salary=75000&phone=1234567890
   ```

---

### Task 2: Create a Salary Range Search

**Objective**: Add endpoint to search employees by salary range.

**Steps**:
1. Add function in `employee_queries.py`:
   ```python
   def search_by_salary_range(min_salary, max_salary):
       query = "SELECT * FROM employees WHERE salary BETWEEN %s AND %s"
       return fetch_query(query, (min_salary, max_salary))
   ```

2. Add endpoint in `main.py`:
   ```python
   @app.get("/employees/search/salary-range")
   def search_salary_range(min_sal: float, max_sal: float):
       results = employee_queries.search_by_salary_range(min_sal, max_sal)
       return {"success": True, "count": len(results), "data": results}
   ```

3. Test:
   ```
   GET /employees/search/salary-range?min_sal=50000&max_sal=75000
   ```

---

## 📚 Learning Resources

### Official Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python Official Docs](https://docs.python.org/3/)

### Video Tutorials
- FastAPI Crash Course
- MySQL for Beginners
- Python REST API Development

### Books
- "Building Web APIs with Flask" by Miguel Grinberg
- "MySQL 8.0 Reference Manual"
- "FastAPI by Example"

### Online Courses
- FastAPI Masterclass
- Complete MySQL Course
- Python for Web Development

### Practice Websites
- LeetCode (SQL problems)
- HackerRank (Python)
- Codewars (Python challenges)

---

## 🚀 Deployment Guide (Optional)

To deploy to production:

1. **Use production server** (not uvicorn with --reload):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 main:app
   ```

2. **Use environment-specific .env files**:
   - `.env.development` (development)
   - `.env.production` (production)

3. **Enable HTTPS** for secure data transmission

4. **Use reverse proxy** (nginx) for better performance

5. **Add rate limiting** to prevent abuse

---

## 📞 Support & Questions

- Check the [Troubleshooting](#troubleshooting) section
- Review [Error Handling](#error-handling) examples
- Consult [Interview Questions](#interview-questions) for concepts

---

## 📄 License

This project is provided as an educational resource under the MIT License.

---

## ✨ Summary

You now have a **complete, production-ready REST API** with:

✅ Employee CRUD operations  
✅ Text file handling  
✅ CSV import/export  
✅ JSON import/export  
✅ File upload/download  
✅ Complete error handling  
✅ Database integration  
✅ API documentation  

**Next Steps**:
1. Test all endpoints with Postman
2. Explore FastAPI auto-generated documentation at `/docs`
3. Modify and extend the API for your needs
4. Deploy to production when ready

Happy coding! 🎉

