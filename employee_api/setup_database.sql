-- setup_database.sql - MySQL Database and Table Initialization Script
-- Run this script in MySQL to set up the database structure
-- Usage: mysql -u root -p < setup_database.sql

-- ============================================================================
-- CREATE DATABASE
-- ============================================================================

-- Create the database (drop if exists for clean setup)
DROP DATABASE IF EXISTS employee_management;
CREATE DATABASE employee_management;

-- Use the database
USE employee_management;

-- ============================================================================
-- CREATE EMPLOYEES TABLE
-- ============================================================================

CREATE TABLE employees (
    -- Primary Key: Unique identifier for each employee
    -- AUTO_INCREMENT: Automatically generates next ID
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Employee name: VARCHAR(100) allows up to 100 characters
    -- NOT NULL: Name is required
    name VARCHAR(100) NOT NULL,
    
    -- Employee email: Must be unique (no duplicates allowed)
    -- VARCHAR(100): Email can be up to 100 characters
    -- UNIQUE: Ensures no two employees have same email
    -- NOT NULL: Email is required
    email VARCHAR(100) UNIQUE NOT NULL,
    
    -- Department name: E.g., "IT", "HR", "Sales"
    -- VARCHAR(100): Department name up to 100 characters
    -- NOT NULL: Department is required
    department VARCHAR(100) NOT NULL,
    
    -- Annual salary: DECIMAL(10, 2) allows values up to 99,999,999.99
    -- Reason for DECIMAL: Avoids floating-point precision issues
    salary DECIMAL(10, 2) NOT NULL,
    
    -- Timestamp when employee was created
    -- DEFAULT CURRENT_TIMESTAMP: Automatically sets to creation time
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Timestamp when employee record was last updated
    -- DEFAULT CURRENT_TIMESTAMP: Automatically sets to creation time
    -- ON UPDATE CURRENT_TIMESTAMP: Automatically updates when record changes
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================================
-- CREATE INDEXES (for faster queries)
-- ============================================================================

-- Index on name for faster searches
CREATE INDEX idx_name ON employees(name);

-- Index on department for faster filtering
CREATE INDEX idx_department ON employees(department);

-- ============================================================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================================================

INSERT INTO employees (name, email, department, salary) VALUES
('John Doe', 'john.doe@company.com', 'IT', 75000),
('Jane Smith', 'jane.smith@company.com', 'HR', 65000),
('Mike Johnson', 'mike.johnson@company.com', 'Sales', 55000),
('Sarah Williams', 'sarah.williams@company.com', 'IT', 80000),
('Robert Brown', 'robert.brown@company.com', 'Finance', 70000);

-- ============================================================================
-- TABLE STRUCTURE EXPLANATION
-- ============================================================================

-- PRIMARY KEY (id):
--   - Uniquely identifies each employee
--   - AUTO_INCREMENT: MySQL automatically assigns next number
--   - Benefits: Fast lookups, data integrity

-- UNIQUE Constraint (email):
--   - Ensures no two employees have same email
--   - Prevents duplicate records
--   - MySQL automatically creates index for faster lookups

-- NOT NULL Constraint:
--   - Fields must always have a value
--   - Ensures data completeness

-- DECIMAL Data Type (salary):
--   - DECIMAL(10, 2): 10 total digits, 2 after decimal point
--   - Why not FLOAT/DOUBLE: Avoids rounding errors with money
--   - Example: 75000.00 is stored exactly, not as 75000.0000001

-- TIMESTAMP Fields:
--   - created_at: Tracks when record was created
--   - updated_at: Tracks last modification time
--   - ON UPDATE: Automatically updated by MySQL

-- ============================================================================
-- USEFUL QUERIES FOR LEARNING
-- ============================================================================

-- View all employees
-- SELECT * FROM employees;

-- Find employee by ID
-- SELECT * FROM employees WHERE id = 1;

-- Find employees by department
-- SELECT * FROM employees WHERE department = 'IT';

-- Search by name (partial match)
-- SELECT * FROM employees WHERE name LIKE '%John%';

-- Get salary statistics
-- SELECT 
--     AVG(salary) as average_salary,
--     MIN(salary) as minimum_salary,
--     MAX(salary) as maximum_salary,
--     COUNT(*) as total_employees
-- FROM employees;

-- Count employees per department
-- SELECT department, COUNT(*) as employee_count FROM employees GROUP BY department;

-- Update employee salary
-- UPDATE employees SET salary = 80000 WHERE id = 1;

-- Delete employee
-- DELETE FROM employees WHERE id = 5;

-- ============================================================================
-- END OF SETUP SCRIPT
-- ============================================================================
