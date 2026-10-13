# employee_queries.py - SQL Queries for Employee CRUD Operations
# This module contains all database operations for employee management
# Functions: add_employee, get_all_employees, get_employee_by_id, update_employee, delete_employee, search_employees

from database import execute_query, fetch_query, fetch_one

# ============================================================================
# TABLE SCHEMA
# ============================================================================
# CREATE TABLE employees (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) UNIQUE NOT NULL,
#     department VARCHAR(100) NOT NULL,
#     salary DECIMAL(10, 2) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );

# ============================================================================
# CREATE (INSERT) - Add new employee
# ============================================================================

def add_employee(name, email, department, salary):
    """
    Adds a new employee to the database.
    
    Args:
        name (str): Employee's full name
        email (str): Employee's email (must be unique)
        department (str): Department name (e.g., "IT", "HR", "Sales")
        salary (float): Annual salary
        
    Returns:
        dict: {"success": True, "id": new_id} or {"success": False, "error": "message"}
        
    Validation:
        - name: Required, string
        - email: Required, unique, valid format
        - department: Required, string
        - salary: Required, positive number
        
    Example:
        result = add_employee("John Doe", "john@company.com", "IT", 75000)
        if result["success"]:
            print(f"Employee added with ID: {result['id']}")
    """
    try:
        # Validate inputs
        if not name or not isinstance(name, str):
            return {"success": False, "error": "Name is required and must be a string"}
        
        if not email or not isinstance(email, str):
            return {"success": False, "error": "Email is required and must be a string"}
        
        if not department or not isinstance(department, str):
            return {"success": False, "error": "Department is required and must be a string"}
        
        if not salary or not isinstance(salary, (int, float)) or salary <= 0:
            return {"success": False, "error": "Salary is required and must be a positive number"}
        
        # Check if email already exists
        existing = fetch_one("SELECT id FROM employees WHERE email = %s", (email,))
        if existing:
            return {"success": False, "error": "Email already exists in the system"}
        
        # Insert new employee
        query = """
            INSERT INTO employees (name, email, department, salary)
            VALUES (%s, %s, %s, %s)
        """
        affected_rows = execute_query(query, (name, email, department, salary))
        
        if affected_rows > 0:
            # Get the ID of newly inserted employee
            employee = fetch_one("SELECT id FROM employees WHERE email = %s", (email,))
            return {"success": True, "id": employee[0], "message": "Employee added successfully"}
        else:
            return {"success": False, "error": "Failed to add employee"}
            
    except Exception as e:
        return {"success": False, "error": f"Database error: {str(e)}"}

# ============================================================================
# READ (SELECT) - Retrieve employees
# ============================================================================

def get_all_employees():
    """
    Retrieves all employees from the database.
    
    Returns:
        list: List of dictionaries with employee data
              [{"id": 1, "name": "John", "email": "john@co.com", ...}, ...]
              
    Example:
        employees = get_all_employees()
        for emp in employees:
            print(f"{emp['name']} - {emp['department']}")
    """
    try:
        query = "SELECT id, name, email, department, salary, created_at, updated_at FROM employees ORDER BY id"
        results = fetch_query(query)
        
        employees = []
        for row in results:
            employees.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "department": row[3],
                "salary": float(row[4]),
                "created_at": str(row[5]) if row[5] else None,
                "updated_at": str(row[6]) if row[6] else None
            })
        return employees
        
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return []

def get_employee_by_id(employee_id):
    """
    Retrieves a single employee by ID.
    
    Args:
        employee_id (int): The employee ID to search for
        
    Returns:
        dict: Employee data or {"error": "message"} if not found
        
    Example:
        emp = get_employee_by_id(1)
        if "error" not in emp:
            print(f"Found: {emp['name']}")
    """
    try:
        if not isinstance(employee_id, int) or employee_id <= 0:
            return {"error": "Invalid employee ID"}
        
        query = "SELECT id, name, email, department, salary, created_at, updated_at FROM employees WHERE id = %s"
        result = fetch_one(query, (employee_id,))
        
        if result:
            return {
                "id": result[0],
                "name": result[1],
                "email": result[2],
                "department": result[3],
                "salary": float(result[4]),
                "created_at": str(result[5]) if result[5] else None,
                "updated_at": str(result[6]) if result[6] else None
            }
        else:
            return {"error": "Employee not found"}
            
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}

def search_employees(search_type, search_value):
    """
    Searches employees by name or department.
    
    Args:
        search_type (str): "name" or "department"
        search_value (str): Value to search for
        
    Returns:
        list: List of matching employees or []
        
    Example:
        # Search by name
        results = search_employees("name", "John")
        
        # Search by department
        results = search_employees("department", "IT")
    """
    try:
        if search_type == "name":
            query = "SELECT id, name, email, department, salary, created_at, updated_at FROM employees WHERE name LIKE %s"
            search_param = f"%{search_value}%"
        elif search_type == "department":
            query = "SELECT id, name, email, department, salary, created_at, updated_at FROM employees WHERE department LIKE %s"
            search_param = f"%{search_value}%"
        else:
            return []
        
        results = fetch_query(query, (search_param,))
        
        employees = []
        for row in results:
            employees.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "department": row[3],
                "salary": float(row[4]),
                "created_at": str(row[5]) if row[5] else None,
                "updated_at": str(row[6]) if row[6] else None
            })
        return employees
        
    except Exception as e:
        print(f"Error searching employees: {e}")
        return []

# ============================================================================
# UPDATE - Modify employee details
# ============================================================================

def update_employee(employee_id, **kwargs):
    """
    Updates employee details. Can update any field individually.
    
    Args:
        employee_id (int): Employee ID to update
        **kwargs: Field names and values to update
                 Allowed: name, email, department, salary
        
    Returns:
        dict: {"success": True/False, "message": "..."} 
        
    Example:
        result = update_employee(1, name="Jane Doe", salary=80000)
        result = update_employee(2, department="HR")
    """
    try:
        if not isinstance(employee_id, int) or employee_id <= 0:
            return {"success": False, "error": "Invalid employee ID"}
        
        # Check if employee exists
        existing = fetch_one("SELECT id FROM employees WHERE id = %s", (employee_id,))
        if not existing:
            return {"success": False, "error": "Employee not found"}
        
        # Validate and build update query
        allowed_fields = ["name", "email", "department", "salary"]
        update_fields = []
        update_values = []
        
        for field, value in kwargs.items():
            if field not in allowed_fields:
                continue  # Skip invalid fields
            
            # Validate values
            if field == "email":
                if not value or not isinstance(value, str):
                    return {"success": False, "error": "Email must be a valid string"}
                # Check if new email already exists (and is not current employee's email)
                existing_email = fetch_one(
                    "SELECT id FROM employees WHERE email = %s AND id != %s",
                    (value, employee_id)
                )
                if existing_email:
                    return {"success": False, "error": "Email already exists"}
            
            elif field == "salary":
                if not value or not isinstance(value, (int, float)) or value <= 0:
                    return {"success": False, "error": "Salary must be a positive number"}
            
            elif field == "name" or field == "department":
                if not value or not isinstance(value, str):
                    return {"success": False, "error": f"{field.capitalize()} must be a non-empty string"}
            
            update_fields.append(f"{field} = %s")
            update_values.append(value)
        
        if not update_fields:
            return {"success": False, "error": "No valid fields to update"}
        
        # Build and execute update query
        query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = %s"
        update_values.append(employee_id)
        
        affected_rows = execute_query(query, tuple(update_values))
        
        if affected_rows > 0:
            return {"success": True, "message": "Employee updated successfully"}
        else:
            return {"success": False, "error": "Failed to update employee"}
            
    except Exception as e:
        return {"success": False, "error": f"Database error: {str(e)}"}

# ============================================================================
# DELETE - Remove employee
# ============================================================================

def delete_employee(employee_id):
    """
    Deletes an employee from the database.
    
    Args:
        employee_id (int): Employee ID to delete
        
    Returns:
        dict: {"success": True/False, "message": "..."} 
        
    Example:
        result = delete_employee(5)
        if result["success"]:
            print("Employee deleted successfully")
    """
    try:
        if not isinstance(employee_id, int) or employee_id <= 0:
            return {"success": False, "error": "Invalid employee ID"}
        
        # Check if employee exists
        existing = fetch_one("SELECT id FROM employees WHERE id = %s", (employee_id,))
        if not existing:
            return {"success": False, "error": "Employee not found"}
        
        # Delete employee
        query = "DELETE FROM employees WHERE id = %s"
        affected_rows = execute_query(query, (employee_id,))
        
        if affected_rows > 0:
            return {"success": True, "message": "Employee deleted successfully"}
        else:
            return {"success": False, "error": "Failed to delete employee"}
            
    except Exception as e:
        return {"success": False, "error": f"Database error: {str(e)}"}

# ============================================================================
# UTILITIES
# ============================================================================

def get_employee_count():
    """
    Returns the total number of employees.
    
    Returns:
        int: Number of employees
    """
    try:
        result = fetch_one("SELECT COUNT(*) FROM employees")
        return result[0] if result else 0
    except Exception as e:
        print(f"Error counting employees: {e}")
        return 0

def get_salary_statistics():
    """
    Returns salary statistics (average, min, max).
    
    Returns:
        dict: {"average": X, "min": Y, "max": Z} or {}
    """
    try:
        query = "SELECT AVG(salary), MIN(salary), MAX(salary) FROM employees"
        result = fetch_one(query)
        
        if result and result[0] is not None:
            return {
                "average": float(result[0]),
                "minimum": float(result[1]),
                "maximum": float(result[2])
            }
        return {}
        
    except Exception as e:
        print(f"Error getting salary statistics: {e}")
        return {}
